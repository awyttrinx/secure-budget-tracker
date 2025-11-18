from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.id}: {self.description}>"

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    total = sum(t.amount for t in transactions)
    return render_template("index.html", transactions=transactions, total=total)

@app.route("/add", methods=["POST"])
def add_transaction():
    description = request.form.get("description", "").strip()
    amount = request.form.get("amount", "").strip()

    # Input validation
    if not description or not amount:
        flash("Both fields are required.", "error")
        return redirect(url_for("index"))

    try:
        amount = float(amount)
    except ValueError:
        flash("Amount must be a valid number.", "error")
        return redirect(url_for("index"))

    if len(description) > 100:
        flash("Description too long (max 100 characters).", "error")
        return redirect(url_for("index"))

    new_transaction = Transaction(description=description, amount=amount)
    db.session.add(new_transaction)
    db.session.commit()

    flash("Transaction added successfully!", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    flash("Transaction deleted.", "success")
    return redirect(url_for("index"))

# -----------------------------
# ADDITIONAL PAGES
# -----------------------------

@app.route("/goals")
def goals():
    # You can later replace these with dynamic data
    goals_data = [
        {"name": "Europe Trip ✈️", "saved": 3000, "target": 4000},
        {"name": "New Laptop 💻", "saved": 800, "target": 1500},
        {"name": "Emergency Fund 💕", "saved": 1200, "target": 5000}
    ]
    return render_template("goals.html", goals=goals_data)

@app.route("/analytics")
def analytics():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template("analytics.html", transactions=transactions)

# -----------------------------
# MAIN ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)