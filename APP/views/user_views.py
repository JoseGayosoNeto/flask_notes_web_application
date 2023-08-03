from APP import db
from flask import Blueprint, flash, redirect, url_for, render_template, request, make_response, jsonify
from ..models import user_model
from flask_login import login_user, login_required, logout_user

auth = Blueprint("auth", __name__)

@auth.route('/login')
def login():
    return "Login.html"

@auth.route('/login', methods=["POST"])
def login_post():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = user_model.User.query.filter_by(email=email).first()

        if not user or not user_model.User.check_password(user.password, password):
            flask(make_response("Incorrect email ou password"), 400)
            return redirect(url_for("auth.login"))
        
        login_user(user=user)

        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))

@auth.route('/signup')
def signup():
    return "Signup.html"

@auth.route('/signup', methods=["POST"])
def signup_post():
    if request.method == "POST":
        email = request.form.get("email")
        fullname = request.form.get("fullname")
        password = request.form.get("password")

        password_hash = user_model.User.generate_encrypted_password

        has_user = user_model.User.query.filter_by(email=email).first()
        if has_user:
            flash(make_response("Email already registered in the system."), 400)
            return redirect(url_for("auth.signup"))
        
        elif not email:
            flash(make_response("Email is required."), 400)
            return redirect(url_for("auth.signup"))
        
        elif not fullname:
            flash(make_response("Full Name is required."), 400)
            return redirect(url_for("auth.signup"))
        
        elif not password:
            flash(make_response("Password is required."), 400)
            return redirect(url_for("auth.signup"))
        
        new_user = user_model.User(email = email, fullname = fullname, password = password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return redirect(url_for('auth.signup'))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))
    