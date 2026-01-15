from sqlalchemy import inspect


from Models.__init__ import db



from Models.tables import (
									AdminChecks,
									Administrators,
									ClientAdmins,
									CorporateChecks,
									Corporates,
									Roles,
									Status,
									Users
								)

def object_as_dict(obj):
	"""
	This function is used to convert an sqlalchemy query from a
	list to a dictionary.
	"""
	return {c.key: getattr(obj, c.key)
			for c in inspect(obj).mapper.column_attrs}






def admin_last_status(user_id):
	"""
	This function is best used without commiting the session
	becuase it is later committed in the DisplayedApprovals
	class found in the displays module.
	"""
	sql_query = (
					db.session.query(AdminChecks).
					filter(AdminChecks.client_being_checked==user_id).
					order_by(AdminChecks.check_id.desc()).first()
				)
	convert_to_dict = object_as_dict(sql_query)
	return convert_to_dict


def corp_last_status(corp_id):
	"""
	This function is best used without commiting the session
	becuase it is later committed in the DisplayedApprovals
	class found in the displays module.
	"""
	# print("The corporate id is :", corp_id)
	sql_query = (
					db.session.query(CorporateChecks).
					filter(CorporateChecks.corp_being_checked==corp_id).
					order_by(CorporateChecks.check_id.desc()).first()
				)
	convert_to_dict = object_as_dict(sql_query)
	return convert_to_dict



def last_admin_status(current_answer, required_data=[]):
	if len(current_answer) >= 1:
		for person in current_answer:
			person_id = person['user_id']
			recent_status = admin_last_status(person_id)["checked_from"]
			last_status = status_function(recent_status).status_name
			person['status_name'] = last_status
			required_data.append(person)
		db.session.commit()
	return required_data


def last_corp_status(current_answer, required_data=[]):
	if len(current_answer) >= 1:
		for corporate in current_answer:
			corporate_id = corporate['corporate_id']
			recent_status = corp_last_status(corporate_id)["checked_from"]
			last_status = status_function(recent_status).status_name
			corporate['status_name'] = last_status
			required_data.append(corporate)
		db.session.commit()
	return required_data

# Functions used to commit changes to the database when for loop ends
def user_function(user_id):
	sql_query = (db.session.query(Users).
					filter(Users.user_id==user_id).first())
	return sql_query

def status_function(status_id):
	sql_query = (db.session.query(Status).
					filter(Status.status_id==status_id).first())
	return sql_query

def role_function(role_id):
	sql_query = (db.session.query(Roles).
					filter(Roles.role_id==role_id).first())
	return sql_query

def corp_function(corporate_name):
	sql_query = (db.session.query(Corporates).
					filter(Corporates.corporate_name==corporate_name).first())
	return sql_query

def corp_function2(corp_id):
	sql_query = (db.session.query(Corporates).
					filter(Corporates.corporate_id==corp_id).first())
	return sql_query

def admin_function(admin_id):
	sql_query = (db.session.query(Administrators).
					filter(Administrators.admin_id==admin_id).first())
	return sql_query


