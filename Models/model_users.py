import datetime, json, jwt, os


from datetime import timedelta

from flask import request


from Helpers.admin_details import AdminDetails
from Helpers.input_validators import ValidInputs


from Models.__init__ import db, hashing
from Models.tables import (
									Administrators,
									BlacklistedTokens,
									ClientAdmins,
									Corporates,
									LoggedAdmins,
									LoggedClients,
									Users,
								)
from sqlalchemy import exc


def generate_jwt_token(admin_role, admin_status, admin_id, corporate_id):
	"""
	Generates a jwt authentication token.

	Args:
		admin_role (int): The first parameter.
		admin_status (int): The second parameter. A user's
							registration status
		admin_id (int): The database id for the user
		corporate_id (int): The corporate_id for the user
	
	Returns:
		A token(str)
	"""
	secret = "ruiherf238429-4-23r-RT="
	expiration = datetime.datetime.now() + timedelta(minutes=200)
	user_token = jwt.encode(
								{	
									'admin_role':admin_role,
									'admin_status':admin_status,
									'admin_id': admin_id,
									'corporate_id': corporate_id,
									'exp': expiration
								},
									secret
							)
	return user_token


class Authentication(AdminDetails):

	def __init__(self, required_role=None):
		self.required_role = required_role
		AdminDetails.__init__(self)

	def is_valid_data(self):
		"""
		Try to extract data from the request object. If the body is empty then
		check for cases where data is sent using variable rules. If that fails
		check to see whether there is a token in the request. Return False if
		all this checks fail.
		"""
		data = False
		try:
			data = json.loads(request.get_data())
			if data is None:
				if len(request.view_args) > 0:
					data = request.view_args
					return True
				elif request.headers.get("user_token"):
					return True	
			return True	
		except json.decoder.JSONDecodeError as e:
			return data

	def is_logged_in(self):
		logged_in_admin = super().get_admin_id
		if logged_in_admin:
			return logged_in_admin
		else:
			return False

	def is_valid_token(self):
		admin_id = self.is_logged_in()
		token = super().get_user_token
		checked_token = BlacklistedTokens().get_by_token(token)
		if admin_id == False:
			return False
		if checked_token != None:
			return False
		return True

	def is_valid_role(self):
		"""
		Make all other validations then check if the required role
		is less than or equal to the current role.
		"""
		admin_role = super().get_admin_role
		if admin_role <= self.required_role:
			return admin_role
		else:
			return False


	# def make_validation(self):
	# 	all_validations = True
	# 	validate_data = self.is_valid_data()
	# 	if validate_data == False:
	# 		return {"status": False, "message": "The data is invalid."}
	# 	check_log_status = self.is_logged_in()
	# 	elif check_log_status == False:
	# 		return {"status": False, "message": "Log in first."}
	# 	check_valid_token = self.is_valid_token()
	# 	elif check_valid_token == False:
	# 		return {"status": False, "message": "Invalid token. Log in first."}
	# 	validate_role = self.is_valid_role()
	# 	elif validate_role == False:
	# 		return {"status": False, "message": "Unauthorised."}
	# 	return True



