We assessed commit `f9f02443446e2b455cc3f3fd8eccd2308cdc56cd`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

  * vulnerable task manager
   * Missing many test cases, especially around authz - potential risk we need to view.

* Who does it do this for? (internal / external customer base)

  * [both, probably](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L96-L97)

* What kind of information will it hold?
  * Dates of Birth
  * Image/Image locations
  * Reset Tokens for Users
* What are the different types of roles?
  * [admins, team members, project managers](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/auth_group_permissions.json#L1-L84)
  * [`Superusers, isStaff`](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L7-L8)

* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  * Python 3
  * Django 3.1.5
* 3rd party components
  * sqlparse
  * xlwt - excel spreadsheet stuff
* Datastore
  * MySQL


## Brainstorming / Risks

* sqlparse performs non validating parsing of statements, might be used with raw queries - investigate later
* xlwt - build is failing, docs are failing - is this updated/maintained?
  * Possible csv injection
* [UserProfile has some interesting fields like DoB, Images - let's look at RFI/LFI](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/migrations/0001_initial.py#L36-L40)
* There are [text/title](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/migrations/0001_initial.py#L47-L49) fields that are likely rendered all throughout the application
* Notes default to ID of 1, if you deleted task 1 - it could potentially lose the relationship to the ORM.
  * Could lead to cascading authz issues
* File model has potential for LFI/RFI/Traversal and any other file related issues (sizing, MIME bypasses etc) https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/migrations/0001_initial.py#L68-L74
* Looks like some of the user seed data does use is_staff and superuser so we should figure out how this actually works and look at the docs
* Ensure test accounts aren't enabled in prod
* Regex in routing - lookup security issues and known nuances to Django routijng

## Checklist of things to review

- [ ] Users appear to have [md5 passwords](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L12-L13)
- [ ] Look for mass assignment to see if you can override the role attributes to give yourself administrative or elevated access

### Risks
- [ ] Look for instances of `| safe` in the template/views
- [ ] Look for OS commands
- [ ] Look at the ORM for instances of `createNativeQuery()`
- [ ] Developer expected `x` but I think we should try to see if `y` is possible

### Authentication
- [ ] Does appear to have a [lockout mechanism](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L10) maybe, so we need to ensure that its done correctly.
- [ ] Login page give error messages, check for enumeration
- [ ] Signup page allows for freeform passwords, does it implement proper password complexity?

### Authorization
- [ ] Uses @login_required decorator, is it applied on all endpoints appropriately?

### Auditing/Logging
- [ ] Logging configuration is in `settings.py`, check documentation for secure settings

### Injection
- [ ] XSS - `|safe`

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

### High

/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/login/	taskManager.views.login	taskManager:login
/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload

- [ ] /taskManager/ping/	taskManager.views.ping	taskManager:ping
  * **FINDING** looks like [`csrf_exempt`](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L859-L860) is on this route - is it GET only?
  * **FINDING** No authorization decorator applied
  * The [regex match might](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L865-L866) allow other commands thru - there are specific commands the application does not want you to use - but it seems its possible other commands will make it thru.
  * Looks to have been a [command injection](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L868-L869) issue before but the user-supplied input is concanetated into the command string
  * [XSS](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/templates/taskManager/base_backend.html#L56-L57)


### Med

/taskManager/	taskManager.views.index	taskManager:index
/taskManager/<project_id>/<task_id>/	taskManager.views.task_details	taskManager:task_details
/taskManager/<project_id>/<task_id>/note_create/	taskManager.views.note_create	taskManager:note_create
/taskManager/<project_id>/<task_id>/note_delete/<note_id>	taskManager.views.note_delete	taskManager:note_delete
/taskManager/<project_id>/<task_id>/note_edit/<note_id>	taskManager.views.note_edittaskManager:note_edit
/taskManager/<project_id>/edit_project/	taskManager.views.project_edit	taskManager:project_edit
/taskManager/<project_id>/manage_tasks/	taskManager.views.manage_tasks	taskManager:manage_tasks
/taskManager/<project_id>/project_delete/	taskManager.views.project_delete	taskManager:project_delete
/taskManager/<project_id>/project_details/	taskManager.views.project_details	taskManager:project_details
/taskManager/<project_id>/task_complete/<task_id>	taskManager.views.task_complete	taskManager:task_complete
/taskManager/<project_id>/task_create/	taskManager.views.task_create	taskManager:task_create
/taskManager/<project_id>/task_delete/<task_id>	taskManager.views.task_delete	taskManager:task_delete
/taskManager/<project_id>/task_edit/<task_id>	taskManager.views.task_edit	taskManager:task_edit

### Low

/	taskManager.views.index	index	login_required

/taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard

/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects

/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/search/	taskManager.views.search	taskManager:search
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list

/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

## Mapping / Authorization Decorators

- [ ] [`@login_required`](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L530-L531)
  * This is a default Django built in function to make sure the user has a session - it is not a role based access (RBAC) control
- [ ] [@user_passes_test(lambda u: u.is_superuser)](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L531-L532)
- [ ] [@user_passes_test(can_create_project)](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L354-L355)
- [ ] [@user_passes_test(can_edit_project)](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L384-L385)
- [ ] [@user_passes_test(can_delete_project)](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L411-L412)
- [ ] [@csrf_exempt](https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L726-L727)

## Mapping / Files

- [ ] https://github.com/sethlaw/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/misc.py#L1-L2
  * This file appears to have some system level functionality - possible OS Injection%
