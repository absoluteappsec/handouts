# Notes for you/your team

We assessed commit `#d055f45e6fd189ab578fe4fe9d96f317f2fbfe34`

## Behavior

* What does it do? (business purpose)

 Task manager
 It appears that multiple users can be assigned to at least one project
 

* Who does it do this for? (internal / external customer base)
  * Internal and External


* What kind of information will it hold?
  * Projects, Notes, Tasks - Images?, Text, Title
  * Projects -> Tasks -> Notes
  * Sensitive data:
    * DoB

* What are the different types of roles?
  * admin, team member, project managers
  * superuser, staff

* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
 * Django 3.1.5 - Python 3

* 3rd party components, Examples:
  * [django-six](https://github.com/sethlaw/vtm/blob/e68a5b590ed4cbfab2e9c93b6618b9736a05dbe2/requirements.txt#L7-L8)
  * Template lang - ['BACKEND': 'django.template.backends.django.DjangoTemplates',](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L128-L129)

* Datastore
  * MySQL


## Brainstorming / Risks

* [missing user_permissions](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L6-L7)
* What if user_permissions can override group permissions
* [is_active](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L30-L31) - this is a possible authn mechanism that could be important - let's look into how its used and any ways to bypass
* Uses both email and username for authn possibly, let's check
* Profile image being stored - Possible File handling weaknesses
* Primary key and User id attributes are expected it seems to mirror one another though that might not always be the case and could potentially impact authorization. Let's check
* Lack of unit tests especially authz based tests indicate significant security gaps
* Password complexity
* Routing uses regex, let's see about any issues or nuanced problems that may arise




## Checklist of things to review

### Risks

- [ ] Tasks, Projects, Notes all take text and title so check those for content injection style issues at a min


### Authentication
- [ ] Login page give error messages, check for enumeration
- [ ] Signup page allows for freeform passwords, does it implement proper password complexity?
* **FINDING** -> [Uses md5](https://github.com/sethlaw/vtm/blob/298fbbec58a256d5c26278bb4234496360fbf99b/taskManager/fixtures/users.json#L12-L13)

### Authorization
- [ ] Uses @login_required decorator, is it applied on all endpoints appropriately?

### Auditing/Logging
- [ ] Logging configuration is in `settings.py`, check documentation for secure settings

### Injection
- [ ] Templates: `|safe`
- [ ] Injection `raw` `execute`
- [ ] System `call` `system` `import os` `subprocess`

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

### High priority

/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
/taskManager/login/	taskManager.views.login	taskManager:login
/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
- [ ] /taskManager/ping/	taskManager.views.ping	taskManager:ping
  * Takes only POST requests, does not have CSRF exempt
  * No login required - can be access unauth'd
  * Obvious exploitable command injection
  * [XSS](https://github.com/sethlaw/vtm/blob/9a4f9d2e2318d8684f22d86fe34f77c79e2105c3/taskManager/templates/taskManager/base_backend.html#L56-L57)

/taskManager/view_img/	taskManager.views.view_img	taskManager:view_img
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password

### Medium priority

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

### Low priority

/taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/search/	taskManager.views.search	taskManager:search
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users


## Mapping / Authorization Decorators

- [ ] [@login_required](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L410-L411)
- [ ] [@user_passes_test(can_delete_project)](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L411-L412)
- [ ] [def can_create_project(user):](https://github.com/sethlaw/vtm/blob/d055f45e6fd189ab578fe4fe9d96f317f2fbfe34/taskManager/views.py#L344-L352)


## Mapping / Files

- [ ] settings.py
  * secret key in source
  * ALLOWED_HOSTS [is `*`](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L19-L20)
  * Logging config https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L21-L22
  * Static root = [30 day retention](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L117-L118)
  * [CSRF Middleware missing](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L75-L76)
  * [File handling](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L84-L85)
  * What is message [storage used for?](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L84-L85)
  * [MESSAGE_STORAGE](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L112)
  * Empty DB password
  * [SESSION_SERIALIZER](https://github.com/sethlaw/vtm/blob/2821241809e22207d2dd6eed540265ce3afc7c21/taskManager/settings.py#L156) is using Pickle (RCE!!!)
