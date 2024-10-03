We assessed commit `e1b245b78a0b8b36361f988a4a065a4ac5524f18`

# Notes for you/your team

## Behavior

* Misc
  - Credentials mentioned in the README for logins: "Login with the username `chris` and a password of `test123`"
  - Are notes tied to a specific user? Like, can only one user see it? Or is a group permission and that is more for attribution of WHO created the note?


* What does it do? (business purpose)
  - Task Manager -> Projects -> Tasks -> Notes
    -  Projects can have multiple users assigned

  - Web Application
* Who does it do this for? (internal / external customer base)
  - Appears to be both
* What kind of information will it hold?
  * PII - dob/ssn
* What are the different types of roles?
  - Auth Groups:
    - Admin
    - project managers
    - team members
  - User permissions
    * Actually called `user_permissions`
    * is_staff
    * is_superuser
* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language 

Python - 3
Django - 3.2.21

* 3rd party components, Examples:
- [xlwt / django-excel](https://github.com/redpointsec/vtm/blob/9e3c64c331951c15f63c847be4f08a6811c3ca55/requirements.txt#L10-L11)
- django-health-check
- requests
- sqlparse


* Datastore
 - MySQL or SQLite


## Brainstorming / Risks

* We need to look csv injection due to excel/csv related libraries
* Look for where `requests` are used for SSRF issues
* django-health-check - Just need to look into it
* Using non-validating sqlparse library - look for validation issues. (ie - .format, .split)
* Sensitive data being handled
  - Auditing (storing this dob/ssn style stuff?)
  - Injection that would lead to leakage
  - Priv Esc
* It appears their is a potential for file handling
* I dont' know what [settings.AUTH_USER_MODEL is](https://github.com/redpointsec/vtm/blob/078c92d10285fbb717bb991308a85a302d0009e8/taskManager/migrations/0001_initial.py#L4)
* [MD5 password hashing?](https://github.com/redpointsec/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L12)
* The permission checks for user seem to have different types of access - so it has Group permission, User permissions, and roles: is_staff / is_superuser
* File handling is happening, appears to be local on the filesystem, and that brings in a new set of concerns

## Checklist of things to review

### Risks
- [ ] CSV Injection
- [ ] Path Traversal (upload)

### Authentication
- [ ] Login page give error messages, check for enumeration
- [ ] Signup page allows for freeform passwords, does it implement proper password complexity?

### Authorization
- [ ] Priv Esc or any form of ATO could be fairly terrible given that it appears this platform will host important data from the company that manages/develops/sells the product

### Auditing/Logging
- [ ] Logging configuration is in `settings.py`, check documentation for secure settings

### Injection
- [ ] Look at things like text, title, and any other inputs avaible for Notes/Tasks/Projects to see if they have validation/escaping issues

### Cryptography
- [ ] Ensure that dob/ssn are encrypted

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes



| Checked? | Name                            | URL Pattern                                             | Controller#Action                                     | Extra Info           |
|--------|---------------------------------|---------------------------------------------------------|-------------------------------------------------------|----------------------|
| [ ]    | index                           | `/`                                                     | `taskManager.views.index`                             | `login_required`     |
| [ ]    | health_check:health_check_home  | `/ht/`                                                  | `health_check.views.MainView`                         |                      |
| [ ]    | taskManager:index               | `/taskManager/`                                         | `taskManager.views.index`                             |                      |
| [ ]    | taskManager:task_details        | `/taskManager/<project_id>/<task_id>/`                  | `taskManager.views.task_details`                      |                      |
| [ ]    | taskManager:note_create         | `/taskManager/<project_id>/<task_id>/note_create/`      | `taskManager.views.note_create`                       |                      |
| [ ]    | taskManager:note_delete         | `/taskManager/<project_id>/<task_id>/note_delete/<note_id>` | `taskManager.views.note_delete`                   |                      |
| [ ]    | taskManager:note_edit           | `/taskManager/<project_id>/<task_id>/note_edit/<note_id>`  | `taskManager.views.note_edit`                      |                      |
| [ ]    | taskManager:project_edit        | `/taskManager/<project_id>/edit_project/`               | `taskManager.views.project_edit`                      |                      |
| [ ]    | taskManager:manage_tasks        | `/taskManager/<project_id>/manage_tasks/`               | `taskManager.views.manage_tasks`                      |                      |
| [ ]    | taskManager:project_delete      | `/taskManager/<project_id>/project_delete/`             | `taskManager.views.project_delete`                    |                      |
| [ ]    | taskManager:project_details     | `/taskManager/<project_id>/project_details/`            | `taskManager.views.project_details`                   |                      |
| [ ]    | taskManager:task_complete       | `/taskManager/<project_id>/task_complete/<task_id>`     | `taskManager.views.task_complete`                     |                      |
| [ ]    | taskManager:task_create         | `/taskManager/<project_id>/task_create/`                | `taskManager.views.task_create`                       |                      |
| [ ]    | taskManager:task_delete         | `/taskManager/<project_id>/task_delete/<task_id>`       | `taskManager.views.task_delete`                       |                      |
| [ ]    | taskManager:task_edit           | `/taskManager/<project_id>/task_edit/<task_id>`         | `taskManager.views.task_edit`                         |                      |
| [ ]    | taskManager:upload              | `/taskManager/<project_id>/upload/`                     | `taskManager.views.upload`                            |                      |
            * Doesn't require anything but a valid session authz-wise
            * **TODO** check out logger.info
            * Passes in user-supplied input to the logging mechanism
            *  Interesting comment ## kind of janky, you have to subimt a file and file by url, I wasn't sure how to get the form to validate
            * ` proj = Project.objects.get(pk=project_id)` POtential IDOR
            * Potential SSRF: 
            ```Python
                url = request.POST.get('url', False)
                response = requests.get(url, timeout=15) #making request for image
            ```
            * Is this a mime-type bypass?   `content_type = response.headers["Content-Type"]`
            * **POTENTIALLY VULNERABLE** [store_uploaded_file looks dangerous](https://github.com/redpointsec/vtm/blob/9e36a07c2be338d76205c3ad346e4c35a9cb113a/taskManager/misc.py#L30-L31)
            * **POTENTIALLY VULNERABLE** We take the name parameter, we name the file based off of that, are there any traversal/injection/etc. style vulns associated with it
| [ ]    | taskManager:change_password     | `/taskManager/change_password/`                         | `taskManager.views.change_password`                   |                      |
| [ ]    | taskManager:dashboard           | `/taskManager/dashboard/`                               | `taskManager.views.dashboard`                         |                      |
| [ ]    | taskManager:download            | `/taskManager/download/<file_id>/`                      | `taskManager.views.download`                          |                      |
| [ ]    | taskManager:download_profile_pic| `/taskManager/downloadprofilepic/<user_id>/`            | `taskManager.views.download_profile_pic`              |                      |
| [ ]    | taskManager:forgot_password     | `/taskManager/forgot_password/`                         | `taskManager.views.forgot_password`                   |                      |
| [ ]    | taskManager:login               | `/taskManager/login/`                                   | `taskManager.views.login`                             |                      |
| [ ]    | taskManager:logout              | `/taskManager/logout/`                                  | `taskManager.views.logout_view`                       |                      |
| [ ]    | taskManager:manage_groups       | `/taskManager/manage_groups/`                           | `taskManager.views.manage_groups`                     |                      |
| [ ]    | taskManager:manage_projects     | `/taskManager/manage_projects/`                         | `taskManager.views.manage_projects`                   |                      |
| [ ]    | taskManager:ping                | `/taskManager/ping/`                                    | `taskManager.views.ping`                              |                      |
| [ ]    | taskManager:profile             | `/taskManager/profile/`                                 | `taskManager.views.profile`                           |                      |
| [ ]    | taskManager:profile_by_id       | `/taskManager/profile/<user_id>`                        | `taskManager.views.profile_by_id`                     |                      |
| [ ]    | taskManager:profile_view        | `/taskManager/profile_view/<user_id>`                   | `taskManager.views.profile_view`                      |                      |
| [ ]    | taskManager:project_create      | `/taskManager/project_create/`                          | `taskManager.views.project_create`                    |                      |
| [ ]    | taskManager:project_list        | `/taskManager/project_list/`                            | `taskManager.views.project_list`                      |                      |
| [ ]    | taskManager:register            | `/taskManager/register/`                                | `taskManager.views.register`                          |                      |
| [ ]    | taskManager:reset_password      | `/taskManager/reset_password/`                          | `taskManager.views.reset_password`                    |                      |
| [ ]    | taskManager:search              | `/taskManager/search/`                                  | `taskManager.views.search`                            |                      |
| [ ]    | taskManager:settings            | `/taskManager/settings/`                                | `taskManager.views.tm_settings`                       |                      |
| [ ]    | taskManager:task_list           | `/taskManager/task_list/`                               | `taskManager.views.task_list`                         |                      |
| [ ]    | taskManager:view_all_users      | `/taskManager/view_all_users/`                          | `taskManager.views.view_all_users`                    |                      |
| [ ]    | taskManager:view_img            | `/taskManager/view_img/`                                | `taskManager.views.view_img`                          |                      |

## Mapping / Authorization Decorators

- [ ] @login_required
- [ ] @csrf_exempt
  * **$POTENTIALLY VULNERABLE** This is a vulnerability if its applied to a state changing operation, look for everywhere this might be an issue
- [ ] @user_passes_test(can_delete_project)
- [ ] @user_passes_test(can_edit_project)
- [ ] @user_passes_test(can_create_project)

## Mapping / Files

- [ ] `taskManager/settings.py`
        * There are important security things here!
- [ ] `taskManager/misc.py`


