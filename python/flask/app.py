from flask import Flask, request, make_response, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    assert True, "This is a test"
    return 'Hello, World!'

@app.route('/double/<num>')
def double(num):
    return str(2 * num)

# @app.route('/double/<num>')
# def double(num):
#     return {'ans': str(2 * num)}, 404, {'Content-Type': 'text/plain'}

click_counts = {}
last_session_id = 0

@app.route('/click-count')
def click_count():
    session_id = request.cookies.get('sessionId')
    if session_id :
        if session_id in click_counts:
            click_counts[session_id] += 1
            return str(click_counts.get(session_id))+ " click(s) for " + session_id
        else:
            click_counts[session_id] = 0
            return str(0) + " click(s) for " + session_id
    else:
        global last_session_id
        last_session_id += 1
        click_counts[str(last_session_id)] = 0
        resp = make_response(str(0) + " click(s) for " + str(last_session_id))
        resp.set_cookie('sessionId', str(last_session_id))
        return resp 
    
app.config['SECRET_KEY'] = os.urandom(32)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

current_username = None

@app.route("/login", methods=['GET', 'POST'])
def login_function():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Log in requested for {form.username.data} with password {form.password.data}")
        global current_username
        current_username = form.username.data
        ## Add function here to check password
        return redirect("/home")
    return render_template("login.html", form=form)

@app.route("/home")
def home():
    return render_template("home.html", username=current_username)

if __name__ == '__main__':
    app.run()