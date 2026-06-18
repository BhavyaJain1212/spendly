# Spec: Registration

## Overview
Add a working `POST /register` handler so new users can create an account.
The `GET /register` route already renders the form; this step wires it up to
the database. On success the user is redirected to the login page. On failure
the form is re-rendered with a clear inline error. This step also adds
`app.secret_key` to `app.py` so later steps (login session, flash messages)
have the foundation they need.

## Depends on
- Step 01 — Database setup (`get_db`, `init_db`, `seed_db` in `database/db.py`,
  both tables created on startup)

## Routes
- `POST /register` — validates form data, hashes password, inserts user, redirects to `/login` — public

## Database changes
No new tables or columns. Uses the existing `users` table:

| Column        | Used |
|---------------|------|
| name          | ✓    |
| email         | ✓    |
| password_hash | ✓    |
| created_at    | auto |

## Templates
- **Modify:** `templates/register.html`
  - Form action already points to `POST /register` — no change needed
  - `{% if error %}` block already present — no change needed
  - Repopulate `name` and `email` fields after a failed submission so the user
    does not have to retype them (add `value="{{ name or '' }}"` and
    `value="{{ email or '' }}"`)

## Files to change
- `app.py` — add `POST /register` route; add `app.secret_key`; add
  `request`, `redirect`, `url_for` to Flask imports (if not already imported)
- `database/db.py` — add `create_user(name, email, password)` function
- `templates/register.html` — repopulate name/email on failed submission

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- `create_user()` lives in `database/db.py`, not inline in the route
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate in this order, stopping at the first failure:
  1. Name is not blank
  2. Email is not blank
  3. Password is at least 8 characters
  4. Email is not already taken (catch `sqlite3.IntegrityError`)
- On success: `redirect(url_for('login'))`
- On failure: `render_template('register.html', error=..., name=name, email=email)`
- `app.secret_key` must be set before any `session` or `flash` usage in later steps;
  use a hard-coded dev string for now (e.g. `"dev-secret-change-in-prod"`)

## Definition of done
- [ ] Submitting the form with valid data creates a new row in `users`
- [ ] Password is stored as a hash, never plaintext
- [ ] Duplicate email shows the error "An account with that email already exists."
- [ ] Blank name shows the error "Name is required."
- [ ] Blank email shows the error "Email is required."
- [ ] Password shorter than 8 characters shows "Password must be at least 8 characters."
- [ ] After a failed submission, the name and email fields are repopulated
- [ ] Successful registration redirects to `/login`
- [ ] App starts without errors after this change