class DetailsFromQuery():
	
	def is_valid_fetch(self, type_of_fetch):
		valid_fetches = ["administrators", "clients", "corporates"] 
		if self.type_of_fetch not in valid_fetches:
			return False
		return True

	def create_user(self, sql_query):
		admin_displays = []

		if sql_query == None:
			return None
		for item in sql_query:
			all_details = {}
			the_item = item.__dict__
			try:
				the_email = the_item["admin_email"]
			except KeyError:
				the_email = the_item["client_email"]
			user_details = user_function(the_item["user_id"])
			user_names = user_details.user_names
			user_identity = user_details.user_identity
			user_id = user_details.user_id
			corp_name = corp_function2(the_item["corporate_id"]).corporate_name
			status_name = status_function(the_item["status_id"]).status_name
			role_name =role_function(the_item["role_id"]).role_name
			user_email = the_email
			all_details["user_names"] = user_names
			all_details["user_identity"] = user_identity
			all_details["user_id"] = user_id
			all_details["status_name"] = status_name
			all_details["role_name"] = role_name
			all_details["user_email"] = user_email
			all_details["corporate_name"] = corp_name
			admin_displays.append(all_details)
		db.session.commit()
		return admin_displays


	def create_corp_details(self, sql_query):
		admin_displays = []
		if sql_query == None:
			return None
		for item in sql_query:
			all_details = {}
			item = item.__dict__
			corp_name = corp_function(item["corporate_name"]).corporate_name
			corporate_pin = corp_function(item["corporate_name"]).corporate_pin
			corporate_id = corp_function(item["corporate_name"]).corporate_id
			all_details["corporate_name"] = corp_name
			all_details["corporate_pin"] = corporate_pin
			all_details["corporate_id"] = corporate_id
			admin_displays.append(all_details)
		db.session.commit()
		return admin_displays

	def create_payments(self, sql_query):
		admin_displays = []
		if sql_query == None:
			return None
		for item in sql_query:
			all_details = {}
			item = item.__dict__
			corp_details = corp_function2(item["corporate_id"])
			corp_names = corp_details.corporate_name
			payment_amount = item["payment_amount"]
			admin =admin_function(item["admin_id"])
			user_names = user_function(admin.user_id).user_names
			all_details["user_names"] = user_names
			all_details["corporate_name"] = corporate_name
			all_details["payment_amount"] = payment_amount
			admin_displays.append(all_details)
		db.session.commit()
		return admin_displays


class DisplayedChecks(DetailsFromQuery):
	"""A superadmin can fetch corporate checks, infotrace_staff checks,
	and client_admin checks super_admin checks"""

	def __init__(self, type_of_fetch, role_id, corp_id=None):
		self.type_of_fetch = type_of_fetch
		self.role_id = role_id
		self.corp_id = corp_id

	def fetch_superadmin_admin_checks(self):
		try:
			fetch_admins = 	(
								db.session.query(Administrators).
								filter(
										Administrators.status_id == 1,
										Administrators.role_id <= 2
										).all()
							)
			return super().create_user(fetch_admins)
		except:
			db.session().rollback()

	def fetch_superadmin_client_checks(self):
		try:
			fetch_clients = (
								db.session.query(ClientAdmins).
								filter(
										ClientAdmins.status_id == 1,
										ClientAdmins.role_id == 3
										).all()
							)
			return super().create_user(fetch_clients)
		except:
			db.session().rollback()

	def fetch_infotrace_admin_checks(self):
		try:
			fetch_admins = 	(
								db.session.query(Administrators).
								filter(
										Administrators.status_id == 1,
										Administrators.role_id == 2
										).all()
							)
			return super().create_user(fetch_admins)
		except:
			db.session().rollback()

	def fetch_infotrace_client_checks(self):
		try:
			fetch_client = 	(
								db.session.query(ClientAdmins).
								filter(
										ClientAdmins.status_id == 1,
										ClientAdmins.role_id == 3
										).all()
							)
			return super().create_user(fetch_clients)
		except:
			db.session().rollback()

	def fetch_client_admin_checks(self):
		try:
			fetch_clients = (
								db.session.query(ClientAdmins).
								filter(
										ClientAdmins.status_id == 1,
										ClientAdmins.role_id >= 4,
										ClientAdmins.corporate_id == self.corp_id
										).all()
								)
			clients = super().create_user(fetch_clients)
			return clients
		except:
			db.session().rollback()

	def fetch_corporates(self):
		try:
			fetch_corps = 	(
								db.session.query(Corporates).
								filter(Corporates.status_id == 1).all()
							)
			corporates = super().create_corp_details(fetch_corps)
			return corporates
		except:
			db.session().rollback()

	def make_a_check_fetch(self):
		if super().is_valid_fetch(self.type_of_fetch) != True:
			return "wrong type of fetch provided"
		if self.type_of_fetch == "administrators" and self.role_id == 1:
			return self.fetch_superadmin_admin_checks()
		elif self.type_of_fetch == "clients" and self.role_id == 1:
			return self.fetch_superadmin_client_checks()
		elif self.type_of_fetch == "administrators" and self.role_id == 2:
			return self.fetch_infotrace_admin_checks()
		elif self.type_of_fetch == "clients" and self.role_id == 2:
			return self.fetch_superadmin_client_checks()
		elif self.type_of_fetch == "clients" and self.role_id == 3:
			return self.fetch_client_admin_checks(self.corporate_id)
		elif self.type_of_fetch == "corporates" and self.role_id <= 2:
			return self.fetch_corporates()


