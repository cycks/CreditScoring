"""
Restructure.__init___.py

This file contains code for used to run the entire application. 


Note:
	1. The populate_status_roles is used to insert the very first
	   status and roles of a user or company registration.
	2. The populate admin is used to insert the first super_admin
	   who will be responsible for registering the first users of
	   the application. It also inserts the very first company in
	   the database.

Note:
	1. Flask cors is used to enables cross origin resource sharing
	2. Flask migrate is used to manage database migrations  
	3. hashing and db are imported here inorder to add the to the
	   app instance.
"""


import os


from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS


from Models.__init__ import db, hashing
from Models.others import populate_status_roles, populate_admin


app = Flask(__name__)
CORS(app, support_credentials=True)

migrate = Migrate(app, db)


def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://cycks:*cycks@Mysql.1899@localhost/development"
	app.config['SECRET_KEY'] = "ruiherf238429-4-23r-RT="
	app.config['DEBUG'] = False
	app.config['TESTING'] = False
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['CORS_HEADERS'] = 'Content-Type'
	with app.app_context():
		db.init_app(app)
		hashing.init_app(app)
		migrate.init_app(app)
		from Users.users import users_routes
		from Users.show_status import display_routes
		from Users.admin_checks import check_routes
		from Users.admin_approvals import approve_routes
		from Companies.corporate_approvals import company_routes
		from SentData.send_endpoints import send_data_routes
		app.register_blueprint(users_routes)
		app.register_blueprint(display_routes)
		app.register_blueprint(check_routes)
		app.register_blueprint(approve_routes)
		app.register_blueprint(company_routes)
		app.register_blueprint(send_data_routes)
		db.create_all()
		populate_status_roles()
		populate_admin()
	return app
