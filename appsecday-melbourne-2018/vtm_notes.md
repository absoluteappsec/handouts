We assessed commit `#ef868eb57fd695377191a8bd17a5a52edfe10d54`

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

Task manager

* Who does it do this for? (internal / external customer base)

Looks to be both external/internal

* What kind of information will it hold?

Notes (potentially sensitive)

Projects -> Tasks -> Notes

* What are the different types of roles?

Superuser, staff, user - separate permissions for roles
There are groups - is this some sort of RBAC/Association

* What aspects concern your client/customer/staff the most?


## Tech Stack

* Framework & Language - Python3/Pip3, MySql, Django framework
* 3rd party libs? - Django extensions, (CSS/JS)
* Datastore?

## Brainstorming / Risks

* MD5 for passwords? Wtf, yo?
* ~Noticed that staff (the role) all have `@tm.com` - what happens if I signup with that address~ Yes there is
* No validation of first/last name
* Version of Django is not locked... is this bad?
* Noticed upload folder, are there routes to upload files? **<~ You can add files to projects**
* what permission schema to do CRUD ops on tasks
* Who can add team members?
* Based on the fact that data is rendered from one user to multiple users - XSS could be a serious concern (Reflected/Stored could have a huge impact)
  * Speaking of cookies - do we have a CSP? Do we have cookie protections like HttpOnly
* Doesn't require a current password to update the old password ** Report but look at CSRF protections?**
* Account edit shows that you can upload a file
* Noticed that we show user account ID in the URL during profile update/edit
* Noticed a search function - SQLi?


## Checklist of things to review based on Brainstorming and Tech Stack

- [x] Look for a signup function
  - [ ] User enum
  - [ ] `@tm.com` what happens if I sign up with that schema
- [ ] Profile pics - does this mean upload?
- [ ] Look for where external JavaScript is included
- [ ] Look at our vendored JS for outdated (retire.js?)
- [ ] File upload handler for profile and notes
- [ ] IDOR for profile updates
- [ ] Look at CSRF protections - especially at the update password function
- [ ] Settings for password hashing and cookie settings
- [ ] CSP?
- [ ] Validation at the model layer for username/lastname and whatever else might make sense
- [ ] SQLi - search function, anywhere else
- [ ] Authz
- [ ] Authn
- [ ] Auditing
- [ ] Crypto (MD5 passwords falls under that)
- [ ] Inection
  - [ ] Look for `raw`, `execute`, `extra`
  - [ ] Look for XSS - `| safe`, `autoescape off`
  - [ ] Command Injection: `os`, `subprocess`

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
- [ ] `POST /taskManager/login/`	taskManager.views.login	taskManager:login
  * takes `username` and `password`
  * potential timing enumeration, password isn't check if user doesn't exist (387/388).
  * passes user/pass to django auth (authenticate)
  * success returns to taskmanager/dashboard
  * No brute force, disabled users still return interesting data on inactive
  * failed_login vs. invalid_username ***
  * login.html
    * FINDING *** User Enumeration, different messages on invalid user vs. invalid password ***

- [ ] `/taskManager/logout/`	taskManager.views.logout_view	taskManager:logout
- [ ] `/taskManager/manage_groups/`	taskManager.views.manage_groups	taskManager:manage_groups
- [ ] `/taskManager/manage_projects/`	taskManager.views.manage_projects	taskManager:manage_projects
- [ ] `POST /taskManager/ping/`	taskManager.views.ping	taskManager:ping
  * Completely unauth'd access available
  * CSRF-able using `csrf_exempt`
  * Command Injection potentially using `subprocess` **CONFIRMED**
- [ ] `/taskManager/profile/`	taskManager.views.profile	taskManager:profile
- [ ] `/taskManager/profile/<user_id>`	taskManager.views.profile_by_id	taskManager:profile_by_id
- [ ] `/taskManager/profile_view/<user_id>`	taskManager.views.profile_view	taskManager:profile_view
- [ ] `/taskManager/reset_password/`	taskManager.views.reset_password	taskManager:reset_password
- [x] `/taskManager/search/`	taskManager.views.search	taskManager:search
  * Requires authn `@login_required`
  * `q` param is the query
  * Project list gets echoed back out as well as the task list
  * Definitely XSS using `safe` on line 14 of `taskManager/templates/taskManager/search.html`
  * HREFs controlled by users?
- [ ] `/taskManager/settings/`	taskManager.views.tm_settings	taskManager:settings
- [x] `/taskManager/view_all_users/`	taskManager.views.view_all_users	taskManager:view_all_users
  * Requires authentication `@login_required`
  * User has to be a `superuser`
  * This thing has people's DOB
  **Likely XSS In the `taskManager/base_backend.html` file on Line 56**
