import os

from sqlalchemy import exc

from Models.__init__ import db, hashing
from Models.tables import (
									Administrators, 
									Borrowers,
									Corporates,
									LoggedAdmins,
									Roles,
									ScoreTypes,
									Status,
									Users
								)


def populate_status_roles():
	"""
	Populates the main tables on startup.
	
	Don't ever change the order of the two lists below.
	Given a list of roles populate the Roles table.
	Given a list of status populate the Status table.
	Given a list of type of scores, populate the ScoreTypes table.
	
	Args:
		None
	Returns:
		None
	
	"""
	all_roles = ["super_admin", "infotrace_admin", "client_admin", 
					"client_staff"]
	all_status = ["awaiting_approval", "approved", "dormant", "blocked", 
					"decision_rescinded", "to_be_checked",  "checked" ]
	all_services = {"premium": 100, "basic": 50}

	roles_check = db.session.query(Roles).first()
	if roles_check is None:
		for item in all_roles:
			try:
				insert_item = Roles(role_name = item)
				db.session.add(insert_item)
				db.session.commit()
			except:
				db.session.rollback()
	status_check = db.session.query(Status).first()
	if status_check is None:
		for item in all_status:
			try:
				insert_item = Status(status_name = item)
				db.session.add(insert_item)
				db.session.commit()
			except:
				db.session.rollback()
	service_check = db.session.query(ScoreTypes).first()
	if service_check is None:
		for key, value in all_services.items():
			try:
				insert_item = ScoreTypes(score_name=key, cost_of_score=value)
				db.session.add(insert_item)
				db.session.commit()
			except:
				db.session.rollback()
	return None


def check_corp_by_name(corporate_name):
	"""
	Validates a company by name.

	Given a corporate name check if the name is in the Corporates
	table. If true, return the corporate_id for the given company.
	if False rollback and return False.

	Args:
		corporate_name (str): The name of the company
	Returns:
		corporate_id (int): The corporate_id of the company
		bool: False If the company is not registered.
	"""

	is_registered = False
	try:
		is_registered = (
						   db.session.query(Corporates).
						   filter(Corporates.corporate_name==corporate_name).
						   first()
						)
		db.session.commit()
	except:
		db.session.rollback()
	if is_registered:
		return is_registered.corporate_id
	else:
		return is_registered



def check_corp_by_id(corporate_id):
	"""
	Validates a company by corporate_id.

	Given a corporate id check if the name is in the Corporates
	table. If true, return the corporate_id for the given company.
	if False rollback and return False.

	Args:
		corporate_id (int): The name of the company
	Returns:
		corporate_id (int): The corporate_id of the company
		bool: False If the company is not registered.
	"""
	is_registered = False
	try:
		is_registered = (
						   db.session.query(Corporates).
						   filter(Corporates.corporate_id==corporate_id).
						   first()
						)
		db.session.commit()
	except:
		db.session.rollback()
	if is_registered:
		return is_registered.corporate_id
	else:
		return is_registered
	


def check_score_type(score_name):
	"""
	Checks the database tables for correct names.

	Given a score name check if the score is in the ScoreTypes
	table. 
	
	Args:
		score_name (str): The name of the score correct
	
	Returns:
		obj: Sqlalchemy query object.

	"""
	
	is_correct_score = None
	try:
		is_correct_score = (
							db.session.query(ScoreTypes).
							filter(ScoreTypes.score_name == score_name).
							first()
						)
		db.session.commit()
	except:
		db.session.rollback()
	return is_correct_score
	
	

################################################################################


def check_borrower(borrower_by_identity):
	"""
	Validate if a single borrower is registered in the table.

	Helper function used in the push_kyc_to_db function to check if a
	borrower_id is in the Borrowers table and return True if that is the
	case and False otherwise.

	Args:
		borrower_identity (int): self explanatory.

	Returns:
		bool: True if the borrower is registered false otherwise.

	"""
	user = False
	try:
		user = Borrowers().borrower_by_identity(borrower_by_identity)
		db.session.commit()
	except:
		db.session.rollback()
	if user:
		return True
	return False



