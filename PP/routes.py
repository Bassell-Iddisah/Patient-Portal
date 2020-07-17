from PP import app
from flask import url_for, redirect, render_template, flash, request
from flask_login import current_user, login_user, logout_user


@app.route('/')
def home():
    return 'Hello World!'
