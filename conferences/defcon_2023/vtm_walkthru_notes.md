We assessed commit `#c1e3089001aff82cbdbd21a87323562e9cf9f4dc`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
  - Task manager
  - Projects have Tasks, Tasks have notes. Projects have multiple users assigned.

* Who does it do this for? (internal / external customer base)
  - External & Internal

* What kind of information will it hold?
  - Files
  - Dates of birth

* What are the different types of roles?
  - There are at least 3 groups, admin_g, project_managers, team_member


* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  - Python 3
  - Django 3.1.5


* 3rd party components, Examples:
  * xlwt

* Datastore
  - MySQL


## Brainstorming / Risks

* Noticed they're using XLWT library to produce CSV... CSV Injection?
* Hey this screen library is not popular, hasn't been maintained, probably something to look at.
* Look out for places where default user Dade is used
* [Image column for notes](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/fixtures/taskManagerNotes.json#L6-L7) may indicate file upload/download
* Potenital for MD5 in use: ["password": "md5$c77N8n6nJPb1$3b35343aac5e46740f6e673521aa53dc",](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/fixtures/users.json#L12-L13)
* there are many ways to authorize or handle permissions - is_staff, is_superuser, user permissions assigned, group permissions assigned, and then group permissions enabled on Projects AND what users are assigned to those projects
* Confirmed - it appears there are file uploads or at least a way to upload files for your profile pic AND it **uses the local filesystem to store**
* Date of Birth is stored - can we access
* ALMOST complete lack of unit tests [class UserTestCase(TestCase):](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/tests.py#L10-L17)
* If login_required is missing then the user_passes_test function will not validate that the user is logged-in: https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.decorators.user_passes_test

## Checklist of things to review

- [ ] Django 3.1.5 is considered insecure according to the django docs site, we need to figure out why.


### Risks
- [ ] Look for instances of `| safe` in the template/views
- [ ] Look for OS commands
- [ ] Look at the ORM for instances of `createNativeQuery()`
- [ ] Developer expected `x` but I think we should try to see if `y` is possible

### Authentication

- [ ] What are the different authentication flows?
  - [x] User Login
  - [ ] User Registration
  - [ ] Forgot Password

- [ ] How are users identified? What information do they have to provide?
  - [ ] Username
     User supplied and chosen - not an email
- [ ] Password 
 - [x] **FINDING** Hashing is MD5 [PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/settings.py#L144-L145)


  - **FINDING** No 2fa/MFA

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

* Missing CSRF middleware [#'django.middleware.csrf.CsrfViewMiddleware',](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/settings.py#L75-L76)


### Auditing/Logging


### Injection


### Cryptography


### Configuration


## Mapping / Routes

### High

/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password

/taskManager/login/	taskManager.views.login	taskManager:login
  - Noticed that the `logger.info` function is passed a user object that could have sensitive values in it.[logger.info(user)](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/views.py#L434-L435)
  - Not sure how we're keeping user-supplied content safe when logging it [logger.info('Disabled Account (%s:%s)' % (username,password))](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/views.py#L441-L442)
  - During the login trace it appears we may have user enum [<h3>Login failed. Please try again</h3>](https://github.com/redpointsec/vtm/blob/c1e3089001aff82cbdbd21a87323562e9cf9f4dc/taskManager/templates/taskManager/login.html#L8-L9) - Looks like potenital enumeration

/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
/taskManager/ping/	taskManager.views.ping	taskManager:ping
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
  * **POSSIBLE VULN** Has a CSRF exempt note on it and accepts POST requests
/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

### Medium

/taskManager.views.index	index	login_required
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

### Low

/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/search/	taskManager.views.search	taskManager:search
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users


## Mapping / Authorization Decorators

- [ ] @login_required
- [ ] @user_passes_test
 - can_create_project
 - can_edit_project
 - can_delete_project
- [ ] @csrf_exempt 

## Mapping / Files

- [ ] taskManager/settings.py
