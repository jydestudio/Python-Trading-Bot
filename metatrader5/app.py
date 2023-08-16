from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
import bot

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret."
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MESSAGE_FLASHING_OPTIONS'] = {"duration": 5}
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# the below code works this way ( if the user tries to access the web app and is not authenticated this well redirect
# him to the specified route, in this case the login route
login_manager.login_view = 'login'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


class signupForm(FlaskForm):
    fname = StringField("First name *", validators=[DataRequired()], render_kw={'autofocus': True})
    lname = StringField("Last name *", validators=[DataRequired()])
    email = StringField("Email address *", validators=[DataRequired(), Email()])
    password = PasswordField("Password *", validators=[DataRequired(), Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*['
                                                                              r'@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                                                                              message='Password must contain symbols, '
                                                                                      'letters, and numbers, '
                                                                                      'and be at least 8 characters '
                                                                                      'long'), length(min=8)],
                             render_kw={'id': 'password'})
    confirm_password = PasswordField("Confirm password *",
                                     validators=[DataRequired(), EqualTo('password', message="Passwords should match"),
                                                 Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*['
                                                        r'@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                                                        message='Password must contain symbols, '
                                                                'letters, and numbers, '
                                                                'and be at least 8 characters '
                                                                'long'), length(min=8)],
                                     render_kw={'id': 'confirm_password'})
    checkbox = BooleanField("", render_kw={'class': 'checkbox', 'id': 'checkbox'})

    submit = SubmitField("SIGNUP", render_kw={'id': 'btn', 'disabled': True})


class loginForm(FlaskForm):
    email = StringField("Email address *", validators=[DataRequired(), Email()], render_kw={'autofocus': True})
    password = PasswordField("Password *", validators=[DataRequired()])
    submit = SubmitField("LOGIN")


class integrateForm(FlaskForm):
    login = StringField("MetaTrader5 login *", validators=[DataRequired(), Email()], render_kw={'autofocus': True})
    password = PasswordField("Password *", validators=[DataRequired()])
    checkbox = BooleanField("", render_kw={'class': 'checkbox', 'id': 'checkbox'})
    submit = SubmitField("INTEGRATE", render_kw={'disabled': True, 'id': 'btn'})


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=False, nullable=False)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(80), nullable=False)
    email_confirmed = False
    password = db.Column(db.String(120), nullable=False)

    # this keeps track of users' email confirmation status
    active = db.Column(db.Boolean(), nullable=False)

    # this checks if user have integrated there mt5 account
    integrated = db.Column(db.Boolean(), nullable=False)


# User loader function for Flask-Login
# the user loader function handle the user's session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.route("/")
# def home():
#     return render_template("email-template.html",)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = loginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect("/dashboard")

            else:
                flash("Incorrect Password", "danger")
                return render_template("login.html", form=form)

        else:
            flash("Incorrect email address", "danger")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = signupForm()

    if form.validate_on_submit() and form.password.data == form.confirm_password.data:
        email = form.email.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=12)
        new_user = User(email=email, fname=form.fname.data, lname=form.lname.data, active=True, integrated=False,
                        password=password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

        # token = serializer.dumps(email, salt='email-confirm')
        # confirm_url = url_for('confirm_email', token=token, _external=True)
        # print(confirm_url)

        # flash(f'A confirmation email has been sent to {email}.', 'success')

    # else:
    #     print("password does not match")
    #     flash("password does not match", "danger")
    #     # return render_template("signup.html", form=form)

    if form.password.data != form.confirm_password.data:
        flash("Password doesn't match", "danger")
        return render_template("signup.html", form=form)

    return render_template("signup.html", form=form)


# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#    try:
#        email = serializer.loads(token, salt='email-confirm', max_age=3600)
#        user = User.query.filter_by(email=email).first()
#        user.active = True
#        db.session.commit()
#        flash('Email confirmed. You can now log in.', 'success')
#        # return redirect(url_for('login'))
#        print("user is updated")

#    except:
#        flash('The confirmation link is invalid or has expired.', 'danger')
#        # return redirect(url_for('login'))
#        print("invalid or expired")


@app.route("/integrate-mt5")
def integrate():
    form = integrateForm()
    if form.validate_on_submit():
        account = form.login.data
        password = form.login.data

        if bot.connect(account, password):
            return redirect("/dashboard")
        else:
            flash("Cannot connect to MetaTrader5, check login details or try again later")
            return render_template("integrate.html", form=form)
    return render_template("integrate.html", form=form)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(port=3000, debug=True)
