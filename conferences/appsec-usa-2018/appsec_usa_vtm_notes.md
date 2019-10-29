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

Task Manager application

* Who does it do this for? (internal / external customer base)

~Internal~ Nope, turns out external

* What kind of information will it hold?

Tasks/Notes for projects
File uploads - anything associated with the project

* What are the different types of roles?

It looks to have groups
We definitely have an admin and staff role - priv escalation?

* What aspects concern your client/customer/staff the most?

View notes of other projects
File uploads... that's scary

## Tech Stack

* Framework & Language - Django, MySQL, Python3

- Template XSS - `|safe`, `mark_safe()`,`autoescape off`
- SQL Injection - `extra()`, `RawQuery`, `raw`
- Admin auth might be `django.contrib`? (library tech stack)


## Brainstorming / Risks

  * Hey, saw `is_staff` as part of the user model... mass assignment?
  * Hey - there are at least admins - `is_superuser`
  * Could we upload malware? (a/v scanning)
  * what size of the files
  * Filetypes restricted? Is there a way that we can?
  * Where do the files go? Do we need to be concerned with protections or can we offload to AWS?
  * Hey I saw a search function - could that be vuln
  * LFI / RFI
  * What if the company is using their own product to track security issues or otherwise sensitive data in this product that external users can access - (tenancy, isolation, etc.)
  * Check to see what ping is doing?
  * all_users - is this right?
  * Settings endpoint exists, what does it do?
  * happy admin in settings.py


## Checklist of things to review based on Brainstorming and Tech Stack

- [ ] Check file uploads
- [ ] Check authorization functions (user, staff, admin)
- [ ] IDOR
- [ ] MFLAC
- [ ] Check authN
- [ ] Check for Todo, Changeme, Fixme, Debug
- [ ] Analyze Ping
- [ ] Check for serialization flaws
- [ ] Check SMTP for DoS Risk
- [ ] Is @login_required applied appropriately?
- [ ] Are custom permissions applied properly?
- [ ] Auditing/Logging
- [ ] Input Validation
- [ ] Output Encoding
- [ ] Crypto
- [ ] Configuration


## Mapping / Routes

- [ ] `GET /` - `views.py` - 456
  * Is there some authz issue w/ this? `@login_required`
- [ ] `GET /taskManager/<project_id>/<task_id>/` - 	taskManager.views.task_details	taskManager:task_details
- [x] `/taskManager/<project_id>/project_details/`	taskManager.views.project_details	taskManager:project_details
- [ ] `/taskManager/<project_id>/task_complete/<task_id>`	taskManager.views.task_complete	taskManager:task_complete
- [ ] `/taskManager/<project_id>/task_create/`	taskManager.views.task_create	taskManager:task_create
- [ ] `/taskManager/<project_id>/task_delete/<task_id>`	taskManager.views.task_delete	taskManager:task_delete
- [ ] `/taskManager/<project_id>/task_edit/<task_id>`	taskManager.views.task_edit	taskManager:task_edit
- [ ] `/taskManager/<project_id>/upload/`	taskManager.views.upload	taskManager:upload
  * File Upload here!
- [ ] `/taskManager/change_password/`	taskManager.views.change_password	taskManager:change_password
- [ ] `/taskManager/dashboard/`	taskManager.views.dashboard	taskManager:dashboard
- [ ] `/taskManager/forgot_password/`	taskManager.views.forgot_password	taskManager:forgot_password
  * AuthN Function
- [ ] `/taskManager/login/`	taskManager.views.login	taskManager:login
  * AuthN function
- [ ] `/taskManager/logout/`	taskManager.views.logout_view	taskManager:logout
- [ ] `/taskManager/manage_groups/`	taskManager.views.manage_groups	taskManager:manage_groups
- [ ] `/taskManager/manage_projects/`	taskManager.views.manage_projects	taskManager:manage_projects
- [ ] `POST /taskManager/ping/`	taskManager.views.ping	taskManager:ping
  * takes an `ip` parameter
  * string concat to cmd
  * exec to subprocess!!!!
  * Command Injection
  * CSRF Exempt
  * No login_required * Access Control Findings
  * DEBUG components available
- [ ] `/taskManager/profile/`	taskManager.views.profile	taskManager:profile
- [ ] `/taskManager/profile/<user_id>`	taskManager.views.profile_by_id	taskManager:profile_by_id
- [ ] `/taskManager/profile_view/<user_id>`	taskManager.views.profile_view	taskManager:profile_view
- [ ] `/taskManager/reset_password/`	taskManager.views.reset_password	taskManager:reset_password
- [ ] `/taskManager/search/`	taskManager.views.search	taskManager:search
- [ ] `/taskManager/settings/`	taskManager.views.tm_settings	taskManager:settings
- [ ] `/taskManager/view_all_users/`	taskManager.views.view_all_users	taskManager:view_all_users
