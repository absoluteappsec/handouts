We assessed commit `#16c83d639021a2357f9323e59a31bdbfa9c8837a`

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

 * Task Manager

* Who does it do this for? (internal / external customer base)
  * Both - looks like we're expecting non TM users https://github.com/sethlaw/vtm/blob/16c83d639021a2357f9323e59a31bdbfa9c8837a/taskManager/fixtures/users.json#L96-L97
* What kind of information will it hold?
  * Projects -> Tasks -> Notes
  * Definitely PII - Birth Dates (with image of person maybe and email and name)
  * [reset token](https://github.com/sethlaw/vtm/blob/16c83d639021a2357f9323e59a31bdbfa9c8837a/taskManager/migrations/0001_initial.py#L37-L38)
* What are the different types of roles?
  * superuser/staff
  * project managers
  * team members
  * admins
* What aspects concern your client/customer/staff the most?
  * Sensitive data access (horizontal/vertical escalation || )

## Tech Stack

* Framework & Language
  * Python 3
  * Django 3.1.5
* 3rd party components, Examples:
  * sqlparse - parses SQL, does it have any security research?
  * pytz - Time zones, wouldn't THINK it'd be vulnerable but let's validate
  * screen - terminal width?
  * requests - Looks like [perhaps SSRF](https://github.com/sethlaw/vtm/blob/16c83d639021a2357f9323e59a31bdbfa9c8837a/taskManager/views.py#L174-L175)
  * S2S Comms? [asgiref](https://github.com/django/asgiref)
  * xwlt
* Datastore
  * MySQL


## Brainstorming / Risks

* Escalation might mean that we are able to see bugs that exist in the app, might mean seeing sensitive PII or corp intellectual property
* App allows File uploads - look for typical issues there: zip bombs, size, malicious content, web shell, access control issues
  * Possible SSRF / LFI || Traversal
* Can we mess with marking other people's projects/tasks/etc complete just to be a jerk
* Doesn't appear that password change requires current password - look into this later
  *  CSRF? Because if you don't have a current password required and can CSRF someone into changing their password... gonna have a bad time
* Django Admin dashboard
* What does sqlparse/requests/asgiref do and can it be vulnerable?
* Django - look for issues with 3.1.5
* profile mgmt - IDOR
* search bar looks like sqli-ectable
* check out system errors
* Is it possible to load too many Tasks/notes/projects
* Uploads folder lives in the publicly accessible (unauth'd) static folder
* I see on_delete called, let's make sure we're clearing out those files correctly
* CSRF Middleware... are we even using? `#'django.middleware.csrf.CsrfViewMiddleware',`
* Why does admin have a static folder? https://github.com/sethlaw/vtm/blob/ - `Directory indexes are not allowed here.` error message at static/admin 16c83d639021a2357f9323e59a31bdbfa9c8837a/taskManager/settings.py#L120-L121
* Pickle serialization being used... can we find the session generating salt/secret

## Checklist of things to review

### Risks

- [ ] SQLi: `.raw`, `.execute`, `.callproc`
- [ ] `|safe`, `autoescape off `,  `data|`
- [ ] `os`, `subprocess`
- [ ] https://www.cvedetails.com/cve/CVE-2021-35042/, https://www.cvedetails.com/cve/CVE-2021-33203/
- [ ] Look for stored secrets to leverage the Pickle weakness
- [ ] look at admin static folder and generally admin functionality
- [ ] verify delete is occurring for user created objects
- [ ] Verify CSRF can be utilized
- [ ] CSRF in change password
- [ ] Verify that the password change functionality is as terrible as we think
- [ ] Check the uploads folder and upload/download functionality for weaknesses
- [ ] Check for DoS conditions by creating too many Tasks, Notes, etc.
- [ ] Validate how system errors/exceptions occur
- [ ] IDOR in Profile management


## Authorization

- [ ] Identify Roles
- [ ] Identify sensitive/privileged endpoints
- [ ] Identify authz expectations specific to the business purpose of the app
  * Can non-privileged users view, add, or alter accounts?
  * Is there functionality to add accounts with higher access levels than their own access?
  * How is separation of duties handled?
- [ ] Identify Authorization functions/filtes
  * Do they take Tokens? Cookies? Custom or handled by a framework?

* Broken Access Control
  - [ ] Insecure Direct Object Reference (`find_by`, `find`, `findOne`, `findAll`, etc)
  - [ ] Missing Function Level Access Control
  - [ ] Verify Authorization Filters

* Generic authz flaws
  - [ ] Sensitive Data Exposure
  - [ ] Mass Assignment
  - [ ] Business Logic Flaws
  - [ ] Are CSRF Protections applied correctly
  - [ ] Are users forced to re-assert their credentials for requests that have critical side-effect (account changes, password reset, etc)?

## Authentication

* Authentication function checks

- [ ] Password hashing mechanism
- [ ] Timing attacks - this could be username/password or HMAC operations verifying keys
- [ ] Forgot Password
- [ ] 2 factor auth
- [ ] Enumeration... if it matters
- [ ] Signup
- [ ] Brute force attacks
- [ ] Session Management Issues
  - [ ] Session Fixation
  - [ ] Session Destruction
  - [ ] Session Length

* Is there service-to-service authentication?
  - [ ] Constant time comparison function used
  - [ ] HMAC generated using a secure algorithm (basically not SHA1/MD5)
  - [ ] Requests occur over SSL/TLS
    - [ ] Verification of SSL/TLS is not turned off
  - [ ] Reasonable TTL implemented (meaning, an hour or less would be normal.)
  - [ ] Accounts for time skew
  - [ ] Shared secret used and stored in vault (not hardcoded)
  - [ ] Unit-tests for:
    * Check fails if token/hmac/nonce/etc. is missing or mismatched
    * Failure if timestamp is missing or expired
    * Failure if signature verification fails

## Auditing

- [ ] If an exception occurs, does the application fails securely?
- [ ] Do error messages reveal sensitive application or unnecessary execution details?
- [ ] Are Component, framework, and system errors displayed to end user?
- [ ] Does exception handling that occurs during security sensitive processes release resources safely and roll back any transactions?
- [ ] Are relevant user details and system actions logged?
- [ ] Is sensitive user input flagged, identified, protected, and not written to the logs?
  * Credit Card #s, Social Security Numbers, Passwords, PII, keys


## Datastore

- [ ] SQL / NoSQL Injection
- [ ] Key store manipulation (memcache, redis)
- [ ] Validations?
- [ ] Typically where cryptographic operations take place such as generate authentication tokens, hashing passwords, etc.

## File handling

- [ ] How are file uploads stored
- [ ] Security controls?
  - [ ] A/V Scanning
  - [ ] Size / Filetype restrictions
- [ ] How are they retrieved (both Access Control but any sort of traversal or LFI/RFI would be interesting)

## Mapping / Routes

### High priority routes

- [ ] /taskManager/change_password/	taskManager.views.change_password	taskManager:change_password
  * Looks like opted out of CSRF protections
  * Includes base html file, [vuln to XSS](https://github.com/sethlaw/vtm/blob/16c83d639021a2357f9323e59a31bdbfa9c8837a/taskManager/templates/taskManager/base_backend.html#L56-L57)
  * Does not require any form of current password or otherwise identifying info

- [ ] /taskManager/forgot_password/	taskManager.views.forgot_password
- [ ] /taskManager/login/	taskManager.views.login	taskManager:login
- [ ] /taskManager/logout/	taskManager.views.logout_view	taskManager:logout
- [ ] /taskManager/register/	taskManager.views.register	taskManager:register
- [ ] /taskManager/reset_password/	taskManager.views.reset_password	taskManager:reset_password

### Medium priority
- [ ] /taskManager/download/<file_id>/	taskManager.views.download	taskManager:download
- [ ] /taskManager/downloadprofilepic/<user_id>/
	taskManager.views.download_profile_pic	taskManager:download_profile_pic
  * Authz == `@login_required`
  * Need to verify how this redirection is occurring because I'm curious if its possible to redirect using the image url

- [ ] /taskManager/<project_id>/upload/	taskManager.views.upload	taskManager:upload
- [ ] /taskManager/ping/	taskManager.views.ping	taskManager:ping


## Mapping / Authorization Decorators

- [ ] `@login_required`
- [ ] `@csrf_exempt`
- [ ] `@user_passes_test`
  * `can_create_project`, can_edit_project, can_delete_project

## Mapping / Files

- [ ] `taskManager/fixtures/users.json` - shows MD5 in the password
- [ ] `settings.py`
- [ ] `taskManager/misc.py`
