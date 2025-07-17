Perfect — here’s your **enhanced and copy-paste-friendly checklist** in full, preserving your structure and markdown formatting while expanding coverage in each section.

---

# ✅ Enhanced Generic Security Checklist

## 🔐 Authorization

### Identification & Design

* [ ] Identify all user roles and associated permissions
* [ ] Identify sensitive/privileged endpoints
* [ ] Identify authz expectations specific to the business purpose of the app

  * Can non-privileged users view, add, or alter accounts?
  * Is there functionality to add accounts with higher access levels than their own?
  * How is separation of duties handled?
* [ ] Review role boundaries for least privilege
* [ ] Identify high-risk role transitions (e.g., elevating user → admin)
* [ ] Identify Authorization functions/filters

  * Do they take tokens? cookies? headers? Are they framework-native or custom-built?

### Authorization Vulnerabilities

* Broken Access Control

  * [ ] Insecure Direct Object Reference (`find_by`, `find`, `findOne`, `findAll`, etc)
  * [ ] Missing Function-Level Access Control
  * [ ] Verify Authorization Filters are used consistently and early in execution

* Generic AuthZ Flaws

  * [ ] Sensitive Data Exposure (access without authorization)
  * [ ] Mass Assignment (unrestricted fields on models)
  * [ ] Business Logic Flaws (e.g., trust boundary violations)
  * [ ] CSRF Protections applied correctly
  * [ ] Re-authentication enforced for critical operations

    * e.g., password change, account deletion

* Advanced Considerations

  * [ ] Race conditions in access control logic (TOCTOU issues)
  * [ ] Are authorization checks contextual (time-based, IP-based, scope-based)?
  * [ ] Fine-grained object- or field-level access control (especially for APIs)

---

## 🔑 Authentication

### Auth Flow Review

* [ ] Enumerate authentication flows:

  * [ ] User Login
  * [ ] User Registration
  * [ ] Forgot Password / Reset
  * [ ] Magic Link / SSO / OAuth / SAML
  * [ ] Device or biometric authentication
* [ ] Identify required credentials for login (username, email, password, 2FA token, etc)
* [ ] Strong password policy in place?
* [ ] CAPTCHA or anti-bot control in signup/login flows?

### Authentication Function Checks

* [ ] Secure password hashing (e.g., bcrypt, scrypt, Argon2 — NOT MD5/SHA1)
* [ ] Secure comparisons (constant-time equality checks)
* [ ] Timing attack mitigation in credential comparisons
* [ ] Forgot password implementation:

  * [ ] Tokens time-limited and one-time-use
  * [ ] Tokens stored securely (hashed if persistent)
* [ ] Brute force protection (rate limiting, lockouts)
* [ ] Account enumeration prevention (generic error messages)
* [ ] 2FA enforcement and configuration
* [ ] Session Management:

  * [ ] Session Fixation prevented
  * [ ] Secure session destruction on logout
  * [ ] Session timeouts reasonable
  * [ ] HttpOnly, Secure, and SameSite cookie flags

### Service-to-Service Authentication

* [ ] Uses HMAC or JWT with secure algorithms (no SHA1/MD5)
* [ ] Communication occurs over verified TLS

  * [ ] TLS verification not disabled
* [ ] Tokens have reasonable TTL (e.g., ≤1 hour)
* [ ] Handles clock skew safely
* [ ] Secrets stored in a vault, not code
* [ ] Unit tests:

  * [ ] Fail on missing/malformed HMAC/tokens
  * [ ] Fail on expired timestamps
  * [ ] Fail on invalid signature

---

## 🧾 Auditing

* [ ] Application fails securely on exception?
* [ ] No sensitive information in user-facing errors
* [ ] Component/system stack traces not exposed
* [ ] Exceptions during secure flows safely rollback
* [ ] Security-relevant events logged:

  * [ ] Auth events (login, failed login, password reset, etc)
  * [ ] Access denied/unauthorized attempts
  * [ ] Data modification actions
