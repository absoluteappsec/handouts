We assessed commit `#abcd134`

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
* Who does it do this for? (internal / external customer base)
* What kind of information will it hold?
* What are the different types of roles?
* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language - Rails/Ruby, Django/Python, mux/Golang
* 3rd party components, Examples:
  * Billing libraries (rubygem, npm, jar, etc.)
  * JavaScript widgets - (marketing tracking, sales chat widget)
  * Reliant upon other applications - such as receiving webhook events
* Datastore - Postgresql, MySQL, Memcache, Redis, Mongodb, etc.


## Brainstorming / Risks

* Here is what the feature or product is supposed to do... what might go wrong?
* Okay - based on the tech stack, I've realized that the:
  * ORM - Does SQLi in _this_ way
  * Template language introduces XSS in _this_ way

## Checklist of things to review

### Risks
- [ ] Look for instances of `| safe` in the template/views
- [ ] Look for OS commands
- [ ] Look at the ORM for instances of `createNativeQuery()`
- [ ] Developer expected `x` but I think we should try to see if `y` is possible

## Mapping / Routes

- [ ] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
- [ ] /taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
- [ ] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
- [ ] /taskManager/ping/	taskManager.views.ping	taskManager:ping
- [ ] /taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
- [ ] /taskManager/forgot_password/	taskManager.views.forgot_password
- [ ] /taskManager/login/	taskManager.views.login	taskManager:login
- [ ] /taskManager/logout/	taskManager.views.logout_view	taskManager:logout
- [ ] /taskManager/register/	taskManager.views.register	taskManager:register
- [ ] /taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
- [ ] /taskManager/view_img/	taskManager.views.view_img	taskManager:view_img
- [ ] /taskManager/<project_id>/<task_id>/	taskManager.views.task_details	taskManager:task_details
- [ ] /taskManager/<project_id>/<task_id>/note_create/	taskManager.views.note_create	taskManager:note_create
- [ ] /taskManager/<project_id>/<task_id>/note_delete/<note_id>	taskManager.views.note_delete	taskManager:note_delete
- [ ] /taskManager/<project_id>/<task_id>/note_edit/<note_id>	taskManager.views.note_edit	taskManager:note_edit
- [ ] /taskManager/<project_id>/edit_project/	taskManager.views.project_edit	taskManager:project_edit
- [ ] /taskManager/<project_id>/manage_tasks/	taskManager.views.manage_tasks	taskManager:manage_tasks
- [ ] /taskManager/<project_id>/project_delete/	taskManager.views.project_delete	taskManager:project_delete
- [ ] /taskManager/<project_id>/project_details/	taskManager.views.project_details	taskManager:project_details
- [ ] /taskManager/<project_id>/task_complete/<task_id>	taskManager.views.task_complete	taskManager:task_complete
- [ ] /taskManager/<project_id>/task_create/	taskManager.views.task_create	taskManager:task_create
- [ ] /taskManager/<project_id>/task_delete/<task_id>	taskManager.views.task_delete	taskManager:task_delete
- [ ] /taskManager/<project_id>/task_edit/<task_id>	taskManager.views.task_edit	taskManager:task_edit
- [ ] /taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
- [ ] /taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
- [ ] /taskManager/profile/	taskManager.views.profile	taskManager:profile
- [ ] /taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
- [ ] /taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
- [ ] /taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
- [ ] /taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
- [ ] /taskManager/search/	taskManager.views.search	taskManager:search
- [ ] /taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
- [ ] /taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
- [ ] /taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users
- [ ] /admin/	django.contrib.admin.sites.index	admin:index
- [ ] /admin/<app_label>/	django.contrib.admin.sites.app_index	admin:app_list
- [ ] /admin/auth/group/	django.contrib.admin.options.changelist_view	admin:auth_group_changelist
- [ ] /admin/auth/group/<path:object_id>/	django.views.generic.base.RedirectView
- [ ] /admin/auth/group/<path:object_id>/change/	django.contrib.admin.options.change_view	admin:auth_group_change
- [ ] /admin/auth/group/<path:object_id>/delete/	django.contrib.admin.options.delete_view	admin:auth_group_delete
- [ ]  /admin/auth/group/<path:object_id>/history/	django.contrib.admin.options.history_view	admin:auth_group_history
- [ ]  /admin/auth/group/add/	django.contrib.admin.options.add_view	admin:auth_group_add
- [ ] /admin/auth/group/autocomplete/	django.contrib.admin.options.autocomplete_view	admin:auth_group_autocomplete
- [ ] /admin/auth/user/	django.contrib.admin.options.changelist_view	admin:auth_user_changelist
- [ ] /admin/auth/user/<id>/password/	django.contrib.auth.admin.user_change_password	admin:auth_user_password_change
- [ ] /admin/auth/user/<path:object_id>/	django.views.generic.base.RedirectView
- [ ] /admin/auth/user/<path:object_id>/change/	django.contrib.admin.options.change_view	admin:auth_user_change
- [ ] /admin/auth/user/<path:object_id>/delete/	django.contrib.admin.options.delete_view	admin:auth_user_delete
- [ ] /admin/auth/user/<path:object_id>/history/	django.contrib.admin.options.history_view	admin:auth_user_history
- [ ] /admin/auth/user/add/	django.contrib.auth.admin.add_view	admin:auth_user_add
- [ ] /admin/auth/user/autocomplete/	django.contrib.admin.options.autocomplete_view	admin:auth_user_autocomplete
- [ ] /admin/jsi18n/	django.contrib.admin.sites.i18n_javascript	admin:jsi18n
- [ ] /admin/login/	django.contrib.admin.sites.login	admin:login
- [ ] /admin/logout/	django.contrib.admin.sites.logout	admin:logout
- [ ] /admin/password_change/	django.contrib.admin.sites.password_change	admin:password_change
- [ ] /admin/password_change/done/	django.contrib.admin.sites.password_change_done	admin:password_change_done
- [ ] /admin/r/<int:content_type_id>/<path:object_id>/	django.contrib.contenttypes.views.shortcut	admin:view_on_site

