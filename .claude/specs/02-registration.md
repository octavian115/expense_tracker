# Spec: Registration

## Overview
Implement user registration so that new visitors can create an account on Spendly.
This step wires up the `POST /register` route to validate form input, insert a hashed
password into the `users` table, and redirect to the login page on success.
It also sets `app.secret_key` (required for `flash()`) and adds the two DB helpers
needed by this and future auth steps.

## Depends on
Step 01 — Database Setup (users table and `get_db()` must exist).

## Routes
- `GET /register` — already implemented, renders `register.html` — public
- `POST /register` — validates input, creates user, redirects to `/login` — public

## Database changes
No new tables.
Two new helper functions in `database/db.py`:
- `get_user_by_email(email)` — returns the matching row or `None`
- `create_user(name, email, password)` — hashes password with `werkzeug`, inserts row, returns new `user_id`

## Templates
- **Modify:** `templates/register.html` — add `<form method="POST">` with fields for
  `name`, `email`, `password`, `confirm_password`; display flashed error/success messages

## Files to change
- `app.py` — set `app.secret_key`; add `POST /register` route; import `flash`, `redirect`, `url_for`, `request`, `session`
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — add form and flash message display

## Files to create
- `static/css/register.css` — page-specific styles for the registration form

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never store plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any `flash()` or `session` usage; use a hard-coded
  dev string for now (e.g. `"dev-secret-change-in-prod"`) — do not use `os.urandom`
- Validate in this order: all fields present → passwords match → email not already taken
- On validation failure: `flash()` the error and re-render `register.html` (do not redirect)
- On success: `flash()` a success message and `redirect(url_for('login'))`
- Use `abort(400)` only for truly malformed requests; prefer `flash` + re-render for user errors
- Do not set `session['user_id']` here — login is Step 3

## Definition of done
- [ ] `GET /register` still renders the form without errors
- [ ] Submitting with any blank field shows an error on the page (no redirect)
- [ ] Submitting with mismatched passwords shows an error on the page
- [ ] Submitting a duplicate email shows "Email already registered" on the page
- [ ] Valid submission inserts a new row in `users` with a hashed (not plaintext) password
- [ ] Valid submission redirects to `/login` with a success flash message visible
- [ ] `create_user()` and `get_user_by_email()` live in `database/db.py`, not in `app.py`
- [ ] No raw SQL strings in `app.py`
- [ ] App starts without errors after changes