class CreatedUsers(ValidInputs):
	"""docstring for CreatedUsers"""
	def __init__(self, mydict, required_inputs):
		ValidInputs.__init__(self, required_inputs)
		self.mydict = mydict


	def is_correct_details(self):
		return super().produce_output(self.mydict)

	def is_registered_corporate(self):
		return Corporates().get_corp_by_name(self.mydict["corporate_name"])

	def is_registered_user(self):
		return Users().get_by_user_identity(self.mydict["user_identity"])

	def register_user(self):
		ed_user = Users(
							user_identity=self.mydict["user_identity"],
							user_names=self.mydict["admin_names"]
						)
		db.session.add(ed_user)
		db.session.commit()
		return True
		
	def register_admin(self, admin_role, user_id, secret):
		# TODO: Check for duplicate emails
		email = Administrators().get_admin_by_email(self.mydict["admin_email"])
		corp = Corporates().get_corp_by_name(self.mydict["corporate_name"])
		if email != None:
			return  {
						"status": False,
						"message": "email taken"
					}
		if corp == None:
			return  {
						"status": False,
						"message": "Company provided is unregistered."
					}
		hashed = hashing.hash_value(self.mydict["admin_password"], salt=secret)
		if admin_role >= 3:
			return  {
						"status": False,
						"message": "Wrong role provided."
					}
		elif admin_role <= 2:
			ed_user = Administrators(
										admin_email=self.mydict["admin_email"],
										admin_password=hashed,
										role_id = admin_role,
										status_id = 1,
										user_id = user_id
									)
			db.session.add(ed_user)
			db.session.commit()
			return  {
						"status": True,
						"message": "administrator registered."
					}
		else:
			return False


	def register_client(self, admin_role, user_id, secret):
		email = ClientAdmins().get_client_by_email(self.mydict["admin_email"])
		corp = Corporates().get_corp_by_name(self.mydict["corporate_name"])
		if email != None:
			return  {
						"status": False,
						"message": "email taken"
					}
		if corp == None:
			return  {
						"status": False,
						"message": "Company provided is unregistered."
					}
		hashed = hashing.hash_value(self.mydict["admin_password"], salt=secret)
		if admin_role <= 2:
			return {
						"status": False,
						"message": "Wrong role provided should be a client role."
					}
		elif admin_role <= 4:
			ed_user = ClientAdmins(
									client_email=self.mydict["admin_email"],
									client_password=hashed,
									role_id = admin_role,
									status_id = 1,
									user_id = user_id,
									corporate_id = corp.corporate_id
								 )
			db.session.add(ed_user)
			db.session.commit()
			return  {
						"status": True,
						"message": "client registered."
					}
		else:
			return False

	def make_registration(self, secret):
		if self.is_correct_details() != True:
			return self.is_correct_details()
		# check if is_registered_corporate is none and return message
		if self.is_registered_corporate() == None:
			return  {
						"status": False,
						"message": "unregistered company."
					}
		# check if user is in Users table and register if none
		is_registered_user = self.is_registered_user()
		if is_registered_user == None:
			self.register_user()
		"""
		If none in the db the first time above fetch again after registration
		"""
		is_registered_user = self.is_registered_user()
		admin_role = super().get_role_id(self.mydict["admin_role"])
		# extract user id from the users table
		user_id = is_registered_user.user_id
		if admin_role == 1 or admin_role == 2:
			reg_status = self.register_admin(admin_role, user_id, secret)
			return reg_status
		if admin_role == 3 or admin_role == 4:
			reg_status = self.register_client(admin_role, user_id, secret)
			return reg_status


def save_admins(mydict, secret):
	"""
	Saves a user into the user table, administrators, or clientadmins tables.

	Using the CreatedUsers class to register a user, then an admin, then
	a client admin.
	"""

	required_inputs = ["user_identity", "admin_names", "admin_email", 
						"admin_password", "admin_role", "corporate_name"]

	registration = CreatedUsers(mydict, required_inputs)
	registration_status = registration.make_registration(secret)
	return registration_status


