We assessed commit `#e1b245b78a0b8b36361f988a4a065a4ac5524f18`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
  - Task manager app
  - Contains Projects, Tasks, Notes and multiple users can be assigned to a Project
* Who does it do this for? (internal / external customer base)
 - Based off seeing both employee and regular user emails, we're going to assume they co-mingle their actual work with other organization and user's work data.
* What kind of information will it hold?
  - SSNs
  - DOBs (no validation)
  - File uploads
* What are the different types of roles?
 - [admin_g](https://github.com/redpointsec/vtm/blob/09433b6d12b65522a7b29c9309f125dcc10e7496/taskManager/fixtures/auth_group_permissions.json#L38), team_members, project_managers
 - [is_staff](https://github.com/redpointsec/vtm/commit/09433b6d12b65522a7b29c9309f125dcc10e7496), is_superuser
 - There is a concept of individual `user_permissions` and `groups` that you belong to
* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  - Python 3
  - Django 3.2.21
* 3rd party components, Examples:
  - django-health-check (need to look at config)
  - xlwt
  - psutil
* Datastore
  - MySQL(?)


## Brainstorming / Risks

* Concerned about the healthcheck bits
* Concerned about csv injection
* MD5 seems to be used for password hashing
* is_active (is this some sort of disabling feature?)
* So far, authz schema seems complex and worth digging into for any potential gaps
* Project and Chris share the same password (test123)
* Staff has a `@tm.com` email address, does that mean we can sign up using that email address and are granted access.
* Validation may be a problem, it seems you can use invalid birthdates according to the seed data.
* File uploads - seem to go to a local path on the filesystem. need to vet. (Some users seem to have their images under a team folder, others under just `/img`)
* SSN/DOB data is sensitive data that needs proper crypto and auditing checks applied.
* There is what appears to maybe be a public `/uploads` folder? Dig in on all the usual - can we get to files we shouldn't, can we upload a remote shell, etc.

## Checklist of things to review

### Risks
- [ ] Look for instances of `| safe` in the template/views
- [ ] Look for OS commands
- [ ] Look at the ORM for instances of `createNativeQuery()`
- [ ] Developer expected `x` but I think we should try to see if `y` is possible

### Authentication
- [ ] [Default creds?](https://github.com/redpointsec/vtm/commit/5444f21852c6376433e5c94dab4a40b95ca8cc04)

### Authorization
- [ ] Learn about `django.contrib.auth.models`

### Auditing/Logging
- [ ] Investigate Logger.info

### Injection
#### System
- [ ] `os.system()`
- [ ] `subprocess`
- [ ] `os.popen()`

#### Content

- [ ] `|safe`
- [ ] `mark_safe`
- [ ] `SafeString`

#### SQL
- [ ] `raw()`
- [ ] `execute()`
- [ ] Use of `transaction`
- [ ] Use of `RawSQL`

### Cryptography
- [ ] Validate proper transit of SSN/DOB
- [ ] Validate proper storage at rest of these values

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

### High Priority

- [ ] /taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
  * Logger.info? What is that, how is defined, where is it defined?
  * Appears to be some authz flaw - only a login is required, and you can download other user's profile pics? OR - this is intentional
  * Is this user controlled? [filepath = user.userprofile.image](https://github.com/redpointsec/vtm/commit/09433b6d12b65522a7b29c9309f125dcc10e7496)
  * it appears, you don't even need to hit this endpoint, you can navigate directly to the profile image link if you know it - [CONFIRMED VULNERABLE](https://github.com/redpointsec/vtm/commit/09433b6d12b65522a7b29c9309f125dcc10e7496)

- [ ] /ht/ health_check.views.MainView	health_check:health_check_home
  * The Health Check code potentially takes a kwargs (arbitrary keywords) and then renders a template file (potentially) so we need to validate this.

/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
/taskManager/login/	taskManager.views.login	taskManager:login
/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users
/taskManager/ping/	taskManager.views.ping	taskManager:ping

### Med Priority

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
/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
/taskManager/search/	taskManager.views.search	taskManager:search

### Low Priority

/taskManager.views.index	index	login_required
/taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img

## Mapping / Authorization Decorators

- [ ] `@login_required`
- [ ] `@user_passes_test`: Checks that the user passes a specified test (a function that returns True or False) before granting access to the view. It is used with custom test functions like `can_create_project`, `can_edit_project`, and `can_delete_project` to check for specific permissions.
- [ ] `@csrf_exempt`: Disables CSRF protection for a particular view, which is a security consideration rather than an authorization control. However, it's included in your list because it affects how requests are authenticated and protected against Cross Site Request Forgery attacks.

## Mapping / Files

- [ ] vtm/taskManager/misc.py
  * Saw some dangerous system commands and file handling, seems like an important one.
- [ ] vtm/taskManager/settings.py
  * Appears to have some seriously security-impacting configuration options
