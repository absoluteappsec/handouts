We assessed commit `#74e64e1ccb617c83ba1db4cbbb24a33051e169f8`

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
  * Task manager

* Who does it do this for? (internal / external customer base)
  * External Users
  * Internal users as well (there is `is_staff`)

* What kind of information will it hold?

  Projects, Tasks, Notes - names and info as well as files attached.

* What are the different types of roles?
  * project managers, admins, team members

* What aspects concern your client/customer/staff the most?
  * ERRRRYTHING

## Tech Stack

* Framework & Language
  Django 2.1.1


* 3rd party components, Examples:
  * Django Extension

* Datastore
  * MySQL - CONFIRMED


## Brainstorming / Risks

* Do we need to worry about sensitive of what is uploaded
* Do we need to worry about disclosing who is on a team
* We need to look at the ORM (mysql specific) for unsafe stuff
  - raw, execute, cursor
* Same for templating (HTML templating)
  - |safe, autoescape off
* Make sure that a user cannot access admin functionality
  * Make sure there is no mass-assignment in self-registration
* Check search functionality
* reviewing logging statements for sensitive information being written

## Checklist of things to review

- [ ] File upload functionality
- [ ] Search function
- [x] Check password change function for other issues (IDOR, CSRF)
- [ ] Look at the Django version for vulns

### Authentication

* Authentication function checks

- [ ] Password hashing mechanism
  * It looks like we might be using MD5 - verify
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


### Auditing

- [ ] If an exception occurs, does the application fails securely?
- [ ] Do error messages reveal sensitive application or unnecessary execution details?
- [ ] Are Component, framework, and system errors displayed to end user?
- [ ] Does exception handling that occurs during security sensitive processes release resources safely and roll back any transactions?
- [ ] Are relevant user details and system actions logged?
- [ ] Is sensitive user input flagged, identified, protected, and not written to the logs?
  * Credit Card #s, Social Security Numbers, Passwords, PII, keys


### Datastore

- [ ] SQL / NoSQL Injection
- [ ] Key store manipulation (memcache, redis)
- [ ] Validations?
- [ ] Typically where cryptographic operations take place such as generate authentication tokens, hashing passwords, etc.

### File handling

- [ ] How are file uploads stored
- [ ] Security controls?
  - [ ] A/V Scanning
  - [ ] Size / Filetype restrictions
- [ ] How are they retrieved (both Access Control but any sort of traversal or LFI/RFI would be interesting)

## Mapping / Routes

- [ ] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
- [ ] /taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
- [ ] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
- [ ] /taskManager/ping/	taskManager.views.ping	taskManager:ping

- [ ] /taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
  * CSRF-able
  * NOT IDOR-able

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


## Mapping / Authorization Decorators

- [ ] @login_required
- [ ] @csrf_exempt

## Mapping / Files

- [ ] settings.py
