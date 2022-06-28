# List of generic checks (non-specific)

## Authorization

- [ ] Identify Roles
- [ ] Identify sensitive/privileged endpoints
- [ ] Identify authz expectations specific to the business purpose of the app
  * Can non-privileged users view, add, or alter accounts?
  * Is there functionality to add accounts with higher access levels than their own access?
  * How is separation of duties handled?
- [ ] Identify Authorization functions/filters
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

- [ ] What are the different authentication flows?
  - [ ] User Login
  - [ ] User Registration
  - [ ] Forgot Password
- [ ] How are users identified? What information do they have to provide?
  - [ ] Username, email, password, 2fa token, etc.
- [ ] Does the application implement strong password policies?

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
    - [ ] Check fails if token/hmac/nonce/etc. is missing or mismatched
    - [ ] Failure if timestamp is missing or expired
    - [ ] Failure if signature verification fails

## Auditing

- [ ] If an exception occurs, does the application fails securely?
- [ ] Do error messages reveal sensitive application or unnecessary execution details?
- [ ] Are Component, framework, and system errors displayed to end user?
- [ ] Does exception handling that occurs during security sensitive processes release resources safely and roll back any transactions?
- [ ] Are relevant user details and system actions logged?
- [ ] Is sensitive user input flagged, identified, protected, and not written to the logs?
  - [ ] Credit Card #s, Social Security Numbers, Passwords, PII, keys
- [ ] Are unexpected errors and inputs logged?
  - [ ] Multiple login attempts, invalid logins, unauthorized access attempts
- [ ] Are log details should be specific enough to reconstruct events for audit purposes?
  - [ ] Are logging configuration settings configurable through settings or environment variables and not hard-coded into the source?
- [ ] Is user-controlled data validated and/or sanitized before logging to prevent log injection?

## Injection

### Input Validation
- [ ] Is all input is validated without exception?
- [ ] Do the validation routines check for known good characters and cast to the proper data type (integer, date, etc.)?
- [ ] Is the user data validated on the client or server or both (security should not rely solely on client-side validations that may be bypassed)?
- [ ] If both client-side and server-side data validation is taking place, are these validations consistent and synchronized?
- [ ] Do string input validation use regular expressions?
- [ ] Do these regular expressions use blacklists or whitelists?
- [ ] What bypasses exist within the regular expressions?
- [ ] Does the application validate numeric input by type and reject unexpected input?
- [ ] How does the application evaluate and process input length?
- [ ] Is a strong separation enforced between data and commands (filtering out injection attacks)?
- [ ] Is there separation between data and client-side scripts?
- [ ] Is provided data checked for special characters before being passed to SQL, LDAP, XML, OS and third party services?
- [ ] For web applications, are often forgotten HTTP request components, including HTTP headers (e.g. referrer) validated?

### Output Encoding
- [ ] Do databases interactions use parameterized queries?
- [ ] Do input validation functions properly encode or sanitize data for the output context?
- [ ] How do framework-provided database ORM functions used?
- [ ] Does the source code use potentially-dangerous ORM functions? (.raw, etc)
- [ ] What output encoding libraries are used?
- [ ] Are output encoding libraries up-to-date and patched?
- [ ] Is proper output encoding used for the context of each output location?
- [ ] Are output encoding routines dependent on regular expressions? Are there any weaknesses or blind-spots in these expressions?

### Specific Injection Vulnerabilities
- [ ] SQL / NoSQL Injection
- [ ] NoSQL Injection - Key store manipulation (memcache, redis)
- [ ] Accept-List/Deny-List validation

## Cryptographic Review
- [ ] What are the standard encryption libraries are used for?
  - [ ] Hashing functions - password hashing, cryptographic signing, etc
  - [ ] Encryption functions - data storage, communications
- [ ] Do the strength of implemented ciphers meet industry standards?
  - [ ] Less than 256-bit encryption
  - [ ] MD5/SHA1 for password hashing
- [ ] Any RC4 stream ciphers
  - [ ] Certificates with less than 1024-bit length keys
  - [ ] All SSL protocol versions
- [ ] Are cryptographic private keys, passwords, and secrets properly protected?

## Configuration Review
- [ ] What are the interesting files used to configure the application and components?
- [ ] Are any endpoints enabled through configurations properly protected with authentication and authorization?
- [ ] Are security protections implemented in framework properly configured?
- [ ] Does the target language and framework version have any known security issues?
- [ ] Are configuration-controlled security headers implemented according to recommended best practices?

## File Handling Review (as needed)

- [ ] How are file uploads stored
- [ ] Security controls?
  - [ ] A/V Scanning
  - [ ] Size / Filetype restrictions
- [ ] How are they retrieved (both Access Control but any sort of traversal or LFI/RFI would be interesting)
