We assessed commit `#d055f45e6fd189ab578fe4fe9d96f317f2fbfe34`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
  * task manager app (managing tasks of what kind?)
    * Contains notes, tasks, projects
    * Projects have tasks, tasks have notes - users are assigned to projects

* Who does it do this for? (internal / external customer base)

    Looks like both the company and users are leveraging the product

* What kind of information will it hold?

    * Note, project, tasks information (titles / text)
    * Images (does this mean we can upload/download?)
    * Dates of birth (PII)

* What are the different types of roles?
  * Noted in the requirements that the app uses Django Admin - probably an admin role
  * Groups available in the auth group config
    * [admin_g](https://github.com/sethlaw/vtm/blob/09433b6d12b65522a7b29c9309f125dcc10e7496/taskManager/fixtures/auth_group_permissions.json#L38), [project_managers](https://github.com/sethlaw/vtm/blob/09433b6d12b65522a7b29c9309f125dcc10e7496/taskManager/fixtures/auth_group_permissions.json#L62), [team_members](https://github.com/sethlaw/vtm/blob/09433b6d12b65522a7b29c9309f125dcc10e7496/taskManager/fixtures/auth_group_permissions.json#L80)
  * [Users also seem to have permissions](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L6-L7) independent of group permissions
  * Additional roles: `is_superuser` `is_staff`

* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  * Python3  - verify that the language version isn't outdated/insecure
  * Django 3.1.5 (make sure this version doesn't have CVEs)

* 3rd party components, Examples:
  * sqlparse (look into any vulns here)
  * xwlt (is this actually needed?) - Can we dump info with it? CSV Injection?
* Datastore
  * mysql 


## Brainstorming / Risks

* xwlt lib check for
  * CSV Injection
  * Is it necessary? Outdated?
  * Can it be used to dump data
  * Didn't see in the webapp where this was used, identify where that's at
* Only supports certain versions of Python - does that mean we're locked into a vulnerable version of Python by using this lib?
* Notes can contain any text - could this be sensitive data
* Title of projects might be sensitive to some organizations - enumeration possible?
* Does [admin user with an admin username](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L15) still exist in production?
* Looks like potentially passwords are md5 hashed
* We might be doing some file handling of profile pics - this is a risk potentially
* Browser URLs with IDs - see if we can switch those up for IDOR (Insecure Direct Object Reference) - `profile_id` `user_id` `file_id`
* Check profile image so its not malicious or nefarious content
* Check for bypasses of file types/mime types of uploaded content
* URL File Upload - is that SQL? Is it Server side request forgery? How is this working
* File size abuse
* Debug endpoints
* Access control on file uploads


## Checklist of things to review

### Risks

- [ ] Look at x endpoints for file upload vulnerabilities
  - [ ]] File size
  - [ ] ACL issues
  - [ ] How does it work?
  - [ ] Bypasses / malicious content


### Authentication

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

* Is there service-to-service authentication?
  - [ ] Constant time comparison function used
  - [ ] HMAC generated using a secure algorithm (basically not SHA1/MD5)
  - [ ] Requests occur over SSL/TLS
    - [ ] Verification of SSL/TLS is not turned off
  - [ ] Reasonable TTL implemented (meaning, an hour or less would be normal.)
  - [ ] Accounts for time skew
  - [ ] Shared secret used and stored in vault (not hardcoded)
  - [ ] Unit-tests for:
    * Check fails if token/hmac/nonce/etc. is missing or mismatched
    * Failure if timestamp is missing or expired
    * Failure if signature verification fails

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

### Auditing/Logging

- [ ] If an exception occurs, does the application fails securely?
- [ ] Do error messages reveal sensitive application or unnecessary execution details?
- [ ] Are Component, framework, and system errors displayed to end user?
- [ ] Does exception handling that occurs during security sensitive processes release resources safely and roll back any transactions?
- [ ] Are relevant user details and system actions logged?
- [ ] Is sensitive user input flagged, identified, protected, and not written to the logs?
  * Credit Card #s, Social Security Numbers, Passwords, PII, keys


### Injection

- [ ] OS
  - [ ] import os
  - [ ] `subprocess`
- [ ] SQL
  - [ ] `raw`, `extra`  `get_prep_value()`
- [ ] HTML
  - [ ] `|safe`
  - [ ] `{% autoescape off %}`
  - [ ] `data|default:`

### Cryptography


### Configuration


## Mapping / Routes

### High risk endpoints
#### Authz/n endpoints

- [x] /taskManager/register/	taskManager.views.register	taskManager:register
 * looked for xss, nothing
 * looked pretty solid - need to look at any ways to mass assign as we're creating a user object out of all the form details
- [ ] /taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
- [ ] /taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
- [ ] /taskManager/login/	taskManager.views.login	taskManager:login
- [ ] /taskManager/logout/	taskManager.views.logout_view	taskManager:logout

#### Sensitive operations

- [ ] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
- [ ] /taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
- [ ] /taskManager/ping/	taskManager.views.ping	taskManager:ping
- [ ] /taskManager/profile/	taskManager.views.profile	taskManager:profile
- [ ] /taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
- [ ] /taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view


### Medium risk

- [ ] /taskManager.views.index	index	login_required

- [ ] /taskManager/	taskManager.views.index	taskManager:index
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
- [ ] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
- [ ] /taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
- [ ] /taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard
- [ ] /taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
- [ ] /taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
- [ ] /taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
- [ ] /taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
- [ ] /taskManager/search/	taskManager.views.search	taskManager:search
- [ ] /taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
- [ ] /taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
- [ ] /taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users
- [ ] /taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

### Lower Priority

#### Admin Django built-in

- [ ] /admin/	django.contrib.admin.sites.index	admin:index
- [ ] /admin/<app_label>/	django.contrib.admin.sites.app_index	admin:app_list
- [ ] /admin/auth/group/	django.contrib.admin.options.changelist_view	admin:auth_group_changelist
- [ ] /admin/auth/group/<path:object_id>/	django.views.generic.base.RedirectView
- [ ] /admin/auth/group/<path:object_id>/change/	django.contrib.admin.options.change_view	admin:auth_group_change
- [ ] /admin/auth/group/<path:object_id>/delete/	django.contrib.admin.options.delete_view	admin:auth_group_delete
- [ ] /admin/auth/group/<path:object_id>/history/	django.contrib.admin.options.history_view	admin:auth_group_history
- [ ] /admin/auth/group/add/	django.contrib.admin.options.add_view	admin:auth_group_add
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

- [ ] csrf_exempt

## Mapping / Files

- [ ] settings.py