from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User_Details, User_Database, History
from app import db, app
from app.forms import RegisterForm


with app.app_context():
    db.create_all()
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")
@app.route("/user_menu", methods=["GET", "POST"])
def user_menu():
    return render_template("user_menu.html")

@app.route("/login", methods=["GET", "POST"])
def detail():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User_Details.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["username"]=user.username
            session["user_id"]=user.id
            return redirect(url_for("user_menu"))
        else:
            return "Invalid Username or Password", 401
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256')
        hashed_confing_password = generate_password_hash(request.form.get("confing_passwird"), method='pbkdf2:sha256')
        u1 = User_Details(username=request.form.get("username"), email=request.form.get("email"),
                          phone=request.form.get("phone"), password=hashed_password,
                          confirm_password=hashed_confing_password)
        db.session.add(u1)
        db.session.commit()
        message = "User successfully created"

        return redirect(url_for("detail"))

@app.route("/show_balance", methods=["GET", "POST"])
def show_balance():
    if request.method == "POST":
        username = session["username"]
        user = User_Database.query.filter_by(username=session["username"]).first()
        if username:
            return render_template("show_balance.html", balance=user.balance, username=user.username)
        else:
            message = ("User not found")
            return render_template("show_balance.html", message=message)
    return render_template("show_balance.html")



@app.route("/add_balance", methods=["GET", "POST"])
def add_balance():
    if request.method == "GET":
        return render_template("add_balance.html")
    else:
        username = session["username"]
        balance = float(request.form.get("balance"))

        existing_user = User_Database.query.filter_by(username=username).first()

        if existing_user:
            existing_user.balance += balance
            db.session.commit()
            message = "Balance successfully updated"
        else:
            u1 = User_Database(username=username, balance=balance)
            db.session.add(u1)
            db.session.commit()
            message = "Balance successfully added"

        return render_template("add_balance.html", message=message)


@app.route("/transfer_money", methods=["GET", "POST"])
def transfer_money():
    message = None
    if request.method == "POST":
        from_username = session["username"]
        to_username = request.form.get("to_username")
        amount = request.form.get("balance")

        user1 = User_Database.query.filter_by(username=from_username).first()
        user2 = User_Database.query.filter_by(username=to_username).first()

        if user1 and user2 and user2!=user1:
            if user1.balance >= float(amount):
                user1.balance -= float(amount)
                user2.balance += float(amount)
                history = History(sender_id=user1.id, receiver_id=user2.id, amount=amount, create_at=datetime.now())
                db.session.add(history)
                db.session.commit()
                message = "Transfer successful."
            else:
                message = "Not enough money."
        else:
            message = "User not found."

    return render_template("transfer_money.html", message=message)


@app.route("/transfer_history", methods=["G"
                                         "ET"])
def transfer_history():
    history_records = History.query.all()
    return render_template("transfer_history.html", history=history_records)



@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        username = session["username"]
        user = User_Database.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            message = "User successfully deleted"
        else:
            message = "User not found"
        return render_template("delete_account.html", message=message)
    else:
        return render_template("delete_account.html")


if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")