We assessed commit `#fff`

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

Task Manager

* Who does it do this for? (internal / external customer base)

If anyone can signup, then its external

* What kind of information will it hold?

* What are the different types of roles?

  * Super user
  * Staff
  * User



* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  * 
* 3rd party components, Examples:
  * Billing libraries (rubygem, npm, jar, etc.)
  * JavaScript widgets - (marketing tracking, sales chat widget)
  * Reliant upon other applications - such as receiving webhook events
* Datastore
  * 


## Brainstorming / Risks

* Tasks / Notes - probably important to keep secret
  * Tasks/notes from within the company that develops it
* PII - is it a concern to be stored/transmitted/etc?
* We know that people have profile images, are they uploading that? File uploads a concern.
  * Is Tavis gonna get me again
* Predictable user ids and task ids, etc.
* The permission array has several numeric groups... could there be a collision
* Validation of Date of Birth
* XSS and SQLi - in the Django Framework
* Command Injection

## Checklist of things to review based on Brainstorming and Tech Stack


## Mapping / Routes

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
/taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
/taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
/taskManager/dashboard/	taskManager.views.dashboard	taskManager:dashboard
/taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
/taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
/taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
/taskManager/login/	taskManager.views.login	taskManager:login
/taskManager/logout/	taskManager.views.logout_view	taskManager:logout
/taskManager/manage_groups/	taskManager.views.manage_groups	taskManager:manage_groups
/taskManager/manage_projects/	taskManager.views.manage_projects	taskManager:manage_projects
/taskManager/ping/	taskManager.views.ping	taskManager:ping
/taskManager/profile/	taskManager.views.profile	taskManager:profile
/taskManager/profile/<user_id>	taskManager.views.profile_by_id	taskManager:profile_by_id
/taskManager/profile_view/<user_id>	taskManager.views.profile_view	taskManager:profile_view
/taskManager/project_create/	taskManager.views.project_create	taskManager:project_create
/taskManager/project_list/	taskManager.views.project_list	taskManager:project_list
/taskManager/register/	taskManager.views.register	taskManager:register
/taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
/taskManager/search/	taskManager.views.search	taskManager:search
/taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
/taskManager/task_list/	taskManager.views.task_list	taskManager:task_list
/taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users



## Mapping / Files

- [ ] /fixtures
- [ ] taskManager/settings.py
- [ ] misc.py
