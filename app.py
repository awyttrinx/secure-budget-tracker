from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf.csrf import CSRFProtect

# ------------------ APP SETUP ------------------ #
app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# ------------------ MODELS ------------------ #
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship("Transaction", backref="user", lazy=True)
    goals = db.relationship("Goal", backref="user", lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Transaction {self.id}: {self.description}>"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    saved = db.Column(db.Float, default=0.0)
    target = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def progress(self):
        return round((self.saved / self.target) * 100, 2) if self.target > 0 else 0

# ------------------ LOGIN MANAGER ------------------ #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------ #

@app.route("/")
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    total = current_user.balance
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

    current_user.balance = amount
    db.session.commit()
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

    current_user.balance -= amount
    new_transaction = Transaction(description=description, amount=amount, user_id=current_user.id)
    db.session.add(new_transaction)
    db.session.commit()

    flash("Transaction added and balance updated!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("index"))

    current_user.balance += transaction.amount
    db.session.delete(transaction)
    db.session.commit()

    flash("Transaction deleted and balance restored.", "success")
    return redirect(url_for("index"))


@app.route("/analytics")
@login_required
def analytics():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
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

        new_goal = Goal(name=goal_name, target=target_amount, user_id=current_user.id)
        db.session.add(new_goal)
        db.session.commit()
        flash(f"Goal '{goal_name}' added (target: ${target_amount}) 💪", "success")
        return redirect(url_for("goals"))

    goals = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.date_created.desc()).all()
    return render_template("goals.html", goals=goals)


@app.route("/delete_goal/<int:id>")
@login_required
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    if goal.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("goals"))

    db.session.delete(goal)
    db.session.commit()
    flash("Goal deleted successfully.", "success")
    return redirect(url_for("goals"))


@app.route("/update_goal/<int:id>", methods=["POST"])
@login_required
def update_goal(id):
    goal = Goal.query.get_or_404(id)
    if goal.user_id != current_user.id:
        flash("Unauthorized action.", "error")
        return redirect(url_for("goals"))

    saved_amount = request.form.get("saved_amount", "").strip()

    try:
        goal.saved = float(saved_amount)
        db.session.commit()
        flash("Goal progress updated!", "success")
    except ValueError:
        flash("Invalid number entered.", "error")

    return redirect(url_for("goals"))


# ------------------ AUTH ROUTES ------------------ #
@app.route("/register", methods=["GET", "POST"])
existing_user = User.query.filter_by(username=username).first()
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if not username or not password:
            flash("Please fill out all fields.", "error")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken.", "error")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

        login_user(user)
        flash("Welcome back 💕", "success")
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
    with app.app_context():
        db.create_all()  # <-- muss eingerückt sein (4 Leerzeichen)
    app.run(debug=True)

# ---------------- ERROR HANDLERS ---------------- #
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500