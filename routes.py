from aliceinit import app,db,login
from forms import LoginForm, RegistrationForm, VerifyForm
from models import Users, Subscribers, Messages, Homework
from funcs import numbercode

from flask import render_template, flash, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse





@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('home')), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return redirect(url_for('home')), 500

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if user.verified == '1' or user.verified == True:
            login_user(user, remember=form.remember_me.data)
            flash('You are logged in!', 'success')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
        else:
            flash('You must verify your account before logging in!')
            return redirect(url_for('verify'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You are logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Please log out first!')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(name = form.name.data, username=form.username.data.lower(), email=form.email.data.lower(), number=form.number.data, verified=False, plan='Student', numberverification = numbercode(6), token = 'NA')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('verify'))
    return render_template('register.html', title='Register', form=form)


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form = VerifyForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is not None and user.numberverification == form.numbercode.data:
            if user.verified == 0 or user.verified == False:
                user.verified = True
                db.session.commit()
                db.session.close()
                flash('Verified!')
                return redirect(url_for('login'))
            else:
                flash('You are already verified!')
                return redirect(url_for('login'))
        else:
            flash('Invalid code or email!')
            return redirect(url_for('verify'))

    return render_template('verify.html', form=form)



if __name__ == '__main__':
    app.run(debug = True)
