import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"


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
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Name is required.", name=name, email=email)
    if not email:
        return render_template("register.html", error="Email is required.", name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        return render_template("login.html", error="Email is required.", email=email)
    if not password:
        return render_template("login.html", error="Password is required.", email=email)

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.", email=email)

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Step 4 is UI-only — all data is hardcoded here. Step 5 will replace this
    # context with real queries from database/db.py. Category names match the
    # seed categories so the swap is a drop-in. The dataset cross-foots:
    # amounts sum to 1,284.50 and the breakdown percents sum to 100.
    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "initials": "DU",
        "member_since": "January 2026",
    }
    stats = {
        "total_spent": "1,284.50",
        "transaction_count": 5,
        "top_category": "Food",
    }
    transactions = [
        {"date": "18 Jun 2026", "description": "Restaurant dinner", "category": "Food",          "amount": "640.00"},
        {"date": "15 Jun 2026", "description": "Electricity bill",  "category": "Bills",         "amount": "420.50"},
        {"date": "12 Jun 2026", "description": "New running shoes", "category": "Shopping",      "amount": "120.00"},
        {"date": "10 Jun 2026", "description": "Cinema ticket",     "category": "Entertainment", "amount": "64.00"},
        {"date": "03 Jun 2026", "description": "Bus pass top-up",   "category": "Transport",     "amount": "40.00"},
    ]
    breakdown = [
        {"name": "Food",          "total": "640.00", "percent": 50},
        {"name": "Bills",         "total": "420.50", "percent": 33},
        {"name": "Shopping",      "total": "120.00", "percent": 9},
        {"name": "Entertainment", "total": "64.00",  "percent": 5},
        {"name": "Transport",     "total": "40.00",  "percent": 3},
    ]
    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        breakdown=breakdown,
    )


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
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
