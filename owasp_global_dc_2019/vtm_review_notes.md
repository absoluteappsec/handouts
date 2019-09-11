# Notes for you/your team

We assessed commit `#74e64e1ccb617c83ba1db4cbbb24a33051e169f8`

## Behavior

* What does it do? (business purpose)

Task Manager Application

* Who does it do this for?
 (internal / external customer base)

 Internal and external

* What kind of information will it hold?

* Projects and tasks and notes
  * The info held within can be anything so it could be sensitive PII, security centric

* What are the different types of roles?

Staff, Superuser, regular user

* What aspects concern your client/customer/staff the most?

* User separation (someone being able to see data from another user)
* File handling
* Exfiltration - creds, personal data, project data, company secrets/IP, source code
* Attacking another staff member


## Tech Stack

* Framework & Language Django 2.2.5 / Python version 3

* 3rd party components, Examples:
Django Extensions
MySQL Client - Nothing obvious from a security perspective, looks well supported

* Datastore - MySQL


## Brainstorming / Risks

* MD5 used for passwords?
* Looks like if staff is using their own product, and we have authz issues, we might be able to find out sensitive info about the company or the app.
* Stored XSS could mean a whole more due to staff using this tool.
* File uploads... this could be scary
* We stored PII (DoB, Full name, and email)
* Password change function looks insecure (missing current password check) - profile updates, forgot password, login
  * CSRF on the password change function.
* Reflecting back user data but specifically the username (XSS concern)
* Download profile pic numerically, is that possibly an issue?
* Are user profile identifiers a sequentially incrementing numeric value? (ie - easy to guess... 1,2,3 etc.)
* Debug appears to be set to true - sensitive data exposure (` you have DEBUG = True in your Django settings file`)
* Uploaded files can be accessed, LFI/RCE/etc?
* Search functionality - possible XSS, SQLi, and SDE.
* Chained exploit thought - what if you can use XSS + CSRF to change an admin's password - what does that give you?


## Checklist of things to review based on Brainstorming and Tech Stack

- [ ] Look for instances of `| safe` & `autoescape off` in the template/views
- [ ] What does having admin permissions give you?
- [ ] SQL Injection `raw` `execute` `extra`
- [ ] `os.system`, `subprocess`, `popen`
- [ ] CSRF protections (especially password change)
- [ ] Password hashing - md5?
- [ ] View file upload/download functionality
- [x] Review authz decorator
  * `@login_required`
  * `@user_passes_test(can_create/edit/delete_project)`
  * `@csrf_exempt`
- [ ] Auditing:
  * Who downloaded files and uploaded files
  * Logging project, task, note CRUD operations
- [ ] Review the view all users for any authz issues

## Mapping / Routes




- [x] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
  * Looked at authz, looks like projects are scoped to the user thru `request.user.id` :thumbsup:
  * Appears [we have command injection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/misc.py#L22-L29) thru the title of the file
  * No file size or type verification
  * File injection (overwriting files)
  * Appears [to be SQLi](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L171-L174)
  * Doesn't appear to have any auditing/logging (who uploaded what)

- [x] /taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
  * [Vulnerable to CSRF](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L779)
  * Missing re-authorization/credentialing (don't have to enter current creds to change them)
  * base_backend calls in external JS
  * Could not find an easy way to exploit this but we have [XSS](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/templates/taskManager/base_backend.html#L56-L57s). It appears signup doesn't really allow us to use these dangerous chars and also be able to login.


- [ ] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
- [ ] /taskManager/downloadprofilepic/<user_id>/	taskManager.views.download_profile_pic	taskManager:download_profile_pic
- [ ] /taskManager/search/	taskManager.views.search	taskManager:search

- [ ] /taskManager/view_all_users/	taskManager.views.view_all_users	taskManager:view_all_users
  * Looked at the authz function and it does require superuser access to view all users.

- [x] /taskManager/ping/	taskManager.views.ping	taskManager:ping
  * [Possible command Injection](https://github.com/sethlaw/vtm/blob/74e64e1ccb617c83ba1db4cbbb24a33051e169f8/taskManager/views.py#L813-L814) - CONFIRMED
  * No obvious XSS
  * Missing Authorization (so any anonymous user can interact with this endpoint)

## Mapping / Files

- [ ] /fixtures
- [ ] taskManager/settings.py
- [ ] misc.py
