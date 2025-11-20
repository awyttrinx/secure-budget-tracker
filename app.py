from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os

# ------------------ APP SETUP ------------------ #
app = Flask(__name__)

# 🔒 Sichere Konfiguration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-key")

# 🌿 Verbindung zur MongoDB Atlas (mit konkretem DB-Namen!)
app.config["MONGO_URI"] = (
    "mongodb+srv://antoniawittrin_db_user:Musikerin911%21"
    "@cluster0.1nyxnng.mongodb.net/girlmath?retryWrites=true&w=majority&appName=Cluster0"
)

mongo = PyMongo(app)

# --- Verbindung testen ---
try:
    mongo.cx.server_info()
    print("✅ MongoDB connection successful!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

csrf = CSRFProtect(app)

# ------------------ LOGIN SETUP ------------------ #
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# ------------------ USER CLASS ------------------ #
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.balance = user_data.get("balance", 0.0)

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

# ------------------ ROUTES ------------------ #
@app.route("/")
@login_required
def index():
    transactions = list(mongo.db.transactions.find({"user_id": current_user.id}).sort("date", -1))
    total = float(current_user.balance)
    return render_template("index.html", transactions=transactions, total=total)


@app.route("/set_balance", methods=["POST"])
@login_required
def set_balance():
    amount = request.form.get("balance")
    try:
        amount = float(amount)
    except ValueError:
        flash("Please enter a valid number.", "error")
        return redirect(url_for("index"))

    mongo.db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": {"balance": amount}})
    flash(f"Balance set to ${amount:.2f}", "success")
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
@login_required
def add_transaction():
    description = request.form.get("description", "").strip()
    amount = request.form.get("amount", "").strip()

    if not description or not amount:
        flash("Both fields are required.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount)
    except ValueError:
        flash("Amount must be a valid number.", "error")
        return redirect(url_for("index"))

    mongo.db.transactions.insert_one({
        "description": description,
        "amount": amount,
        "date": datetime.utcnow(),
        "user_id": current_user.id
    })

    new_balance = float(current_user.balance) - amount
    mongo.db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": {"balance": new_balance}})

    flash("Transaction added and balance updated!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<id>")
@login_required
def delete_transaction(id):
    transaction = mongo.db.transactions.find_one({"_id": ObjectId(id)})
    if not transaction or transaction["user_id"] != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("index"))

    mongo.db.transactions.delete_one({"_id": ObjectId(id)})
    mongo.db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$inc": {"balance": transaction["amount"]}}
    )

    flash("Transaction deleted and balance restored.", "success")
    return redirect(url_for("index"))


@app.route("/analytics")
@login_required
def analytics():
    transactions = list(mongo.db.transactions.find({"user_id": current_user.id}))
    return render_template("analytics.html", transactions=transactions)


@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    if request.method == "POST":
        goal_name = request.form.get("goal_name")
        target_amount = request.form.get("target_amount")

        if not goal_name or not target_amount:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("goals"))

        try:
            target_amount = float(target_amount)
        except ValueError:
            flash("Target amount must be a number.", "error")
            return redirect(url_for("goals"))

        mongo.db.goals.insert_one({
            "name": goal_name,
            "target": target_amount,
            "saved": 0.0,
            "date_created": datetime.utcnow(),
            "user_id": current_user.id
        })

        flash(f"Goal '{goal_name}' added (target: ${target_amount}) 💪", "success")
        return redirect(url_for("goals"))

    goals = list(mongo.db.goals.find({"user_id": current_user.id}).sort("date_created", -1))
    return render_template("goals.html", goals=goals)


@app.route("/delete_goal/<id>")
@login_required
def delete_goal(id):
    goal = mongo.db.goals.find_one({"_id": ObjectId(id)})
    if not goal or goal["user_id"] != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("goals"))

    mongo.db.goals.delete_one({"_id": ObjectId(id)})
    flash("Goal deleted successfully.", "success")
    return redirect(url_for("goals"))


@app.route("/update_goal/<id>", methods=["POST"])
@login_required
def update_goal(id):
    goal = mongo.db.goals.find_one({"_id": ObjectId(id)})
    if not goal or goal["user_id"] != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("goals"))

    saved_amount = request.form.get("saved_amount", "").strip()

    try:
        saved_amount = float(saved_amount)
        mongo.db.goals.update_one({"_id": ObjectId(id)}, {"$set": {"saved": saved_amount}})
        flash("Goal progress updated!", "success")
    except ValueError:
        flash("Invalid number entered.", "error")

    return redirect(url_for("goals"))


# ------------------ AUTH ROUTES ------------------ #
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        if not username or not email or not password:
            flash("Please fill out all fields.", "error")
            return redirect(url_for("register"))

        if mongo.db.users.find_one({"username": username}):
            flash("Username already taken.", "error")
            return redirect(url_for("register"))

        if mongo.db.users.find_one({"email": email}):
            flash("Email already registered.", "error")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_pw,
            "balance": 0.0
        })

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user_data = mongo.db.users.find_one({
            "$or": [{"username": identifier}, {"email": identifier}]
        })

        if not user_data or not check_password_hash(user_data["password"], password):
            flash("Invalid username/email or password.", "error")
            return redirect(url_for("login"))

        login_user(User(user_data))
        flash(f"Welcome back, {user_data['username']} 💕", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("login"))


# ---------------- ERROR HANDLERS ---------------- #
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# ------------------ RUN APP ------------------ #
if __name__ == "__main__":
    app.run(debug=True)

