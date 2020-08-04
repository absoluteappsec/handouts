


---

# Notes for you/your team

We assessed commit `#155526c8a4c35bc15716157837d02c9566b0941e`

## Behavior

* What does it do? (business purpose)

LMS - Online way to teach/take courses?

* Who does it do this for? (internal / external customer base)

Outside the org (External)

* What kind of information will it hold?

Hold: Files, Written content, Messaging? (messages within the system), Grade/Test Results, PII

* What are the different types of roles?
  * Administrator
  * Instructors
  * Users

```
Privileges:

Backups
Categories
Courses
Enrollment
External Tools
Forums
GameMe
Gradebook
HelpMe
Languages
Learner Tools
Modules
News Feeds
Patcher
Themes
Users
```

* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  * PHP Version 5.2.0+
  * TEMPLATING: Savant2

* 3rd party components, Examples:
  * Apache 1.3/2.0
  * Zlib
  * Curl (optional)
  * Allow the use of CAPTCHA - GD (Graphics Draw)
  * What are they using for OAuth? - Themselves (custom not using a lib)
    * Also calls out to Google

* Datastore
  * MySQL -  4.1.10
    * Standard MYSQL PHP library... basically without a prepared statement it looks pretty raw/vulnerable
    * Interesting documentation here: `documentation/developer/database.gif`

* CURRENT RUNNING VERSION DETAILS:

```
ATutor Version:
2.2.4
PHP Version:
5.6.36-1+ubuntu16.04.1+deb.sury.org+1
MySQL Version:
5.7.31-0ubuntu0.16.04.1
OS:
Linux 4.13.0-43-generic
```


## Brainstorming / Risks

* Allows for custom themes... can I upload my own CSS/JS?
* Check these configs and what they do, seems dangerous - include/config.php:

```
safe_mode = Off
upload_max_filesize >= 2 MB
post_max_size >= 8 MB
sessions
Sessions support must be enabled in PHP.
session.auto_start = 0
session.auto_start must be disabled in PHP.
session.save_path
session.save_path must be set to a real path that can store session data.
. in include_path
```

* Check these configs and what they do, seems dangerous - php.ini:

```
display_errors          = Off
arg_separator.input     = ";&"
register_globals        = Off
magic_quotes_gpc        = Off
magic_quotes_runtime    = Off
allow_url_fopen         = On
allow_url_include       = Off
register_argc_argv      = Off
zlib.output_compression = On
session.use_trans_sid   = 0
```
* Tons of system options in the system preferences - check those out
* Looks like OAuth is configurable? `mods/_standard/basiclti/tool/admin_create.php`
* Profile/badge image uploads (think about RCE)
* You can upload patches to the server - `mods/_standard/patcher/patch_create.php`
  * AND YOU CAN WRITE SQL LOLOMGWTF

* SQL Injection (very possible)
* SSTI - Server Side Template Injection?
* Role based priv esc (because its customizable) - verifying those authz functions
* MFLAC - previous CVEs
* Remote Code Execution - patch uploads, for example
* Unauthorized Grade modification
* Bypassing tests to complete courses?
* Can we bypass GD/CAPTCHA (client-side controls? remember me?)
* CSRF specifically to get an instructor or admin to do something you would like such as approving/grading a test
* Accessing test answers/keys
* OAuth
  * state parameter validation?
  * callback URI validation?
  * Entropy of state, keys, access codes, etc.
  * Are they allowing OAuth v1?
* See if you could lock out the professor so that you can skip that test and go to the movies with your friends
* SHA1 factory appears to be hashing (they call it encryption) the passwords submitted to the app client-side using `sha-1factory.js`.
* Are they creating custom CSRF checks? If so, validate that - not using the session token

## Checklist of things to review

### Risks

- [ ] Theme checks - look for ways to introduce vulnerable code
- [ ] System preferences - look for abuse cases
- [ ] SHA1 Factory usage - analyze and look for abuse cases (look to see about how the secret key is made / salt)
  - [ ] Looks as though you can [set your own CSRF token]()
- [ ] Look at how CSRF protection has been built/designed/implemented
    *  Looks like we have the ability to set our own CSRF token 
- [ ] OAuth
  * state parameter validation?
  * callback URI validation?
  * Entropy of state, keys, access codes, etc.
  * Are they allowing OAuth v1?
- [ ] Uploads:
  - [ ] Profile
  - [ ] Badge
  - [ ] File
- [ ] Business Logic Flaws
  - [ ] Is it possible to lock out the professor?
  - [ ] Is it possible to skip the test?


### Authentication

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


### Authorization

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


### Auditing/Logging
- [ ] If an exception occurs, does the application fails securely?
- [ ] Do error messages reveal sensitive application or unnecessary execution details?
- [ ] Are Component, framework, and system errors displayed to end user?
- [ ] Does exception handling that occurs during security sensitive processes release resources safely and roll back any transactions?
- [ ] Are relevant user details and system actions logged?
- [ ] Is sensitive user input flagged, identified, protected, and not written to the logs?
  * Credit Card #s, Social Security Numbers, Passwords, PII, keys

### Injection
- [ ] ORM `where` function allows for string concatenation, search for all instances

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

- [x] `./mods/_core/users/admin_delete.php`
  * admin_authenticate() let's investigate
  * ton of SQL - we need to verify whether or not there is SQLi
  * `write_to_log` - look into this log writing function (AT_ADMIN_LOG_UPDATE being passed)
  * `html_get_list` <~ could I be able to inject some content? [here](https://github.com/atutor/ATutor/blob/155526c8a4c35bc15716157837d02c9566b0941e/mods/_core/users/admin_delete.php#L175-L176)


```
- [ ] ./mods/_core/users/admins/index.php
- [ ]  ./mods/_core/users/admins/create.php
- [ ] ./mods/_core/users/admins/reset_log.php
- [ ] ./mods/_core/users/admins/password.php
- [ ] ./mods/_core/users/admins/detail_log.php
- [ ] ./mods/_core/users/admins/delete.php
- [ ] ./mods/_core/users/admins/log.php
- [ ]  ./mods/_core/users/admins/edit.php
- [ ]  ./mods/_core/users/admins/my_edit.php
- [ ]  ./mods/_core/users/admins/my_password.php
- [ ]  ./mods/_core/users/admin_email.php
- [ ] ./mods/_core/users/admin_deny.php
```


## Mapping / Authorization Decorators

- [ ] `admin_authenticate()`
- [ ] `check_csrf_token()`

## Mapping / Files

* In the brainstorming section we listed out some possibly dangerous config options for the files below.

- [ ] include/config.inc.php
- [ ] include/vitals.inc.php
  * [$savant = Savant2()](https://github.com/atutor/ATutor/blob/155526c8a4c35bc15716157837d02c9566b0941e/include/vitals.inc.php#L253-L254)
- [ ] footer.inc.php
- [ ] header.inc.php
- [ ] securimage/securimage.php
- [ ] include/login_functions.inc.php
