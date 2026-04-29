---
description: Create dummy Indian user(s) in the database. Usage: /seed-user [count=1]
allowed-tools: Read, Bash(python3:*)
---

Read `database/db.py` to understand the users table schema and the `get_db()` helper.

Then write and run a Python script using Bash that creates $ARGUMENTS{default:1} user(s):

For each user:
1. Generate a realistic random Indian user:
   - Name: realistic Indian first + last name (vary regions — Bengali, Tamil, Punjabi, Marathi, etc.)
   - Email: derived from name with random 2–3 digit suffix (e.g. priya.nair47@gmail.com)
   - Password: "password123" hashed with werkzeug's `generate_password_hash`
   - created_at: current UTC datetime

2. Retry if the email already exists in the users table (max 5 attempts, then skip with a warning).

3. Insert using the same `get_db()` pattern from db.py. Wrap in try/except — print any DB errors clearly.

4. After all inserts, print a summary table:
   - id | name | email