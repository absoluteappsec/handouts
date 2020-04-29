Node Appsec Checklist/Braindump
===


:warning: STILL A WIP :warning:


### Easy Wins


#### Security Headers

[`npm install --save helmet`](https://www.npmjs.com/package/helmet)

```javascript
const express = require('express')
const helmet = require('helmet')

const app = express()

app.use(helmet()) // Defaults -> https://github.com/helmetjs/helmet#how-it-works

// We can help w/ CSP
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    styleSrc: ["'self'", 'maxcdn.bootstrapcdn.com']
  }
}))
```

#### Secure defaults - Session Cookie

We have to be explicit about declaring cookies secure as Express doesn't do this by default.

```javascript
const sess = session({
  store,
  secret: process.env.SOME_SECRET,
  resave: false,
  saveUninitialized: true,
  // Set the cookie's security settings
  cookie: { secure: true }
})
```

Re-use of secrets to generate sessions is a common issue. This is insecure and the session secret should be its own value that is not re-used anywhere else in the application.

**BAD**

```javascript
const sess = session({
  store,
  secret: process.env.WEBHOOK_SECRET,
  resave: false,
  saveUninitialized: true
})
```

**GOOD**

```javascript
const sess = session({
  store,
  secret: process.env.UNIQUE_SINGULAR_PURPOSE_SECRET,
  resave: false,
  saveUninitialized: true
})
```

Another good idea is the use of `sameSite` option with a value of `"Lax"` for express 4.x+ applications.

```javascript
const sess = session({
  store,
  secret: process.env.UNIQUE_SINGULAR_PURPOSE_SECRET,
  resave: false,
  saveUninitialized: true,
  cookie: { sameSite: 'Lax' }
})
```

#### CSRF

[`npm install --save csurf`](https://www.npmjs.com/package/csurf)

```javascript
const express = require('express')
const app = express()

const csrf = require('csurf')
const bodyParser = require('body-parser')
app.use(bodyParser.urlencoded({ extended: false }))
const cookieParser = require('cookie-parser')
app.use(cookieParser())
app.use(csrf({ cookie: true }))

app.get('/form', function(req, res) {
  // pass the csrfToken to the view
  res.render('send', { csrfToken: req.csrfToken() })
})

app.post('/process', function(req, res) {
  res.send('data is being processed')
})

```

#### Web Sockets 

Websockets can cause CSRF issues if we do not implement a CSRF-like mitigation because websocket requests do not obey the Same Origin Policy (SOP).

The easiest way to prevent CSRF is to strictly check the `Origin` header against a hardcoded value but implementing a CSRF token approach would also work.

```
  const wss = new WebSocket.Server({
    verifyClient: (info, done) => {
      sess(info.req, {}, () => {
        const expectedOrigin = process.env.APP_URL || 'http://localhost:3000'
        const originHeader = info.req.headers.origin
        if (originHeader !== expectedOrigin) {
          done(false)
        } else {
          done(info.req.session)
        }
      })
    },
    server
  })
```

### Common Anti-Patterns

- Building URLs or HTML with backtick interpolatino
  - `fetch(\`${user_controlled}.somedomain.com/hook`)`
  - `<h1>${username}</h1>`

- Mixing user input and templates
  - User controlled templates -> liquidjs
  - Other languages if user controlled can gain RCE

- Insufficient protections of OAuth dance
  - Not adding state parameter

### Tools/Techniques

#### Vulnerable packages/libs

    npm audit

#### Mass-Assignment

    Search for `(req.body)`, `(req.params)`, or `(req.query)` - this will help uncover when **all** user-supplied parameters are being used to instantiate model objects.

#### Command Injection

    Search for `child_process.exec(` or `.exec(`

#### String interpolation regex:

    `.*?\$\{.*?\}\`

#### Nunjucks escaping disable

    \|\s*safe


#### Print all routes

    node -e  "const { app } = require('./app'); app._router.stack.forEach(function(r){if (r.route && r.route.path){console.log(r.route.path)}})"

One item to note is that if you can group routes logically based off something such as a user's role in the application (as an example). For instance, if we wanted to group all routes that should require the admin role together, we could do the following:

```javascript
const protectedRouter = express.Router()
adminProtectedRouter.use(adminOnlyMiddleware)

adminProtectedRouter.get('/admin', somestuff)

app.use(adminProtectedRouter)
```
