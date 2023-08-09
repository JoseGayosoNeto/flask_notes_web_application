from APP import db, mail
from flask import Blueprint, flash, redirect, url_for, render_template, request
from ..models import user_model, notes_model, note_content_model
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from secrets import token_urlsafe
from datetime import datetime, timedelta

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
            flash("Incorrect email ou password", "error_incorrect_credentials")
            return redirect(url_for("auth.login"))
        
        if user.token_confirmed == True:
            login_user(user=user)
        else:
            flash("Account not confirmed!", "error_not_confirmed_account")
            return redirect(url_for("auth.login"))

    return redirect(url_for("main.profile"))

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
            token = token_urlsafe(16)
            new_user = user_model.User(email = email, full_name = fullname, password = password_hash, account_token = token)
            db.session.add(new_user)
            db.session.commit()

            confirm_account_url = url_for('auth.confirm', account_token=token, _external=True)
            msg = Message('Confirm your account', recipients=[email])
            msg.html = render_template("confirmation_email.html", confirm_account_url=confirm_account_url)
            mail.send(msg)
            flash(f"A confirmation email has been sent to {email}. You can now leave this page.", "confirmation_message")

    return redirect(url_for('auth.signup'))
    
@auth.route('/confirm/<string:account_token>')
def confirm(account_token):
    user = user_model.User.query.filter_by(account_token=account_token).first()

    if user:
        time_limit = timedelta(days=7)
        if datetime.utcnow() - user.token_generated_at > time_limit:
            db.session.delete(user)
            db.session.commit()
            
            return "Expired token. Create a new account."
        else:
            user = user_model.User.query.filter_by(account_token=account_token).update({"token_confirmed" : True})
            db.session.commit()
            user = user_model.User.query.filter_by(account_token=account_token).first()
            msg = Message('Account confirmed', recipients=[user.email])
            msg.html = render_template("account_confirmed_message.html", user=user)
            mail.send(msg)
            return redirect(url_for('auth.login'))
    
    return redirect(url_for("auth.login"))




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/delete_user/user/<int:id>')
@login_required
def delete_user(id):
    user = user_model.User.query.filter_by(id=id).first()
    if user:
        if user.notes.filter(notes_model.Note.contents.any()).count():
            for content in user.notes:
                note_content_model.Note_Content.query.filter_by(note_id=content.id).delete()
            
        
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("auth.signup"))