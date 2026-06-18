# Spec: Login and Logout

## Overview
Wire up the `POST /login` handler so users can authenticate with their email and
password, and implement the `GET /logout` route so they can end their session.
On successful login, Flask's built-in `session` stores the user's id and name,
then redirects to `/profile`. On failure the login form is re-rendered with an
inline error. Logout clears the session and returns the user to the landing page.
This step also fixes the hardcoded `action="/login"` in `login.html` to use
`url_for()`, consistent with the rest of the project.

## Depends on
- Step 01 — Database setup (`get_db`, `users` table, `PRAGMA foreign_keys = ON`)
- Step 02 — Registration (`create_user`, `app.secret_key` already set)

## Routes
- `POST /login` — validates credentials, sets session, redirects to `/profile` — public
- `GET /logout` — clears session, redirects to `/` — public

## Database changes
No new tables or columns. Adds one new helper function to read from the existing
`users` table:

| Function | Purpose |
|---|---|
| `get_user_by_email(email)` | Returns the matching `users` row (or `None`) |

## Templates
- **Modify:** `templates/login.html`
  - Change `action="/login"` → `action="{{ url_for('login') }}"` (fix hardcoded URL)
  - Repopulate the email field on failed submission: add `value="{{ email or '' }}"` to the email input

## Files to change
- `app.py` — add `session` to Flask imports; implement `POST /login`; replace stub
  `GET /logout` with real implementation; import `get_user_by_email` from `database.db`
- `database/db.py` — add `get_user_by_email(email)` function
- `templates/login.html` — fix hardcoded form action; repopulate email on error

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed)
and Flask's built-in `session`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Password verification via `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Login validation order, stop at first failure:
  1. Email field is not blank
  2. Password field is not blank
  3. User with that email exists AND password matches — show a single generic error
     `"Invalid email or password."` for both cases (do not distinguish which field is wrong)
- On success: set `session['user_id']` and `session['user_name']`, then
  `redirect(url_for('profile'))`
- On failure: `render_template('login.html', error=..., email=email)`
- `GET /logout`: call `session.clear()`, then `redirect(url_for('landing'))`
- `get_user_by_email` lives in `database/db.py`, not inline in the route

## Definition of done
- [ ] Submitting the login form with correct credentials sets the session and redirects to `/profile`
- [ ] Submitting with a wrong password shows `"Invalid email or password."`
- [ ] Submitting with an unknown email shows `"Invalid email or password."`
- [ ] Blank email field shows `"Email is required."`
- [ ] Blank password field shows `"Password is required."`
- [ ] After a failed login, the email field is repopulated
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] `session['user_id']` and `session['user_name']` are set after successful login
- [ ] After logout, `session` contains no user data
- [ ] App starts without errors after this change
