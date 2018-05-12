App-specific Settings
=====================

**django-auth_enhanced** provides various settings to be as flexible and
pluggable as possible.

This section lists all available settings with their respective default values.
To alter any of these settings, simply include them in your project's settings
module.

**django-auth_enhanced** will check its settings automatically for validity
and report any errors with detailled hints.


Available Settings
------------------

.. glossary::

    DAE_ADMIN_LIST_DISPLAY
        TODO: document this setting!

    DAE_ADMIN_SHOW_SEARCHBOX
        TODO: document this setting!

    DAE_ADMIN_SIGNUP_NOTIFICATION
        Controls, if admins / superusers will be notified of new signups.

        **Accepted Values:**

        * ``False`` (default value): No notification will be sent.
        * a tuple of the following structure: ``('django', 'django@localhost', ('mail', )),``, where ``'django'`` is a username, ``'django@localhost'`` a valid email address and ``('mail', )`` a tuple of notification methods. As of now, only ``'mail'`` is supported.

    DAE_ADMIN_USERNAME_STATUS_COLOR
        TODO: document this setting!

    DAE_EMAIL_ADMIN_NOTIFICATION_PREFIX
        All emails to admins / superusers will have a subject, that is prefixed
        with this string, put in ``[]``, i.e. if this setting is set to ``'foo'``,
        the subject of mails will be ``[foo] Some generic mail to admins``. If
        this setting is set to ``''``, the subject will be ``Some generic mail
        to admins``.

        **Accepted Values:**

        * a string (default value ``''``)

    DAE_EMAIL_FROM_ADDRESS
        All emails sent by this app will use this *from*-address.

        Please note, that the default value relies on Django's
        ``DEFAULT_FROM_EMAIL``, see `Django's documentation <https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email>`_
        for more details.

        **Accepted Values:**

        * all valid mail addresses

    DAE_EMAIL_PREFIX
        All emails sent to *normal users* will have a subject, that is prefixed
        with this string, put in ``[]``, i.e. if this setting is set to ``'foo'``,
        the subject of mails will be ``[foo] Some generic mail to users``. If
        this setting is set to ``''``, the subject will be ``Some generic mail
        to users``.

        **Accepted Values:**

        * a string (default value ``''``)

    DAE_EMAIL_TEMPLATE_PREFIX
        This setting determines, where to look for email templates.

        **django-auth_enhanced** makes use of Django's template engine to create
        its email messages. This setting allows you, to seperate your email
        templates from the html-templates.

        **Example:** Let's assume your Django project is set up to look for
        templates in the following path ``project_root/templates/``. By putting
        this setting to ``auth_enhanced/mail``, Django will search the path
        ``project_root/templates/auth_enhanced/mail/`` for mail templates.

        **Accepted Values:**

        * a string, that can be suffixed to a path. Please note, that this **must not include** a trailing slash (``'mail'`` instead of ``'mail/'``).

    DAE_OPERATION_MODE
        This is the most important setting of **django-auth_enhanced**,
        determing how newly registered users are handled.

        **Accepted Values:**

        * ``'auto'`` (default value): This automatic mode is the closest to Django's default behaviour. Newly registered users are activated by default and are immediatly able to login.
        * ``'email-verification'``: In this mode, the user is required to verify his email address. An automatically generated email is sent, including a verification link/token. His account is activated when the address is verified. This mode will automatically include an email field in the signup form.
        * ``'manual'``: This mode requires manual activation of newly created users. Admins/superusers will have to log into the administration backend and activate the user.

    DAE_SALT
        This salt is used to seperate different signing processes in your
        project nicely seperated. See `Django's documentation <https://docs.djangoproject.com/en/dev/topics/signing/#using-the-salt-argument>`_
        for more details.

        **Accepted Values:**

        * a string (default value ``'django-auth_enhanced'``)

    DAE_VERIFICATION_TOKEN_MAX_AGE
        This setting determines, how long any verification token is considered
        valid in the application.

        **Accepted Values:**

        * an integer, specifying the maximum age in seconds
        * a string, with ``h`` as its last character and any number of digits, that is parsable into an integer value. This will be calculated as a given amount of hours, i.e. ``'2h'`` means two hours
        * a string, with ``d`` as its last character and any number of digits, that is parsable into an integer value. This will be calculated as a given amount of days, i.e. ``'1d'`` means one day or 24 hours

        The default value is ``3600``, so all tokens are valid for one hour.


Developer's Description
-----------------------

**django-auth_enhanced** *injects* the default values of its settings on
startup, using the ``AppConfig.ready()``-method (**Yes**, this is
discouraged explicitly in Django's documentation, but it is easily the best way
to provide default settings for app-specific settings).

If you want to have a look into it: the *AppConfig* ``AuthEnhancedConfig`` is
found in ``apps.py``. However, the actual injection-functions are found in
``settings.py``.

The checks for validity are performed by Django's built-in check framework.
The app-specific checks can be found in ``checks.py``.
