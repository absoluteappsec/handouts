# ✅ **Practical Secure Code Review Checklist (2025 Edition)**

## 🔐 Authorization

### Identification & Design

* [ ] Enumerate roles and their permissions
* [ ] Identify privilege boundaries and transitions (e.g., user → admin)
* [ ] Map sensitive/privileged endpoints to role access
* [ ] Identify high-impact business logic operations (e.g., fund transfers, ownership changes)
* [ ] Ensure admin-only endpoints aren’t exposed to lower roles
* [ ] Verify authorization rules are contextual (e.g., tenant ID or resource ownership enforced)

### Implementation Checks

* [ ] Authz enforced **in all layers** (API, GraphQL resolvers, service layers)
* [ ] Check for **auth bypass** via:

  * [ ] Frontend hidden UI elements but no backend check
  * [ ] GraphQL/resolvers with no auth middleware
  * [ ] Mobile or alternative client interfaces
* [ ] Inconsistent use of `req.user`, `current_user`, `session[:user_id]` across endpoints
* [ ] Dangerous default scopes (e.g., `.all` or `.first` without ownership filtering)

### Common Authorization Vulnerabilities

* [ ] Insecure Direct Object Reference (IDOR)
* [ ] Missing function-level access control
* [ ] Elevation of privilege due to insufficient access filters
* [ ] Access control enforced via client input (e.g., role passed in request)

---

## 🔑 Authentication

### Flows & Coverage

* [ ] Identify all entry points:

  * [ ] Web UI login
  * [ ] API tokens
  * [ ] Mobile tokens
  * [ ] SSO / OAuth2 flows
* [ ] Verify token binding (e.g., is JWT tied to IP/device?)
* [ ] Compare code-based flows vs. password-based flows
* [ ] Validate social login + password login don’t cause duplicate user accounts
* [ ] Re-auth required for high-risk changes (email, password, MFA)

### Common Flaws

* [ ] Password reset logic:

  * [ ] Token cannot be reused
  * [ ] Tokens expire reasonably (15–60 min)
* [ ] `find_user_by_email` logic avoids leaking timing or existence
* [ ] Multiple identity providers properly scoped (e.g., don’t mix Google and internal authz)
* [ ] Passwords stored with modern hash + salt (bcrypt, scrypt, Argon2)
* [ ] Login throttling enabled

### Session & Token Handling

* [ ] Secure flags set: `HttpOnly`, `Secure`, `SameSite=Strict/Lax`
* [ ] JWT tokens:

  * [ ] Signed with strong secret or asymmetric key
  * [ ] Expiry enforced server-side (not just `exp` claim)
  * [ ] Revocation support if needed

---

## 🧾 Auditing & Logging

* [ ] Log sensitive operations (role change, password update, token generation)
* [ ] Avoid logging sensitive content (passwords, keys, SSNs)
* [ ] Ensure log entries contain:

  * [ ] `user_id` or subject identifier
  * [ ] `action` taken
  * [ ] `resource` affected
  * [ ] `timestamp`
* [ ] Avoid log injection via newline/control characters
* [ ] Separate logs by severity: info, warning, error, security
* [ ] Exception handling paths log failures securely

---

## 💉 Injection & Input Handling

### Input Validation

* [ ] Validate on both client and server
* [ ] Prefer allow-list (known good) patterns
* [ ] Input sanitized before DB/OS calls
* [ ] Dangerous keywords (e.g., `DROP`, `UNION`, `--`) blocked or neutralized
* [ ] Control characters (e.g., null byte, carriage return) stripped

### Injection-Specific Checks

* [ ] SQL injection: check raw SQL fragments, dynamic `where`, `.execute`, or `.raw` calls
* [ ] NoSQL injection (e.g., MongoDB): untrusted values used in query shape
* [ ] GraphQL injection: no validation on user-constructed queries
* [ ] Template injection: unescaped values rendered in server-side templates (Jinja, Twig, etc.)
* [ ] Dangerous joins (e.g., `+ req.param` or `${userInput}` in SQL paths)

### ORM Misuse (based on slides)

* [ ] Use of raw query building (`.raw`, `.query()`, `Sequelize.literal()`)
* [ ] No input embedded into `JOIN` clauses or `WHERE` fragments dynamically
* [ ] Unsafe default scopes (e.g., returning full record set)

---

## 🔐 Cryptographic Practices

* [ ] All cryptographic operations use well-reviewed libraries
* [ ] No homegrown token or encryption schemes
* [ ] Secrets rotated and not hardcoded in source
* [ ] TLS enforced with strong cipher suites
* [ ] Symmetric keys stored securely (vault, KMS)

---

## ⚙️ Configuration Security

* [ ] App not running in debug or test mode in production
* [ ] All error reporting routed through secure channels
* [ ] `.env`, `.DS_Store`, `.git` folders blocked from external access
* [ ] Secrets injected via environment, not hardcoded
* [ ] Secure headers:

  * [ ] `Content-Security-Policy`
  * [ ] `X-Content-Type-Options`
  * [ ] `Strict-Transport-Security`
  * [ ] `Referrer-Policy`

---

## 📁 File & Upload Handling

* [ ] Uploaded files stored outside public web root
* [ ] Filetype validated using:

  * [ ] Extension
  * [ ] MIME type
  * [ ] Magic number (content inspection)
* [ ] Uploaded filenames not reused or written directly
* [ ] No dynamic file paths from user input (`fs.readFile(req.query.name)`)
* [ ] Dangerous file operations (based on slides):

  * [ ] `open`, `read`, `write`, `fs.unlink`, `eval`, `execFile`, `os.system`
* [ ] Zip bombs or recursive archive protections
* [ ] Antivirus/scan integration in upload pipeline

---

## 🧠 Business Logic

* [ ] Check assumptions around:

  * [ ] Ownership and tenant boundaries
  * [ ] Maximum allowed changes (e.g., balance edits, privilege changes)
  * [ ] Sequential operations (e.g., pay → confirm → execute)
* [ ] Abuse of bulk/batch APIs (mass actions)
* [ ] Time-based logic that can be manipulated (e.g., `created_at` passed in from user)


Would you like this turned into a downloadable spreadsheet, GitHub checklist format, or JSON schema for automated scanning systems?
