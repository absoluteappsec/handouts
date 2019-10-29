We assessed commit `#74e64e1ccb617c83ba1db4cbbb24a33051e169f8`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

  Task Manager

* Who does it do this for? (internal / external customer base)

  Internal Employees & External Customers

* What kind of information will it hold?

  Tasks, Notes, Projects.. could be sensitive
  Date of Birth of users

* What are the different types of roles?
  Groups: Admins, Project Managers,Team Member
  Staff and Super User attributes on user model objects

* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  Python3
  Django
  django_extensions <~ may have some security impacting pieces to it because I noticed permission setup and also template validation [in the documentation](https://django-extensions.readthedocs.io/en/latest/command_signals.html).
  mysqlclient


* 3rd party components, Examples:
  None so far

* Datastore -
   MySQL
   File handling using `django.core.files`


## Brainstorming / Risks

  * XSS - notes, projects and tasks
  * Appears to use MD5 for passwords?
  * TM employees using the product for managing their own products... ramifications?
  * noticed file uploads for profile pics - file access/handling
  * What if sensitive pics are uploaded to the projects - CONFIRMED THAT PROJECTS CAN HAVE FILES
  * Image processing... RCE? Something else like traversal/LFI/RFI?


## Checklist of things to review based on Brainstorming and Tech Stack

- [ ] Command Injection: system, call, popen, stdout, stderr, import os
- [ ] SQL Injection: raw, execute, select, where
- [ ] XSS: Autoescape, |safe, escapejs
  - [ ] Take a look at filenames and see if we render those unsafely anywhere
- [ ] File handling: `File`, `django.core.files`
- [x] CSRF on the password change?
- [ ] IDOR on Projects/Notes/Tasks/Profile
- [ ] Pattern for permission mgmt
- [ ] File Handling / Image Processing
- [ ] Make sure these two files don't have XSS taskManager/base_backend.html && taskManager/messages.html

## Mapping / Routes

#### Primary

- [x] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
  * Files are not IDOR-able, didn't see traversal

- [x] /taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
  * Are we concerned if you can download other people's profile pics. Ask staff about this.

- [x] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
  * Appears uploads are stored under the static directory which is directly accessible without authz
  * [Command Injection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/misc.py#L22-L29)
  * [SQL Injection using execute and interpolation](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L171-L174)
  * [Potential open redirection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L182-L184)

- [x] /taskManager/ping/	taskManager.views.ping	taskManager:ping
  * No CSRF Protections
  * [Command Injection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L806-L816) Confirmed
  * Without authorization and CSRF protection - this is a potential point of DDoS via CSRF-ing users

- [x] /taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
  * ~Check for CSRF~ Confirmed CSRF
  * No current password required + CSRF == High Risk
  * Using `set_password` which is built into django auth contrib :thumbsup:
  * There is no password validation - any password excepted

- [x] /taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
  * Doesn't have CSRF protections but that makes sense because its unauthenticated
  * [SQL Injection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L748-L749)
  * Length of the token
  * Check on os.urandom and "uniqueness"
  * Is 10 mins sufficient
  * Is email address unique, reset an admin's account etc.
  * Email enumeration via exception messages. [Success](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L769-L770) and [warning](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L772-L773).

- [ ] /taskManager/login/	taskManager.views.login	taskManager:login

- [ ] /taskManager/logout/	taskManager.views.logout_view	taskManager:logout
- [ ] /taskManager/register/	taskManager.views.register	taskManager:register
- [ ] /taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
- [ ] /taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

/taskManager/<project_id>/<task_id>/	taskManager.views.task_details	taskManager:task_details
/taskManager/<project_id>/<task_id>/note_create/	taskManager.views.note_create	taskManager:note_create
/taskManager/<project_id>/<task_id>/note_delete/<note_id>	taskManager.views.note_delete	taskManager:note_delete
/taskManager/<project_id>/<task_id>/note_edit/<note_id>	taskManager.views.note_edit	taskManager:note_edit
/taskManager/<project_id>/edit_project/	taskManager.views.project_edit	taskManager:project_edit
/taskManager/<project_id>/manage_tasks/	taskManager.views.manage_tasks	taskManager:manage_tasks
/taskManager/<project_id>/project_delete/	taskManager.views.project_delete	taskManager:project_delete
/taskManager/<project_id>/project_details/	taskManager.views.project_details	taskManager:project_details
/taskManager/<project_id>/task_complete/<task_id>	taskManager.views.task_complete	taskManager:task_complete
/taskManager/<project_id>/task_create/	taskManager.views.task_create	taskManager:task_create
/taskManager/<project_id>/task_delete/<task_id>	taskManager.views.task_delete	taskManager:task_delete
/taskManager/<project_id>/task_edit/<task_id>	taskManager.views.task_edit	taskManager:task_edit
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/search/	taskManager.views.search	taskManager:search
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users

#### Secondary

/admin/	django.contrib.admin.sites.index	admin:index
/admin/<app_label>/	django.contrib.admin.sites.app_index	admin:app_list
/admin/auth/group/	django.contrib.admin.options.changelist_view	admin:auth_group_changelist
/admin/auth/group/<path:object_id>/	django.views.generic.base.RedirectView
/admin/auth/group/<path:object_id>/change/	django.contrib.admin.options.change_view	admin:auth_group_change
/admin/auth/group/<path:object_id>/delete/	django.contrib.admin.options.delete_view	admin:auth_group_delete
/admin/auth/group/<path:object_id>/history/	django.contrib.admin.options.history_view	admin:auth_group_history
/admin/auth/group/add/	django.contrib.admin.options.add_view	admin:auth_group_add
/admin/auth/group/autocomplete/	django.contrib.admin.options.autocomplete_view	admin:auth_group_autocomplete
/admin/auth/user/	django.contrib.admin.options.changelist_view	admin:auth_user_changelist
/admin/auth/user/<id>/password/	django.contrib.auth.admin.user_change_password	admin:auth_user_password_change
/admin/auth/user/<path:object_id>/	django.views.generic.base.RedirectView
/admin/auth/user/<path:object_id>/change/	django.contrib.admin.options.change_view	admin:auth_user_change
/admin/auth/user/<path:object_id>/delete/	django.contrib.admin.options.delete_view	admin:auth_user_delete
/admin/auth/user/<path:object_id>/history/	django.contrib.admin.options.history_view	admin:auth_user_history
/admin/auth/user/add/	django.contrib.auth.admin.add_view	admin:auth_user_add
/admin/auth/user/autocomplete/	django.contrib.admin.options.autocomplete_view	admin:auth_user_autocomplete
/admin/jsi18n/	django.contrib.admin.sites.i18n_javascript	admin:jsi18n
/admin/login/	django.contrib.admin.sites.login	admin:login
/admin/logout/	django.contrib.admin.sites.logout	admin:logout
/admin/password_change/	django.contrib.admin.sites.password_change	admin:password_change
/admin/password_change/done/	django.contrib.admin.sites.password_change_done	admin:password_change_done
/admin/r/<int:content_type_id>/<path:object_id>/	django.contrib.contenttypes.views.shortcut	admin:view_on_site


## Mapping / Authorization Decorators

- [x] `@login_required` = have a session
  * have to have a session
- [x] `@user_passes_test(can_create_project)`
- [x] `@user_passes_test(can_edit_project)`
- [x]  @user_passes_test(can_delete_project
   * using built-in contrib.auth to look at permissions.
   * Permissions = User > Group > Auth Group Permissions
- [x] @user_passes_test(lambda u: u.is_superuser
   `is_superuser` = true
- [x] @csrf_exempt
  * CSRF check

## Mapping / Files

- [ ] settings.py
  * Secret Key is hardcoded in source
  * Simple logging [does not include timestamp](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/settings.py#L30)
  * [Emailing logs... uhhh... sensitive data](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/settings.py#L42-L43)
  * We can't even use CSRF protections, its commented out ['django.middleware.csrf.CsrfViewMiddleware'](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/settings.py#L79-L80)
  * `django.core.files.uploadhandler.TemporaryFileUploadHandler` <~ look at docs
  * [No password and harcoded creds](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/settings.py#L93-L102)
  * Messages get stored in cookies `django.contrib.messages.storage.cookie.CookieStorage`
  * Serialization issue (Pickle)
  * MD5 password hashing
  * Signed cookies (client-side cookies)

- [ ] misc.py
