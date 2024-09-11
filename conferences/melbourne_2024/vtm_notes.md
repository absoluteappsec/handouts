We assessed commit `#e1b245b78a0b8b36361f988a4a065a4ac5524f18`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

task manager

 It appears to have a schema of Notes > Tasks > Projects

* Who does it do this for? (internal / external customer base)

 Does this for internal & external because tm.com and zerocool.net emails are used in the seeds file.

* What kind of information will it hold?
  - PII (SSN, DOB)

* What are the different types of roles?

    [admin_g, team_members, project_managers](https://github.com/redpointsec/vtm/blob/09433b6d12b65522a7b29c9309f125dcc10e7496/taskManager/fixtures/auth_group_permissions.json#L80)

    It appears these roles are managed outside authz: ` "is_staff": ` & `"is_superuser"`


* What aspects concern your client/customer/staff the most?


## Tech Stack

* Framework & Language
    - Django - 3.2.21
    - Python 3
* 3rd party components, Examples:
    pytz==2020.5
    screen==1.0.1 (What is this used for? Screen width? Ask developers)
    sqlparse==0.4.4 (sqlparse is a non-validating SQL parser for Python. It provides support for parsing, splitting and formatting SQL statements.)
    xlwt==1.3.0
    requests==2.31.0
    django-health-check==3.16.5
    psutil==5.9.5
* Datastore
 - MySQl


## Brainstorming / Risks

* Need to look into sqlparse and its non-validating behavior
* MySQL - Look for SQL Injection
* Screen - looks to be an unsupported library, outdated, and not sure about its usage
* Check if requests has issues. The main thing here is, I need to know why the application is making requests out to other services.
* Sequential IDs for Note records, just mentioning for IDOR later
* Unsure of how much JS validation is occurring but notes appear to have XSS data in the unit-test
* Are user passwords MD5 hashed? According to the users.json fixture, it appears that way
* We're handling SSN/DOB so we need to look closely at logging, at encryption, at every point those values flow in the app.
* File handling of profile images and this happens to stored locally on the file system so now we need to go and look for all the standard vulns around handling files on your filesystem
* [Looks like there is potentially no password validation](https://github.com/redpointsec/vtm/blob/078c92d10285fbb717bb991308a85a302d0009e8/taskManager/tests.py#L49)
* Since we are loading XSS strings into fixtures, we should also have tests.
* I saw csrf_exempt used, we should see WHY that is the case
* See if they are chaining templates with the `render()` function
* View site to see if its actually employing a CSP because I don't see it in the code

## Checklist of things to review

### Risks
- [ ] 

### Authentication
- [ ] Login page give error messages, check for enumeration
- [ ] Signup page allows for freeform passwords, does it implement proper password complexity?

### Authorization
* Uses @login_required, @csrf_exempt, and @user_passes_test
- [ ] Investigate superuser "view all users"
- [ ] Identify Roles
- [ ] Identify sensitive/privileged endpoints
- [ ] Identify authz expectations specific to the business purpose of the app
  * Can non-privileged users view, add, or alter accounts?
  * Is there functionality to add accounts with higher access levels than their own access?
  * How is separation of duties handled?
- [ ] Identify Authorization functions/filters
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
- [ ] Logging configuration is in `settings.py`, check documentation for secure settings

### Injection
- [ ] XSS - autoescape off and |safe

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

### High

/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
/taskManager/login/	taskManager.views.login	taskManager:login
/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users
    - [FOLLOW-UP] dig in further on the u.is_superuser lambda
    - [FOLLOW-UP] Appears that the header uses `|safe` to output the username on the page

/taskManager/ping/	taskManager.views.ping	taskManager:ping
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
/ht/	health_check.views.MainView	health_check:health_check_home

### Med

/taskManager/	taskManager.views.index	taskManager:index
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
/taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard
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
/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

### Low

/taskManager.views.index	index	login_required


## Mapping / Authorization Decorators

- [ ] `ensure_logged_in`

## Mapping / Files

- [ ] settings.py
- [ ] misc.py
  * [FOLLOW-UP] Contains system calls and other potentially dangerous functions
