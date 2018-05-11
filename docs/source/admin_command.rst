Admin Commands
==============

**django-auth_enhanced** provides an app-specific admin command, to check some
of the inner mechanics of the application.

This section describes this command and its functions.


Unique Emails
-------------

One of the features of **django-auth_enhanced** is the enforcement of unique
email addresses. The original and default, Django-built in ``User`` is not
extended or modified, so, unique email addresses are not enforced on
database-level.

Instead, by using **django-auth_enhanced**'s forms will validate given email
addresses to ensure, that they are not yet associated with another account.

As an additional check, a management command is provided to check the project
for not unique email addresses.

.. code-block:: bash

    $ python manage.py authenhanced unique-email

This command will check all email addresses and report user accounts, that use
non-unique addresses.

If all addresses are unique, it will output a success message.


Admin Notifications
-------------------

By using the app's setting :term:`DAE_ADMIN_SIGNUP_NOTIFICATION`, superusers
may enable a notification about the newly registered user.

The setting is checked, using `Django's system check framework
<https://docs.djangoproject.com/en/dev/ref/checks/>`_, but only regarding
*syntactically* correct values.

This command checks furthermore, whether the specified usernames belong to an
actual superuser and if the user's email address is verified and associated
with the given account.

.. code-block:: bash

    $ python manage.py authenhanced admin-notification

The command will report any issues or print a success message.
