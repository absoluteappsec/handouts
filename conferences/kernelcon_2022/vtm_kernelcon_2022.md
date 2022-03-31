We assessed commit `#d055f45e6fd189ab578fe4fe9d96f317f2fbfe34`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

  * Task manager - manages tasks?
  * ~So far we know it holds Tasks - tasks have notes.~
  * Relationship appears to be Projects > Tasks > Notes
  * Allows both email and username - something to consider

* Who does it do this for? (internal / external customer base)
  * Both Internal / External [because of this](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L96)

* What kind of information will it hold?
  * [Date of Birth](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/usersProfiles.json#L17-L18)
  * File upload
  * Contents of tasks/notes - could be sensitive (project management)

* What are the different types of roles?
  * `admin`, `project_manager`, `team_member`
    * [Permissions appear to be numeric and occur for these roles](https://github.com/sethlaw/vtm/blob/09433b6d12b65522a7b29c9309f125dcc10e7496/taskManager/fixtures/auth_group_permissions.json#L45-L62)
  * also appears to have staff / superuser roles
* What aspects concern your client/customer/staff the most?
  * Content of the projects / scheduling?
  * DoB
  * File Uploads
  * XSS?

## Tech Stack

* Framework & Language
  * Python 3
  * Django 3.1.5
* 3rd party components
  * asgiref - Async comms
  * screen - terminal/screen width?
  * sqlparse - Potential SQLi issues?
  * xlwt - Creates MS 95/2003 compatible content
* Datastore
  * MySQL


## Brainstorming / Risks

* Excel / CSV - Injection?
* SQL Parsing, Potential SQLi issues?
* Developer lacks confidence
* I see some image related content... [confirmed file upload/download issues?](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/usersProfiles.json#L15)
* DoB - Date of birth?
* Saw some payloads that had XSS as seed data - is this a testing _thing_?
* Noticed [MD5 in the Seed file](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L12)
* No real testing of authorization - we should be possibly concerned about authz
* Appears to be using user defined filenames - might be some issues there
* Noticed log entries about:
    * logging fixes
    * ping template fix / some ping restrictions..
      * System / OS Injection?
    * uploads and date fixes
    * login xss fix
    * denying rm
    * add ternary statement to not expose aws api keys in a ssrf
    * adding union sqli
    * disable csrf protections - 000d496f1acaa96c3467aecd23b4524e5f2a8c76
    * one more xss
      * Doesn't appear to have any CSP in code - would need to look at live prod site to ensure this is accurate
  *  user_passes_test - if done improperly appears to allow anon users to access
  * Have only seen RBAC style decorators applied in a few places - we may have a substantial authz problem
  * Due to user enum & 2fa not existing as an option - this is a fairly high risk for ATO application
  * Any place that a user can set details of their anon session can be an issue as we may have session fixation using the login function. 
    > "Note that any data set during the anonymous session is retained in the session after a user logs in"
* Python 3 - need to verify any edge case or weirdness in Regex work 

    

## Checklist of things to review

### Risks

- [ ] XSS stuff: `|safe`, `autoescape off`, `data|`
- [ ] Look for ATO methods
- [ ] Verify 3.1.5 Django isn't vuln (or is)
- [ ] os, subprocess

### Authentication

* Authentication function checks

- [ ] Password hashing mechanism
 * Possibly MD5
- [ ] Timing attacks
  * login function does a lot when there is a user, not so much when there isn't
- [ ] Forgot Password
- [x] 2 factor auth
  * Doesn't exist
- [x] Enumeration... if it matters
  * 100% at the login - several ways
- [ ] Signup
- [x] Brute force attacks
  * We don't know yet we saw no explicit (though possibly implicit thru Django's built-in functions) where we are preventing brute force / rate limiting in any way.
- [ ] Session Management Issues
- [ ] Session Fixation
    * redirect, auth_login, authenticate - NEED TO INVESTIGATE
    * login (auth_login) = sets ID of user on *existing* session, authenticate - verifies credentials and existence
    * Verify later that the source of login uses cycle_key() to prevent this vuln / dynamically validate
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
  - [x] Unit-tests for:
    * TWO WHOLE UNIT TESTS


### Authorization
- [ ] Uses @login_required decorator, is it applied on all endpoints appropriately?

### Auditing/Logging
- [ ] Logging configuration is in `settings.py`, check documentation for secure settings

### Injection
- [ ] ORM `where` function allows for string concatenation, search for all instances

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

### High priority

/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password

/taskManager/login/	taskManager.views.login	taskManager:login
  * Just a weird thing - we have this [immutable declaration](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L428-L429)
  * Noticed logging, let's check info level and that it will be logged in prod
  * Logging an [entire user object](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L434)
  * Possible enumeration
  * User-controllable values logged
  * authenticate, auth_login (THIS IS ACTUALLY LOGIN) - what do these do? They are django built
  * Session fixation
  * [Redirect appears to use user-supplied input](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L439) as part of the URL (side note: research what redirect does)
  * [Commented out CSRF](https://github.com/sethlaw/vtm/blob/568cc898bbfb11c024f6fe378a3b39353db3ff93/taskManager/templates/taskManager/login.html#L21)
  * [Possible DOM Injection](https://github.com/sethlaw/vtm/blob/568cc898bbfb11c024f6fe378a3b39353db3ff93/taskManager/templates/taskManager/login.html#L37-L46)
  * None of the included html files appeared to have XSS

/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
/taskManager/ping/	taskManager.views.ping	taskManager:ping
  * [csrf exempt](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L859)
  * [regex bits here](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L865)
  * [Command Injection](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L868) - CONFIRMED
  * [XSS](https://github.com/sethlaw/vtm/blob/9a4f9d2e2318d8684f22d86fe34f77c79e2105c3/taskManager/templates/taskManager/base_backend.html#L56)
/taskManager/search/	taskManager.views.search	taskManager:search
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users

### Medium Priority

**ACCESS CONTROL**

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
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

### Low priority

/ taskManager.views.index	index	login_required

## Mapping / Authorization Decorators

- [ ] @login_required
  * Built-in convenience function from Django
  * Not authz - more so... are you logged in?
- [ ] @csrf_exempt
  * This is frightening
- [ ] @user_passes_test
  * (lambda u: u.is_superuser)
  * [can_create_project](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L344-L346)
  * [can_edit_project](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L347-L349)
  * [can_delete_project](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L350-L352)

## Mapping / Files

- [ ] settings.py
  * Seems like an important config file
