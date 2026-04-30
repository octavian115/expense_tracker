# Spec: Login and Logout

## Overview
This step implements session-based authentication for Spendly. Users can sign in with their email and password; on success a server-side session records their identity. A logout route clears the session. The login route also acts as the gateway to all protected pages — every stub route that requires authentication will redirect here until the user is signed in. This is the first step that introduces Flask's `session` object, which all subsequent steps depend on.

## Depends on
- Step 01 — Database Setup (`users` table and `get_db()` must exist)
- Step 02 — Registration (`create_user`, `get_user_by_email` must exist; at least one user must be in the DB)

## Routes
- `POST /login` — Validates credentials, starts session, redirects to `/` until the dashboard is implemented in Step 5
- `GET /login` — Renders the login form — public
- `GET /logout` — Clears the session, redirects to `/` — public (safe to call when already logged out)

## Database changes
No database changes. The existing `users` table already stores `password_hash`.

## Templates
- **Modify:** `templates/login.html` — add a POST form with `email` and `password` fields, flash message display, and a link to the registration page

## Files to change
- `app.py` — implement `POST /login` logic and `GET /logout` logic
- `templates/login.html` — add the login form and flash display

## Files to create
No new files.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available via the existing `werkzeug` install.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only via `get_db()`
- Parameterised queries only — no f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Store only `user_id` and `user_name` in `session` — never store the password hash or full row
- Use `session.clear()` in logout — not `session.pop()` one key at a time
- After successful login redirect with `redirect(url_for(...))` — never a bare string URL
- Flash an error message on bad credentials — do not reveal whether the email or password was wrong (use a generic message)
- The login route must accept both GET and POST (`methods=["GET", "POST"]`)
- Do not implement any `@login_required` decorator in this step — that belongs to a later step

## Definition of done
- [ ] Visiting `GET /login` renders a page with email and password fields and a submit button
- [ ] Submitting valid credentials (e.g. `demo@spendly.com` / `demo123`) sets a session and redirects away from `/login`
- [ ] Submitting an unrecognised email shows a flash error without revealing which field was wrong
- [ ] Submitting a correct email but wrong password shows the same generic flash error
- [ ] Visiting `GET /logout` clears the session and redirects to `/`
- [ ] After logout, the session no longer contains `user_id`
- [ ] The login page displays a link to the registration page
- [ ] The login form uses `url_for("login")` as its action — no hardcoded URLs in the template
