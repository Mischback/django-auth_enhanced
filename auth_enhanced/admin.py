# -*- coding: utf-8 -*-
"""Contains app-specific admin classes."""

# Django imports
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# app imports
from auth_enhanced.models import UserEnhancement


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

    def get_actions(self, request):
        """Extends the default 'get_actions()'-method to exclude the bulk
        action 'delete objects' from the dropdown."""

        # get the original list of actions
        actions = super(EnhancedUserAdmin, self).get_actions(request)

        # remove the action from the dropdown
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions


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