class LoggedUsers(ValidInputs):
	"""docstring for CreatedUsers"""
	def __init__(self, mydict, required_inputs=None):
		ValidInputs.__init__(self, required_inputs)
		self.mydict = mydict

	def is_correct_details(self):
		return super().produce_output(self.mydict)

	def is_registered_admin(self):
		return Administrators().get_admin_by_email(self.mydict["admin_email"])

	def is_registered_client(self):
		return ClientAdmins().get_client_by_email

	def is_correct_password(self, db_password):
		recieved_password = self.mydict["password1"]
		check_password = hashing.check_value(
												db_password,
												recieved_password,
												salt="ruiherf238429-4-23r-RT="
											)
		return check_password

	def generate_token(self, sql_query):
		user_token =  generate_jwt_token(
											sql_query.role_id,
											sql_query.status_id,
											sql_query.admin_id,
											sql_query.corporate_id
										)
		return user_token

	def insert_logged_admin(self, admin_id):
		ed_user = LoggedAdmins(admin_id=admin_id)
		try:
			db.session.add(ed_user)
			db.session.commit()
			return True
		except:
			return False

	def log_in_admin(self):
		is_valid_inputs = super().produce_output(self.mydict)

		if is_valid_inputs != True:
			return {
						"status": False,
						"message": is_valid_inputs
					}

		# TODO consider checking if the generated token is in the blacklist
		reg_status = self.is_registered_admin()
		if reg_status == None:
			return {
						"status": False,
						"message":"unregistered email"
					}

		db_password = reg_status.admin_password
		is_correct_password = self.is_correct_password(db_password)
		admin_id = reg_status.admin_id

		if is_correct_password == False:
			return {
						"status": False,
						"message": "incorrect password provided"
					}

		is_approved_admin = reg_status.status_id
		if is_approved_admin != 2:
			return {
						"status": False,
						"message": """Contact your immediate supervisor
									for approval"""
					}


		user_token = self.generate_token(reg_status).decode("utf-8")
		if self.insert_logged_admin(admin_id) == True:
			return {	
						"status": True, 
						"message": "login successful",
						"token": user_token,
						"role_id": reg_status.role_id
					}
		elif self.insert_logged_admin(admin_id) == False:
			return  {
						"status": False, 
						"message": "Error on login"}

	def insert_logged_client(self, client_id):
		ed_user = LoggedClients(client_id=client_id)
		try:
			db.session.add(ed_user)
			db.commit()
			return True
		except:
			return False

	def log_in_client(self):
		is_valid_inputs = super().produce_output(self.mydict)
		if is_valid_inputs != True:
			return {
						"status": False,
						"message":is_valid_inputs
					}
		# TODO consider checking if the generated token is in the blacklist
		reg_status = self.is_registered_client()
		if reg_status == None:
			return {
						"status": False,
						"message":"unregistered email"
					}

		db_password = reg_status.admin_password
		is_correct_password = self.is_correct_password(db_password)
		admin_id = reg_status.admin_id

		if is_correct_password == False:
			return {
						"status": False,
						"message": "incorrect password provided"
					}

		is_approved_admin = reg_status.status_id
		if is_approved_admin != 2:
			return {
						"status": False, 
						"message": "Contact your supervisor for approval"
					}

		user_token = self.generate_token(reg_status).decode("utf-8")
		if self.insert_logged_client(admin_id) == True:
			return {
						"status": True, 
						"message": "login successful.",
						"token": user_token,
						"role_id": reg_status.role_id
					}
		elif self.insert_logged_client(admin_id) == False:
			return {"status": False, "message": "Error on login"}

	def blacklist_token(self, token):
		"""
		used to blacklist tokens that have not expired but are still valid.
		"""
		ed_user = BlacklistedTokens(token=token)
		db.session.add(ed_user)
		db.session.commit()
		return True

	def update_logs(self, role_id, admin_id):
		"""
		"""
		if admin_id == None or role_id == None:
			return False
		if role_id == 1 or role_id == 2:
			login = (
					  db.session.query(LoggedAdmins).
					  filter(LoggedAdmins.admin_id == admin_id).				
					  order_by(LoggedAdmins.admin_id.desc()).first()
					)
		elif role_id == 3 or role_id == 4:
			login = (
					  db.session.query(LoggedClients).
					  filter(LoggedClients.admin_id == admin_id).				
					  order_by(LoggedClients.admin_id.desc()).first()
					)
		else:
			return False
		try:
			login.logoutDate = datetime.datetime.now()
			db.session.commit()
			return True
		except AttributeError as error_message:
			db.session.rollback()
			return False

	def logout(self):
		"""
		On loguout update the LoggedAdmins and the LoggedClients
		column (logout date to the current time.) If the token is still valid
		insert the token in blacklisted tokens.
		"""
		# TODO check if the token is in the blacklisted table
		
		login_status = self.update_logs(
											self.mydict["role_id"],
											self.mydict["admin_id"]
										)
		if login_status == True:
			try:
				secret = "ruiherf238429-4-23r-RT="
				decoded_token = jwt.decode(self.mydict["user_token"], secret)
				self.blacklist_token(self.mydict["user_token"])
				return {
							"status": True,
							"messge": "Logged out successfully."
						}
			except jwt.exceptions.ExpiredSignatureError:
				return {
							"status": True,
							"message": "expired session."
						}
		elif login_status == False:
			return {
							"status": False,
							"message": "You were not logged in."
						}