class DisplayedApprovals(DetailsFromQuery):
	"""
	The status name should not indicate the current status. Instead, it should
	indicate the previous status.
	"""
	
	def __init__(self, type_of_fetch, role_id, corporate_id=None):
		self.type_of_fetch = type_of_fetch
		self.role_id = role_id
		self.corporate_id = corporate_id

	def fetch_superadmin_admin_approvals(self):
		try:
			fetch_admins = (
								db.session.query(Administrators).
								filter(
										Administrators.status_id == 7,
										Administrators.role_id <= 2
									  ).all()
								)
			
			current_answer = super().create_user(fetch_admins)
			# Fetch the recent status as checked_from in the AdminChecks table
			last_status_from_AdminChecks = last_admin_status(current_answer)
			return last_status_from_AdminChecks
		except:
			db.session().rollback()

	def fetch_superadmin_client_approvals(self):
		try:
			fetch_clients = (
								db.session.query(ClientAdmins).
								filter(
										ClientAdmins.status_id == 7,
										ClientAdmins.role_id <= 2
									   ).all()
							)
			current_answer = super().create_user(fetch_clients)
			# Fetch the recent status as checked_from in the AdminChecks table
			last_status_from_AdminChecks = last_admin_status(current_answer)
			return last_status_from_AdminChecks
		except:
			db.session().rollback()


	def fetch_superadmin_corp_approvals(self):		
		try:
			fetch_corps = (
							db.session.query(Corporates).
							filter(
									Corporates.status_id == 7
								  ).all()
						  )
			current_answer = super().create_corp_details(fetch_corps)
			# Fetch the recent status as checked_from in the AdminChecks table
			last_status_from_CorpChecks = last_corp_status(current_answer)
			return last_status_from_CorpChecks
			
		except Exception as e:
			db.session().rollback()


	def fetch_superadmin_pay_approvals(self):
		try:
			payment_result = (
								db.session.query(ClientPayments).
								filter(
											ClientPayments.uploaded_by != None,
											ClientPayments.approved_by == None
									   ).all()
							 )
			return super().create_payments(payment_result)
		except:
			db.session().rollback()


	def fetch_client_admin_approvals(self):
		try:
			fetch_result = (
							db.session.query(ClientAdmins).
							filter(
									ClientAdmins.status_id == 7,
									ClientAdmins.role_id == 4,
									ClientAdmins.corporate_id == self.corp_id
								).all()
							)
			current_answer = super().create_user_details(fetch_result)
			# Fetch the recent status as checked_from in the AdminChecks table
			last_status_from_AdminChecks = last_admin_status(current_answer)
			return last_status_from_AdminChecks
		except:
			db.session().rollback()
	
	def make_an_approval_fetch(self):
		if super().is_valid_fetch(self.type_of_fetch) != True:
			return "wrong type of fetch provided"
		if self.type_of_fetch == "administrators" and self.role_id == 1:
			return self.fetch_superadmin_admin_approvals()
		elif self.type_of_fetch == "clients" and self.role_id == 1:
			return self.fetch_superadmin_client_approvals()
		elif self.type_of_fetch == "corporates" and self.role_id == 1:
			return self.fetch_superadmin_corp_approvals()
		elif self.type_of_fetch == "payments" and self.role_id == 1:
			return self.fetch_superadmin_pay_approvals()
		elif self.type_of_fetch == "clients" and self.role_id == 3:
			return self.fetch_client_admin_approvals(self.corporate_id)
		elif self.type_of_fetch == "corporates" and self.role_id <= 2:
			return self.fetch_corporates()