* [ ] Logs are:

  * [ ] Tamper-resistant
  * [ ] Rotated regularly
  * [ ] Reviewed or aggregated for analysis
* [ ] Sensitive input masked in logs:

  * [ ] Passwords, tokens, SSNs, PII, API keys
* [ ] Inputs validated/sanitized before logging (log injection defense)
* [ ] Logging configuration is environment-specific (not hardcoded)

---

## 💉 Injection

### Input Validation

* [ ] All input is validated (no exceptions)
* [ ] Positive validation (known-good patterns)
* [ ] Data typed and coerced (integer, date, etc)
* [ ] Consistent client + server-side validation
* [ ] Regular expressions used safely:

  * [ ] Whitelist preferred
  * [ ] No blind spots or regex bypasses
* [ ] Input length bounded
* [ ] Separation between input and:

  * [ ] Code execution (SQL, OS commands)
  * [ ] Client-side JS (XSS)
* [ ] HTTP headers validated (User-Agent, Referer, etc)

### Output Encoding

* [ ] Use parameterized queries (ORM, prepared statements)
* [ ] ORM: avoid `.raw`, `eval()`, or direct query construction
* [ ] Output properly encoded for context:

  * [ ] HTML, JS, URL, CSS, headers
* [ ] Libraries used for encoding:

  * [ ] Are they maintained/patched?
  * [ ] Are they context-aware?
* [ ] Avoid using regex for output encoding

### Specific Injection Types

* [ ] SQL Injection
* [ ] NoSQL Injection
* [ ] Command Injection
* [ ] LDAP Injection
* [ ] SSTI (Server-Side Template Injection)
* [ ] XSS: Reflected, Stored, DOM-based
* [ ] Header injection (CRLF)
* [ ] Accept-list / Deny-list protections reviewed

---

## 🔐 Cryptographic Review

* [ ] Approved crypto libraries used (e.g., libsodium, BouncyCastle)
* [ ] Encryption standards meet industry recommendations:

  * [ ] No MD5/SHA1
  * [ ] ≥256-bit key length
  * [ ] No RC4 or SSLv2/v3
* [ ] Certificates ≥2048-bit RSA or ECDSA equivalents
* [ ] Secrets/keys not hardcoded or in source control
* [ ] Secure key storage (vault, HSM, KMS)
* [ ] Key rotation policies documented and enforced
* [ ] Secrets in transit encrypted (TLS, HTTPS)
* [ ] Data at rest encrypted where needed (PII, tokens)

---

## ⚙️ Configuration Review

* [ ] Review all application/framework configuration files
* [ ] Debug/verbose logging disabled in production
* [ ] Feature flags / beta features gated securely
* [ ] Security headers implemented:

  * [ ] Content-Security-Policy
  * [ ] X-Content-Type-Options
  * [ ] X-Frame-Options / CSP frame-ancestors
  * [ ] Referrer-Policy
  * [ ] Strict-Transport-Security
* [ ] Framework protections enabled:

  * [ ] CSRF
  * [ ] Secure cookies
  * [ ] Input sanitization

---

## 📁 File Handling (If Applicable)

* [ ] File uploads stored outside web root?
* [ ] Upload restrictions enforced:

  * [ ] File type whitelist
  * [ ] Size limits
  * [ ] MIME validation
* [ ] AV or malware scanning performed
* [ ] User-supplied filenames not trusted
* [ ] Uploads cannot overwrite existing files
* [ ] Upload access controlled (download requires auth)
* [ ] No path traversal (e.g., `../../`)
* [ ] No Remote File Inclusion (RFI)
* [ ] Temporary files cleaned up securely

---

Let me know if you'd like this output tailored for a **spreadsheet**, **internal GitHub checklist**, **PR audit tool**, or **automated scanner integration**.
