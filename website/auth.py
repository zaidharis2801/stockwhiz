from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, send_mail
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os



from .emailclass import sendmail

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')

@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        accountnumber = request.form.get('account')
        profile_pic = request.files['profile_pic']

        # Grab Image Name

        pic_filename = secure_filename(profile_pic.filename)


        # Set UUID
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save That Image
        saver = request.files['profile_pic']

        # Change it to a string to save to db
        profile_pic = pic_name


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(lastname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(address) > 100:
            flash('Address must be less than or equal to 100 characters.', category='error')
        elif len(accountnumber) != 16:
            flash('Account Number must be equal to 16 characters.', category='error')
        else:
            new_user = User(email=email, first_name=firstname, last_name=lastname,
                            password=generate_password_hash(password, method='sha256'), CurrentAddress = address, AccountNumber = accountnumber, CurrentBalance = 0, profile_pic = profile_pic)
            db.session.add(new_user)
            db.session.commit()
            saver.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            sendmail("Account Created!", "ADH Destinies", "adhdestinies@gmail.com", firstname, email,
                     "Account Created Successfully!")
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


def send_reset_email(user):
    token = user.get_reset_token()
    #     msg = Message('Password Reset Request',
    #                   sender='noreply@demo.com',
    #                   recipients=[user.email])
    #     msg.body = f'''To reset your password, visit the following link:
    #     {url_for('auth.reset_token', token=token, _external=True)}
    #
    #     If you did not make this request then simply ignore this email and no changes will be made.
    # '''
    #     mail.send(msg)

    x = {url_for('auth.reset_token', token=token, _external=True)}
    y = user.first_name
    z =  user.email
    sendmail("Password Reset Request", "ADH Destinies", "adhdestinies@gmail.com", y, z,
             "To reset your password, visit the following link:" + str(x) +
             " If you did not make this request then simply ignore this email and no changes will be made."
             )


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # if current_user.is_authenticated:
    #     return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('forget.html', user = current_user)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashedpassword = generate_password_hash(password, method='sha256')
            user.password = hashedpassword
            db.session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('auth.login'))
    return render_template('reset_token.html', user = current_user)
