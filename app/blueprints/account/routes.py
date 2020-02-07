from app import db
from app.models import User
from flask import render_template, redirect, url_for, flash
from app.blueprints.account.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user
from app.blueprints.account import account

@account.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  context = {
    'form': form
  }
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash("You've used either the wrong email or password. Try again!", "danger")
      return redirect(url_for('account.login'))
    flash("You have logged in successfully", "success")
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('index'))
  return render_template('login.html', **context)

@account.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  
  if form.validate_on_submit():
    u = User(name=form.name.data, email=form.email.data)
    u.generate_password(form.password.data)
    db.session.add(u)
    db.session.commit()
    flash("You have registered successfully.", 'warning')
    return redirect(url_for('account.login'))

  context = {
    'form': form
  }
  return render_template('register.html', **context)

@account.route('/logout')
def logout():
  logout_user()
  flash("You have successfully logged out", "primary")
  return redirect(url_for('account.login'))