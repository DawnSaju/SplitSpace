from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import requests
import os

app = Flask(__name__, static_url_path='/static')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
# postgres://sustainai_user:ZkQFwvwmYHTYd6lAatYA5TJle4Bx16BD@dpg-ckrqd5prfc9c738oau80-a.oregon-postgres.render.com/sustainai
app.config['SECRET_KEY'] = "TEST1233444222"

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
blueprint_login_views = {
    'roommate': 'roommate.roommate_signin',
    'family_member': 'family_member.familyMember_signin',
    'admin': 'admin.admin_signin',
}
@app.errorhandler(404)
def page_not_found(e):
    return 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('home.html')

from app import routes