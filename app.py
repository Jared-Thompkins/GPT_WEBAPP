from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from models import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import openai
from extensions import client, db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

# Tester 

try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection unsuccessful", e)

#Tester ^

def get_user(username):
    user_collection = db["users"]
    user = user_collection.find_one({"username": username})
    return user

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.get_by_username(form.username.data)
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(id=None, username=form.username.data, password=form.password.data)

        # Save the user to MongoDB
        new_user.save()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    temp_id = session.get("_user_id")
    user = User.get_by_id(temp_id)
    return user

# Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful.')
            return redirect(url_for('index'))

        else:
            flash('Login unsuccessful. Please check username and password.')
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('index'))

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        firstPart = request.form["firstPart"]
        animal = request.form["animal"]

        system_message = firstPart if firstPart else "You are a helpful assistant."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": generate_prompt(firstPart, animal)}
            ]
        )
        
        generated_response = response['choices'][0]['message']['content']
        formatted_response = format_paragraphs(generated_response)

        return redirect(url_for("index", result=formatted_response))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def format_paragraphs(text):
    paragraphs = text.split('\n')
    for i in range(len(paragraphs)):
        parts = paragraphs[i].split('**')
    for j in range(len(parts)):
        if j % 2 == 1: 
            parts[j] = f'<b>{parts[j]}</b>'
    paragraphs[i] = ''.join(parts)

    return '<p>' + '</p><p>'.join(paragraphs) + '</p>'


def generate_prompt(firstPart, animal):
    return f"{animal.capitalize()}"

if __name__ == "__main__":
    app.run(port=5000)