def confirm_registred_corporates(data):
	"""
	Validates a list of Corporates.

	Used in all functions that send transactional data to the
	db to confirm whether corporates in the entire data set are
	all registered.

	Args:
		data(:obj:`json`):  data sent by the request
	Returns:
		list: An empty list if all corporates are registered.
			  A list of unregistered corporates otherwise.

	"""
	list_of_corporates = data['corporate_id']
	not_registered = []
	for corporate in list_of_corporates:
		try:
			registered_corporate = Corporates.query.get(corporate)
		except:
			db.session.rollback()
		if not registered_corporate:
			not_registered.append(corporate)
	db.session.commit()
	return not_registered
	

def confirm_registered_borrower(data):
	"""
	Validates a list of borrowers.

	Used in all functions that send transactional data to the
	db to confirm whether all borrowere in the entire data set
	are all registered.

	Args:
		data(:obj:`json`):  data sent by the request
	Returns:
		list: An empty list if all borrowers are registered.
			  A list of unregistered borrowers otherwise.
	"""
	list_of_borrowers = data["borrower_identity"]
	not_registered = []
	for borrower in list_of_borrowers:
		try:
			registered_borrower = Borrowers().borrower_by_id
			db.session.commit()
		except:
			db.session.rollback()
		if not registered_borrower:
			not_registered.append(borrower)
	db.session.commit()
	return not_registered
	


def save_company_details(mydict, admin_id):
	"""
	Saves company details to the database.

	Given a dictionary containing the corporate details, confirm
	that the company is not already registered. If the company is
	registered return a string indicating the same. If the company
	name is not register the company.

	Args:
		mydict (dict): A dictionary with company details
		user_identity (int): The user_identity for the person registering
						the company.

	Returns:
		bool: Returns True if the registration is ok.
		str: If the company name is taken.
	"""
	corp_name = mydict["corporate_name"]
	try:
		is_registered_corp = (
								db.session.query(Corporates).
								filter(Corporates.corporate_name==corp_name).
								first()
							  )
		if is_registered_corp == None:
			ed_user = Corporates(
									corporate_name =corp_name,
									corporate_pin = mydict["corporate_pin"],
									status_id = 1,
									created_by = admin_id
								)		
			db.session.add(ed_user)
			db.session.commit()
			return True
	except exc.IntegrityError as e:
		db.session.rollback()
		return False
	else:
		db.session.rollback()
		return "Company already registered."


def populate_admin():
	"""
	Insert the first super admin in the db.

	used in the __init__ of the main application on app start up.
	Using default details provided in the function hash the password
	and check if the Users table is empty. If so, insert the
	user in the User and Administrators table. Also populates the 
	first company in the Corporates table.

	Note:
		Always remember to use a good password here.
	
	Args:
		None
	Returns:
		bool: Returns True 
	"""
	password = hashing.hash_value(
									"password", 
									salt="ruiherf238429-4-23r-RT="
								 )
	admin_names = "Wycliffe Sikolia"
	admin_email = "sikolia.wycliffe100@gmail.com"
	user_identity = 27813100
	user_check = db.session.query(Users).first()
	try:
		if user_check is None:
			insert_item = Users(
									user_identity=user_identity,
									user_names=admin_names
								)
			db.session.add(insert_item)
			db.session.commit()
	except:
		db.session.rollback()
	admin_check = db.session.query(Administrators).first()
	try:
		if admin_check is None:
			insert_item = Administrators(admin_email=admin_email,
										 admin_password=password,
										 role_id=1, status_id=2, user_id=1,
										 corporate_id=1)
			db.session.add(insert_item)
			db.session.commit()
	except:
		db.session.rollback()
	corporate_check = db.session.query(Corporates).first()
	try:
		if corporate_check is None:
			insert_item = Corporates(corporate_pin="Info1234", created_by=1,
									 corporate_name="InfoTrace Analytics", 
									 status_id=2)
			db.session.add(insert_item)
			db.session.commit()
		return True
	except:
		db.session.rollback()
	return True


