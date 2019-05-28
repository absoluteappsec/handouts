We assessed commit `#ef868eb57fd695377191a8bd17a5a52edfe10d54`

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

Task manager

* Who does it do this for? (internal / external customer base)

Internal & External

* What kind of information will it hold?

  * Information about users
  * Tasks that might contain sensitive data - new features being released
  * Recon of the company makeup
  * Consider notes, tasks, projects to be sensitive in nature
  * It has file uploads, so... a concern

* What are the different types of roles?

  * Admins, Project managers, team members

  * Admins can add people to projects and change their permission level
  * Project managers can change attributes of a project
  * Team members can add notes and do basic editing of a project


* What aspects concern your client/customer/staff the most?

  * File handling of uploads
    * Malware
    * Size of the file
    * Parsing of these files (like xml bomb)
  * Sensitive data being exposed meaning the actual projects, tasks, and notes (IDOR).
  * Business logic in terms of messing with a competitor
  * Multi-tenant app means that all the same data is in the database - SQLi would be devastating
  * Auditing properly


## Tech Stack

* Framework & Language
  * Python 3
  * Django 2.1.5
* 3rd party components, Examples:
  * ORM - mysqlclient
* Datastore
  * MySQL


## Brainstorming / Risks

* Concerned that IDOR would lead to the exposure of information on vulnerabilities in this platform
* Reminder: look up any known security issues with mysqlclient
* Looking for:
  * SQLi - raw, extra, execute (anything else makes sense) - type coercion To prevent this, perform the correct typecasting before using the value in a query.
  * XSS:
    * User input that is not escaped and put into an html tag's attribute
    * mark_safe, safe, is_safe, autoescape off
  * Command Injection:
    * import os, subprocess
 * Concerned about boundaries / data being stored from multiple tenants
 * Priv esc leading to being able to view projects, elevate privs, etc.
 * Auditing events - CRUD on projects, tasks, etc.
 * Check validation of password strength



## Checklist of things to review based on Brainstorming and Tech Stack

- [ ] raw, extra, execute
- [ ] mark_safe, safe, is_safe, autoescape off
- [ ] import os, subprocess
- [ ] IDOR
- [ ] Forceful browsing
- [ ] CRUD auditing of projects
- [ ] Authentication - password hashing, validation routine, brute forcing, forgot password/reset
- [ ] Configuration review


## Mapping / Routes

- [x] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
  * Login required dec
  * Possible SQLi
  * Maybe IDOR?
  * Potentially open redirection
  * `store_uploaded_file` - path traversal, command injection, forceful browsing
  * Potential DoS from resource exhaustion (file size)

- [x] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
  * mimetypes.guess_type
  * Make sure you can't download any off the file system (this is because of that vulnerable store_uploaded_file function)
  * IDOR did not appear to be an issue.

- [x] /taskManager/forgot_password/	taskManager.views.forgot_password	taskManager:forgot_password
  * exempt from csrf (but unauth'd so should be good)
  * `raw` is dangerous - SQLi on line 748
  * enumeration (possibly a concern?)
  * os.urandom + custom token generation logic

- [x] /taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password
  * CSRF exempt but okay because its unauth'd (potentially ok)
  * Brute forcing of six character reset token possible
  * If brute-forced, then you'd be able to set someone else's password (not sure which user)
  * Verify the duration of the tokens

- [x] /taskManager/search/	taskManager.views.search	taskManager:search
  * Login decorator (only checks that we're signed in)
  * XSS thru the q parameter - [`|safe`](https://github.com/sethlaw/vtm/blob/ef868eb57fd695377191a8bd17a5a52edfe10d54/taskManager/templates/taskManager/search.html#L14-L15) is called
   * [`base_backend.html`](https://github.com/sethlaw/vtm/blob/ef868eb57fd695377191a8bd17a5a52edfe10d54/taskManager/templates/taskManager/base_backend.html#L56-L57) contains self-xss

- [x] /taskManager/settings/	taskManager.views.tm_settings	taskManager:settings
  * XSS with the HTTP header values [on this line of settings.html](https://github.com/sethlaw/vtm/blob/ef868eb57fd695377191a8bd17a5a52edfe10d54/taskManager/templates/taskManager/settings.html#L28-L29)
  * Sensitive data exposure?


## Mapping / Files

- [x] /fixtures
- [x] taskManager/settings.py
- [x] misc.py
