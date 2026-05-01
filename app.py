from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from database.db import create_user, get_db, get_user_by_email, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not all([name, email, password, confirm]):
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.")
            return render_template("register.html")

        if get_user_by_email(email):
            flash("Email already registered.")
            return render_template("register.html")

        create_user(name, email, password)
        flash("Account created! Please sign in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.")
            return render_template("login.html")

        session.clear()
        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Ayush Kumar",
        "email": "ayush@example.com",
        "member_since": "January 2024",
    }
    stats = {
        "total_spent": "₹1,850.24",
        "transaction_count": 12,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "Apr 25, 2026", "description": "Coffee shop",    "category": "Food",          "amount": "₹9.99"},
        {"date": "Apr 21, 2026", "description": "Miscellaneous",  "category": "Other",         "amount": "₹18.75"},
        {"date": "Apr 17, 2026", "description": "Clothes",        "category": "Shopping",      "amount": "₹80.00"},
        {"date": "Apr 13, 2026", "description": "Cinema tickets", "category": "Entertainment", "amount": "₹25.00"},
        {"date": "Apr 10, 2026", "description": "Pharmacy",       "category": "Health",        "amount": "₹45.00"},
    ]
    categories = [
        {"name": "Bills",         "total": "₹120.00", "pct": 65},
        {"name": "Shopping",      "total": "₹80.00",  "pct": 43},
        {"name": "Transport",     "total": "₹35.00",  "pct": 19},
        {"name": "Entertainment", "total": "₹25.00",  "pct": 14},
        {"name": "Health",        "total": "₹45.00",  "pct": 24},
        {"name": "Food",          "total": "₹22.49",  "pct": 12},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           transactions=transactions,
                           categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
