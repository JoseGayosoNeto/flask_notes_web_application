from APP import db
from flask import Blueprint, flash, redirect, url_for, render_template, request
from ..models import user_model
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route('/')
def login():
    return render_template("home.html")

@auth.route('/login', methods=["POST"])
def login_post():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = user_model.User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Incorrect email ou password", 400)
            return redirect(url_for("auth.login"))
        
        login_user(user=user)

        return redirect(url_for("main.profile"))

    return redirect(url_for("auth.login"))

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=["POST"])
def signup_post():
    if request.method == "POST":
        email = request.form.get("email")
        fullname = request.form.get("fullname")
        password = request.form.get("password")

        password_hash = generate_password_hash(password)

        has_user = user_model.User.query.filter_by(email=email).first()
        if has_user:
            flash("Email already registered in the system.", "error_user_already_exists")
        
        if not email:
            flash("Email is required.", "error_not_email")
        
        if not fullname:
            flash("Full Name is required.", "error_not_fullname")
        
        if not password:
            flash("Password is required.", "error_not_password")
        
        if len(password) < 6:
            flash("Password must have at least 6 characters", "error_password_minlength")
        
        if len(password) > 20:
            flash("Password must be a maximum of 20 characters", "error_password_maxlength")

        if not has_user and email and fullname and password and 6 <= len(password) <= 20:
            new_user = user_model.User(email = email, full_name = fullname, password= password_hash)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))

    return redirect(url_for('auth.signup'))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
    