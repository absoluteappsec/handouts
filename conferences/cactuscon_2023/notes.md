We assessed commit `#f56127a5cc820dfb1ea7ab0b99bd28b2d4d54146`

# Notes for you/your team

## Behavior

* What does it do? (business purpose)

  - Help desk support ticketing system 
  > Faveo Helpdesk provides Businesses with an automated Helpdesk system to manage customer support.

* Who does it do this for? (internal / external customer base)

  - Ticketing system - presumably at least 2 roles



* What kind of information will it hold?


* What are the different types of roles?

  - Admin / Guest / Agent / User
    - [CheckRoles](https://github.com/ladybirdweb/faveo-helpdesk/blob/f56127a5cc820dfb1ea7ab0b99bd28b2d4d54146/app/Http/Middleware/CheckRole.php#L24-L25)
  - Teams -> Departments -> Group
 
* What aspects concern your client/customer/staff the most?

## Tech Stack

* Framework & Language
  - PHP Version: 7.1+
  - Laravel (5.6)


* 3rd party components, Examples:
  
- Authentication strategy [built-in from Laravel](https://laravel.com/api/5.8/Illuminate/Contracts/Auth.html)
- [CSRF Tokens](https://github.com/ladybirdweb/faveo-helpdesk/blob/f56127a5cc820dfb1ea7ab0b99bd28b2d4d54146/app/Http/Middleware/VerifyCsrfToken.php#L8)

* Datastore 
- MySQL 5.0+
- Redis

## Brainstorming / Risks

* Account lockout mechanism - should check it out
  * [Security Event](https://github.com/ladybirdweb/faveo-helpdesk/blob/f56127a5cc820dfb1ea7ab0b99bd28b2d4d54146/database/seeds/DatabaseSeeder.php#L1976-L1977)
* File handling - because this doesn't just upload to Azure's blob storage or S3... there are likely options for exploiting the filesystem (LFI/RFI/Traversal/Template Injection). 

From their [documentation](https://github.com/ladybirdweb/faveo-helpdesk/wiki/Faveo-File-Storage)

> Faveo Provides two kind of file storage

> - File system
> - Database

File system is further divided in two kind of storage

Private - To store ticket attachments
Public - To store KB files such as images used in KB

* Lack of unit-tests may mean less focus on authorization issues, etc.

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
