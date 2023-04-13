We assessed commit `f9f02443446e2b455cc3f3fd8eccd2308cdc56cd`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
Task manager

* Who does it do this for? (internal / external customer base)

  * Looks like both tm employees and external customers: ["email": "dade@zerocool.net",](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L96-L97)

* What kind of information will it hold?
 * PII / DoB
 * Notes data - title, text, image? (with a date), 
 * Tasks data
 * Projets which have multiple users assigned to them and title/text data
   * Projects -> Tasks -> Notes (assocation)
   * ["project":1](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/taskManagerTasks.json#L8-L9)

* What are the different types of roles?
  * We have some auth groups:
    * ["name": "admin_g"](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/auth_group_permissions.json#L38)
    * ["name": "project_managers"](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/auth_group_permissions.json#L62-L63)
    * ["name": "team_member"](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/auth_group_permissions.json#L80-L81)
* User roles 
    * ["is_superuser": true,](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L14-L15)
    * `is_staff`
    * Looks like users are assigned to groups: ["groups": [](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L37-L40)




* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language - Rails/Ruby, Django/Python, mux/Golang

Python3
Django 3.1.5
asgiref==3.3.1
> ASGI is a standard for Python asynchronous web apps and servers to communicate with each other

screen==1.0.1 (Console/Screen/Terminal width and so on) - barely used, tons written in C - risk
xlwt==1.3.0 (further potential for CSV injection)
sqlparse

* 3rd party components, Examples:
  

* Datastore - Postgresql, MySQL, Memcache, Redis, Mongodb, etc.
  - MySQL (we use sqlparse to access):
> sqlparse is a non-validating SQL parser for Python. It provides support for parsing, splitting and formatting SQL statements.



  

## Brainstorming / Risks

* Potential for CSV extension
  * [django-excel-base==1.0.4](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/requirements.txt#L4-L6)
  * xlwt==1.3.0
* sqlparse and we should think about any sql injection vulns there
* screen is old, unused, c code (62%)
* Noticed in the notes section the user is a string value
  * ["user":"admin",](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/taskManagerNotes.json#L40-L41)
* Looks like Date of birth is captured by the application (PII)
  - ["dob"  : "00/00/00"](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/usersProfiles.json#L8-L9)
* Looks to be some file upload ON the filesystem ["image" : "/static/taskManager/img/bot.png",](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/usersProfiles.json#L6-L7)
  * Is filename user controllable
* 

## Checklist of things to review

- [ ] Looks like perhaps we're using md5 for passwords ["password": "md5$c77N8n6nJPb1$3b35343aac5e46740f6e673521aa53dc",](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/fixtures/users.json#L12-L13)
- [ ] * Note to self: username and email both exist, check if both can be used.

### Risks

- [ ] MySQL Admin running as root, let's verify that doesn't happen beyond local dev

### Authentication

- [ ] What are the different authentication flows?
  - [ ] User Login
  - [ ] User Registration
  - [ ] Forgot Password
- [ ] How are users identified? What information do they have to provide?
  - [ ] Username, email, password, 2fa token, etc.
- [ ] Does the application implement strong password policies?

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
    - [ ] Check fails if token/hmac/nonce/etc. is missing or mismatched
    - [ ] Failure if timestamp is missing or expired
    - [ ] Failure if signature verification fails


### Authorization

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

#### Content Injection

- [ ] `|safe`
- [ ] autoescape off 
  * Because auto-escaping is turned off in the base template, it will also be turned off in the child template
- [ ] data|default (unless data is interpolated into the string literal ... we should be fine)

#### SQL Injection

- [ ] .raw
- [ ] execute
- [ ] callproc (this is for stored procedures)

#### Command Injection

- [ ] subprocess.call()
- [ ] os.system()

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

### High priority

/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
/taskManager/login/	taskManager.views.login	taskManager:login
/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password

- [ ] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
  * Login_required is the only authz mechanism
  * Might have some log injection due to lack of validation [logger.info('User %s upload %s' % (request.user.username,project_id))](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L172-L173)
  * Content type is user controllable [content_type = response.headers["Content-Type"]](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L185)
  * Server side request forgery (SSRF) - [url = request.POST.get('url', False)](https://github.com/redpointsec/vtm/blob/f9f02443446e2b455cc3f3fd8eccd2308cdc56cd/taskManager/views.py#L182-L184)
  * 

/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/ping/	taskManager.views.ping	taskManager:ping
/taskManager/search/	taskManager.views.search	taskManager:search

### Medium Priority

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
/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users

### Low priority

/	taskManager.views.index	index	login_required
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

** Details availabe here https://docs.djangoproject.com/en/4.2/topics/auth/default/

- [ ] @login_required
  * Checks if you're authenticated
- [ ] [@csrf_exempt](https://docs.djangoproject.com/en/4.2/ref/csrf/#django.views.decorators.csrf.csrf_exempt)
- [ ] can_create_project

## Mapping / Files

- [ ] /path/to/some/important/file.sh