## Mapping / Authorization Decorators

- [ ]

## Mapping / Files

- [ ]

## Authentication

* Authentication function checks

- [ ] Password hashing mechanism
- [ ] Timing attacks - this could be username/password or HMAC operations verifying keys
- [ ] Forgot Password
- [ ] 2 factor auth
- [ ] Enumeration... if it matters
- [ ] Signup
- [ ] Brute force attacks
- [ ] Session Management Issues
  - [ ] Session Fixation
  - [ ] Session Destruction
  - [ ] Session Length

### Authorization

- [ ] Identify Roles
- [ ] Identify sensitive/privileged endpoints
- [ ] Identify authz expectations specific to the business purpose of the app
  * Can non-privileged users view, add, or alter accounts?
  * Is there functionality to add accounts with higher access levels than their own access?
  * How is separation of duties handled?
- [ ] Identify Authorization functions/filtes
  * Do they take Tokens? Cookies? Custom or handled by a framework?

* Broken Access Control
  - [ ] Insecure Direct Object Reference (`find_by`, `find`, `findOne`, `findAll`, etc)
  - [ ] Missing Function Level Access Control
  - [ ] Verify Authorization Filters

* Generic authz flaws
  - [ ] Sensitive Data Exposure
  - [ ] Mass Assignment
  - [ ] Business Logic Flaws
  - [ ] Are CSRF Protections applied correctly
  - [ ] Are users forced to re-assert their credentials for requests that have critical side-effect (account changes, password reset, etc)?


## Auditing

- [ ] If an exception occurs, does the application fails securely?
- [ ] Do error messages reveal sensitive application or unnecessary execution details?
- [ ] Are Component, framework, and system errors displayed to end user?
- [ ] Does exception handling that occurs during security sensitive processes release resources safely and roll back any transactions?
- [ ] Are relevant user details and system actions logged?
- [ ] Is sensitive user input flagged, identified, protected, and not written to the logs?
  * Credit Card #s, Social Security Numbers, Passwords, PII, keys


## Datastore

- [ ] SQL / NoSQL Injection
- [ ] Key store manipulation (memcache, redis)
- [ ] Validations?
- [ ] Typically where cryptographic operations take place such as generate authentication tokens, hashing passwords, etc.

## File handling

- [ ] How are file uploads stored
- [ ] Security controls?
  - [ ] A/V Scanning
  - [ ] Size / Filetype restrictions
- [ ] How are they retrieved (both Access Control but any sort of traversal or LFI/RFI would be interesting)
