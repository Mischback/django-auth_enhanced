# -*- coding: utf-8 -*-
"""Contains app-specific admin classes."""

# Django imports
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.messages import ERROR, SUCCESS, WARNING
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

# app imports
from auth_enhanced.models import UserEnhancement
from auth_enhanced.settings import DAE_CONST_MODE_EMAIL_ACTIVATION


def register_only_debug(*models, **kwargs):
    """Register the given model(s) classes and wrapped ModelAdmin class with
    admin site, if DEBUG=True in project's settings.

    See https://github.com/django/django/blob/master/django/contrib/admin/decorators.py
    for the original Django implementation.

    TODO: Using '**kwargs' doesn't mimic Django2.0 codebase, but Django1.11!"""

    # need a callable here, but just 'pass'ing is fine...
    def _wrapper_noop(admin_class):
        pass

    if settings.DEBUG:
        # re-use Django's register-decorator
        return admin.register(*models, **kwargs)

    # return a noop
    return _wrapper_noop


class EnhancedUserStatusFilter(admin.SimpleListFilter):
    """Custom SimpleListFilter to filter on user's status"""

    # the title of this filter
    title = _('status')

    # the parameter in the URL
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """Controls the options in the filter list.

        First value in the tuple: parameter in the query string
        Second value: The caption for the filter list"""

        return (
            ('users', _('Users')),
            ('staff', _('Staff')),
            ('superusers', _('Superusers'))
        )   # pragma nocover

    def queryset(self, request, queryset):
        """This actually modifies the queryset, if the filter is applied."""

        if self.value() == 'users':
            return queryset.filter(is_staff=False).filter(is_superuser=False)

        if self.value() == 'staff':
            return queryset.filter(is_staff=True)

        if self.value() == 'superusers':
            return queryset.filter(is_superuser=True)

        return queryset


