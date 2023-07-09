from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)



@auth.route("/login", methods=["GET", "POST"] )
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in as {} ".format(user.username.title()))

                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash("Invalid Credentials. \n Use valid credentials; if otherwise, your user account will be locked.", category="warning")
        else: 
            flash("Invalid Credentials", category="error")

    return render_template("login.html", user=current_user )

@auth.route("/signup", methods=["GET", "POST"])
def sign_up(): 
    if request.method == 'POST':
        name = request.form.get("name")
        cohort = request.form.get("cohort")
        country = request.form.get("country")
        phone = request.form.get("phone")
        email = request.form.get("email")
        status = request.form.get("status")
        about = request.form.get("about")
        github = request.form.get("github")
        twitter = request.form.get("twitter")
        instagram = request.form.get("instagram")
        facebook = request.form.get("facebook")
        website = request.form.get("website")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        username = request.form.get("username")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email already in use.', category='error')
        elif username_exists:
            flash('Username already in use.', category='error')
        elif len(name) < 8:
            flash('Please enter your fullname', category = 'error')
        elif password != password2:
            flash('Password mismatch.', category='error')
        elif len(username) < 3:
            flash('Username is too short.', category='error')
        elif len(username) > 18:
            flash('Username is too long.', category='error')
        elif len(password) < 6:
            flash('Password is too weak.', category='error')
        elif len(email) < 6:
            flash('Invalid email', category='error')
        else:
            new_user = User(email = email,
                            name = name,
                            username = username,
                            password = generate_password_hash(password, method='sha256'),
                            cohort = cohort,
                            country = country,
                            phone = phone,
                            status = status,
                            about = about,
                            instagram = instagram,
                            twitter = twitter,
                            github = github,
                            facebook = facebook,
                            website = website,
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Successfully Created. Welcome ' + current_user.username)
            return redirect(url_for('views.index', user=current_user))
        
    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))