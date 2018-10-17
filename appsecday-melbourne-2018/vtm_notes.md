We assessed commit `#abcd134`

# Findings

## 1.

### Description

Describe some stuff.

### Recommendation

Recommend some stuff.

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
* Who does it do this for? (internal / external customer base)
* What kind of information will it hold?
* What are the different types of roles?
* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
* 3rd party libs?
* Datastore?

## Brainstorming / Risks

## Checklist of things to review based on Brainstorming and Tech Stack

## Mapping / Routes

- [ ] `GET /` - `views.py` - 456
- [ ] `GET /taskManager/<project_id>/<task_id>/` - 	taskManager.views.task_details	taskManager:task_details
- [ ] `/taskManager/<project_id>/project_details/`	taskManager.views.project_details	taskManager:project_details
- [ ] `/taskManager/<project_id>/task_complete/<task_id>`	taskManager.views.task_complete	taskManager:task_complete
- [ ] `/taskManager/<project_id>/task_create/`	taskManager.views.task_create	taskManager:task_create
- [ ] `/taskManager/<project_id>/task_delete/<task_id>`	taskManager.views.task_delete	taskManager:task_delete
- [ ] `/taskManager/<project_id>/task_edit/<task_id>`	taskManager.views.task_edit	taskManager:task_edit
- [ ] `/taskManager/<project_id>/upload/`	taskManager.views.upload	taskManager:upload
- [ ] `/taskManager/change_password/`	taskManager.views.change_password	taskManager:change_password
- [ ] `/taskManager/dashboard/`	taskManager.views.dashboard	taskManager:dashboard
- [ ] `/taskManager/forgot_password/`	taskManager.views.forgot_password	taskManager:forgot_password
- [ ] `/taskManager/login/`	taskManager.views.login	taskManager:login
- [ ] `/taskManager/logout/`	taskManager.views.logout_view	taskManager:logout
- [ ] `/taskManager/manage_groups/`	taskManager.views.manage_groups	taskManager:manage_groups
- [ ] `/taskManager/manage_projects/`	taskManager.views.manage_projects	taskManager:manage_projects
- [ ] `POST /taskManager/ping/`	taskManager.views.ping	taskManager:ping
- [ ] `/taskManager/profile/`	taskManager.views.profile	taskManager:profile
- [ ] `/taskManager/profile/<user_id>`	taskManager.views.profile_by_id	taskManager:profile_by_id
- [ ] `/taskManager/profile_view/<user_id>`	taskManager.views.profile_view	taskManager:profile_view
- [ ] `/taskManager/reset_password/`	taskManager.views.reset_password	taskManager:reset_password
- [ ] `/taskManager/search/`	taskManager.views.search	taskManager:search
- [ ] `/taskManager/settings/`	taskManager.views.tm_settings	taskManager:settings
- [ ] `/taskManager/view_all_users/`	taskManager.views.view_all_users	taskManager:view_all_users
