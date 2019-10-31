We assessed commit `#74e64e1ccb617c83ba1db4cbbb24a33051e169f8`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
  * Task Manager

* Who does it do this for? (internal / external customer base)
  * Internal / External users (we think)

* What kind of information will it hold?
  Project details, tasks, notes, files
  * PII such as date of birthdate, full name, email address

* What are the different types of roles?
  * Admin, Team Member, Project Manager
  * Users have is_staff and is_superuser options attached to their profile
  * We think that team members in the same group can edit the same items (projects?)

* What aspects concern your client/customer/staff the most?
  * Sensitive data exposure of projects/notes/tasks
    * If the internal TM team is using this product, they could be storing sensitive data about the actual product

* IDOR in Projects, profile views, and any weird logic issues with being able to add people's profiles and then view their details.

## Tech Stack

* Framework & Language
  * Python3/Pip3
  * django 2.1.1
* 3rd party components, Examples:

* Datastore
  * MySQL


## Brainstorming / Risks

* Passwords appear to be MD5 hashed... look into this
* Can a user belong to multiple groups and how is access control enforced, concerns?
* Notes have usernames and not PKs for the association
  * Authz issues w/ this? (create a checklist item)
* Verify that if we can escalate or have an ACL issue, that we audit correctly and don't misidentify the malicious actor
* Username, Email address, and primary key are likely used to identify the user
* File uploads - test for various vulns like size limitations, overriding files, downloading other people's files or source code, etc.
  * Not only is the file potentially an issue but the name... can we overwrite, or enter XSS, etc.
  * File upload in two places - one is to attach files to a task and the other is to upload a profile pic
  * Ask folks if its an issue to see other people's profile pics (especially the actual TM employee's pics)

* XSS and SQL Injection issues when creating or modifying tasks, notes, projects

* Doesn't ask for the old password when changing the password
  Concerns: Privilege Escalation and CSRF
* Search function:
  * Injection issues or overly broad search results


## Checklist of things to review based on Brainstorming and Tech Stack

- [ ] OS Command Injection: system, subprocess, import os/subprocess
- [ ] XSS: |safe, autoescape off
- [ ] SQL Injection: execute, raw
- [ ] Privilege Escalation/IDOR: Profiles, Projects, Tasks
- [ ] CSRF protection (especially the change password)
- [ ] Review File Upload
- [ ] Serialization (Pickle?)


## Mapping / Routes

- [x] /taskManager/<project_id>/upload/	taskManager.views.upload
  * saw import os in the views.py file, let's go back to this (double back)
  * The only authz decorator is just requiring that someone is logged in
  * [Command injection here](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/misc.py#L22-L29)
  * No ACL on the upload folder
  * No input validation on the file name
  * Possible directory traversal/overwriting
  * [SQL Injection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L171-L174)
  * We need to vendor in this code
  * [XSS](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/templates/taskManager/base_backend.html#L56-L57)
- [ ] /taskManager/change_password/ taskManager.views.change_password
- [ ] /taskManager/register/ taskManager.views.register
- [ ] /taskManager/search/ taskManager.views.search

## Mapping / Authorization Decorators

- [ ] @login_required
  * If the user isn't logged in, redirects to login_url in settings.py, otherwise proceed!
- [ ] @user_passes_test(can_create_project, can_edit_project, can_delete_project)
  * Has perm documention https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.has_perm
   * Permission page: https://docs.djangoproject.com/en/2.2/topics/auth/default/#topic-authorization
  * Boolean based on whether a User object has permissions
  * Note that user_passes_test() does not automatically check that the User is not anonymous.
- [ ] @user_passes_test(lambda u: u.is_superuser)
- [ ] @csrf_exempt
  * This makes a function unsafe (doesn't have CSRF protections applied)

## Mapping / Files

- [ ] taskManager/settings.py
