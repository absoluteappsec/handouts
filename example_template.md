We assessed commit `#abcd134`

# Findings

## 1. SQL Injection

### Description

Describe some stuff.

### Recommendation

Recommend some stuff.

## 2. Insecure Direct Object Reference (IDOR)

### Description

Describe some stuff.

### Recommendation

Recommend some stuff.

---

# Notes for you/your team

## Behavior

* What does it do? (business purpose)
* Who does it do this for? (internal / external customer base)
* What kind of information will it hold?
* What are the different types of roles?
* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language - Rails/Ruby, Django/Python, mux/Golang
* 3rd party components, Examples:
  * Billing libraries (rubygem, npm, jar, etc.)
  * JavaScript widgets - (marketing tracking, sales chat widget)
  * Reliant upon other applications - such as receiving webhook events
* Datastore - Postgresql, MySQL, Memcache, Redis, Mongodb, etc.


## Brainstorming / Risks

* Here is what the feature or product is supposed to do... what might go wrong?
* Okay - based on the tech stack, I've realized that the:
  * ORM - Does SQLi in _this_ way
  * Template language introduces XSS in _this_ way

## Checklist of things to review 

### Risks
- [ ] Look for instances of `| safe` in the template/views
- [ ] Look for OS commands
- [ ] Look at the ORM for instances of `createNativeQuery()`
- [ ] Developer expected `x` but I think we should try to see if `y` is possible

### Authentication
- [ ] Login page give error messages, check for enumeration
- [ ] Signup page allows for freeform passwords, does it implement proper password complexity?

### Authorization
- [ ] Uses @login_required decorator, is it applied on all endpoints appropriately?

### Auditing/Logging
- [ ] Logging configuration is in `settings.py`, check documentation for secure settings

### Injection
- [ ] ORM `where` function allows for string concatenation, search for all instances

### Cryptography
- [ ] References to base64 when handling passwords, is this bad?

### Configuration
- [ ] Code is ruby/rails, make sure and run brakeman before closing out

## Mapping / Routes

- [ ] `GET /lulz LulzController.java`
- [ ] `POST /admin/rofl AdminRoflController.java`

## Mapping / Authorization Decorators

- [ ] `ensure_logged_in`

## Mapping / Files

- [ ] /path/to/some/important/file.sh