class EnhancedUserAdmin(UserAdmin):
    """This class substitutes the default admin interface for user objects.

    It is designed to enhance and substitute the default admin interface
    provided by 'django.contrib.auth'. But furthermore, it should be as
    pluggable as possible, to be able to deal with custom user models."""

    # 'list_display' controls, which fields will be displayed in the list view.
    # This is configurable with an app-specific setting or will be left at
    # Django's default value:
    #   ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # TODO: Django already checks the value of 'list_display', so it might be
    #   unnecessary to actually check DAE_ADMIN_LIST_DISPLAY within the app.
    #   However, it should be ensured, that the app's setting only includes
    #   valid values, which depends on the AUTH_USER_MODEL in use.
    try:
        list_display = settings.DAE_ADMIN_LIST_DISPLAY
    except AttributeError:
        pass

    # 'list_filter' controls, which filters will be usable in the list view.
    # Django's default admin class provides the following list:
    #   ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_filter = (EnhancedUserStatusFilter, 'is_active', 'groups')

    # 'search_fields' determines the target fields for the search box
    # The search box can be disabled with an app-specific setting, accordingly
    #   the 'search_field' will be set to an empty tuple.
    try:
        if not settings.DAE_ADMIN_SHOW_SEARCHBOX:
            search_fields = ()
            setattr(settings, 'DAE_ADMIN_SHOW_SEARCHBOX', False)
    except AttributeError:
        # following line is exactly Django's default. Doesn't need to be set!
        # search_fields = ('username', 'email', 'first_name', 'last_name')
        setattr(settings, 'DAE_ADMIN_SHOW_SEARCHBOX', True)

    # 'ordering' controls the default ordering of the list view
    # Django's default value is just 'username'
    ordering = ('-is_superuser', '-is_staff', 'is_active', 'username')

    # 'list_select_related' will automatically add an 'select_related'
    #   statement to the queryset and thus reduce the number of SQL queries.
    list_select_related = ('enhancement',)

    actions = ['action_bulk_activate_user', ]

    def action_bulk_activate_user(self, request, queryset, user_id=None):
        """Performs bulk activation of users in Django admin.

        This action is accessible from the drop-down menu and works together
        with selecting user objects by checking their respective checkbox.
        Furthermore, it handles the actual activation of single user aswell,
        because ultimatively, this method is used to perform the activation
        when 'action_activate_user()' is called."""

        activated = []
        not_activated = []
        user_model = get_user_model()

        # the method is called from 'action_activate_user', so a queryset has
        #   to be constructed...
        if user_id and not queryset:
            try:
                queryset = [user_model.objects.get(pk=user_id)]
            except user_model.DoesNotExist:
                # provide an empty queryset. This mimics the behaviour of
                #   Django, if invalid user IDs are provided in the POST-request
                queryset = []

        # at this point, 'queryset' is filled and can be iterated
        for user in queryset:
            if (
                settings.DAE_OPERATION_MODE == DAE_CONST_MODE_EMAIL_ACTIVATION and
                not user.enhancement.email_is_verified
            ):
                not_activated.append(getattr(user, user_model.USERNAME_FIELD))
            else:
                user.is_active = True
                user.save()
                activated.append(getattr(user, user_model.USERNAME_FIELD))

        # return messages for successfully activated accounts
        if activated:
            count = len(activated)
            self.message_user(
                request,
                ungettext_lazy(
                    '%(count)d user was activated successfully (%(activated_list)s).',
                    '%(count)d users were activated successfully (%(activated_list)s).',
                    count
                ) % {
                    'count': count,
                    'activated_list': ', '.join(activated),
                },
                SUCCESS,
            )

        # return messages for accounts, that could not be activated, because
        #   their mail address is not verified
        if not_activated:
            count = len(not_activated)
            self.message_user(
                request,
                ungettext_lazy(
                    "%(count)d user could not be activated, because his email "
                    "address is not verified (%(activated_list)s)!",
                    "%(count)d users could not be activated, because their "
                    "email addresses are not verified (%(activated_list)s)!",
                    count
                ) % {
                    'count': count,
                    'activated_list': ', '.join(not_activated),
                },
                ERROR,
            )

        # the method did nothing; this means something unexpected happened,
        #   i.e. invalid user IDs were provided
        if not (activated or not_activated):
            self.message_user(
                request,
                _('Nothing was done. Probably this means, that no or invalid user IDs were provided.'),
                ERROR,
            )
    action_bulk_activate_user.short_description = _('Activate selected users')

    def changelist_view(self, request, extra_context=None):
        """Pass some more context into the view.

        This is used to:
            - provide the legend for color-coded or prefixed usernames.

        The legend will be provided at the bottom of the list. Please note,
        that a modified/extended template is used to provide the actual
        HTML-code for this."""

        extra_context = extra_context or {}
        extra_context['enhanceduseradmin_legend'] = self.get_additional_legend()

        return super(EnhancedUserAdmin, self).changelist_view(request, extra_context=extra_context)

    def email_with_verification_status(self, user_obj):
        """Combines the email-address and the email's verification status."""

        # get the icon
        icon = _boolean_icon(user_obj.enhancement.email_is_verified)

        return format_html('{} {}', icon, getattr(user_obj, user_obj.EMAIL_FIELD))
    email_with_verification_status.short_description = _('EMail Address')
    email_with_verification_status.admin_order_field = '-email'

    def get_actions(self, request):
        """Extends the default 'get_actions()'-method to exclude the bulk
        action 'delete objects' from the dropdown."""

        # get the original list of actions
        actions = super(EnhancedUserAdmin, self).get_actions(request)

        # remove the action from the dropdown
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    def get_additional_legend(self):
        """Returns a legend depending on the applied settings.

        Especially relevant is the 'list_display' attribute of this class and
        the settings of 'DAE_ADMIN_USERNAME_STATUS_CHAR' and
        'DAE_ADMIN_USERNAME_STATUS_COLOR'."""

        result = {}

        try:
            if 'username_status_char' in self.list_display:
                result['char'] = settings.DAE_ADMIN_USERNAME_STATUS_CHAR
        except AttributeError:
            pass

        try:
            if 'username_status_color' in self.list_display:
                result['color'] = settings.DAE_ADMIN_USERNAME_STATUS_COLOR
        except AttributeError:
            pass

        return result

    def status_aggregated(self, user_obj):
        """Returns the status of an user as string.

        Possible values: 'user', 'staff', 'superuser'; these strings will be
        localized."""

        status = _('user')
        if user_obj.is_superuser:
            status = _('superuser')
        elif user_obj.is_staff:
            status = _('staff')

        return status
    status_aggregated.short_description = _('Status')

    def username_status_char(self, user_obj):
        """Returns the username with a prefix, according to its status."""

        try:
            char = settings.DAE_ADMIN_USERNAME_STATUS_CHAR
        except AttributeError:
            return getattr(user_obj, user_obj.USERNAME_FIELD)

        if user_obj.is_superuser:
            obj_char = char[0]
        elif user_obj.is_staff:
            obj_char = char[1]
        else:
            return getattr(user_obj, user_obj.USERNAME_FIELD)

        return format_html('[{}]{}', obj_char, getattr(user_obj, user_obj.USERNAME_FIELD))
    username_status_char.short_description = _('Username (status)')
    username_status_char.admin_order_field = '-username'

    def username_status_color(self, user_obj):
        """Returns a colored username, according to its status."""

        try:
            color = settings.DAE_ADMIN_USERNAME_STATUS_COLOR
        except AttributeError:
            return getattr(user_obj, user_obj.USERNAME_FIELD)

        if user_obj.is_superuser:
            obj_color = color[0]
        elif user_obj.is_staff:
            obj_color = color[1]
        else:
            return getattr(user_obj, user_obj.USERNAME_FIELD)

        return format_html(
            '<span style="color: {};">{}</span>',
            obj_color,
            getattr(user_obj, user_obj.USERNAME_FIELD)
        )
    username_status_color.short_description = _('Username (status)')
    username_status_color.admin_order_field = '-username'


@register_only_debug(UserEnhancement)
class UserEnhancementAdmin(admin.ModelAdmin):
    """Integrates UserEnhancement into Django's admin menu.

    This ModelAdmin is just used for development and should not be registered
    in real production versions.
    UserEnhancements will be integrated into the respective admin class for
    the User-objects."""
    pass


# substitute the default implementation of the user admin
# TODO: should this be configurable?
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), EnhancedUserAdmin)
