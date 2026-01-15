"""
This module contains classes used to make checks and
approvals. Contains the following classes.
	1. Checks: used for making all checks
	2. Approvals: Used for making all approvals.
"""



from Models.__init__ import db

from Helpers.input_validators import ValidInputs


from Models.tables import (
							AdminApprovals,
							AdminChecks,
							Administrators,
							ClientAdmins,
							CorporateApprovals,
							CorporateChecks,
							Corporates,
							Status
							)

class Checks(ValidInputs):
	"""
	A class used for making checks.

	Inherits from the ValidInputs class which is used here
	to ensure that the inputs provided in mydict are of
	valid types and names.
	

	Attributes:
        mydict (dict): A dictionary containing all inputs provided
        by the  user.

        required_inputs (list): A list containing the inputs required
        for a given check.
    """
	def __init__(self, mydict, required_inputs=None):
		ValidInputs.__init__(self, required_inputs)
		self.mydict = mydict
	
	def is_correct_details(self):
		"""
		Validates inputs.

		Confirms that all the required_iputs are present and are of 
		valid type.
		"""
		return super().produce_output(self.mydict)

	def is_registered_admin(self):
		"""Query the Administrators by their email address"""
		return Administrators().get_admin_by_email(self.mydict["admin_email"])

	def is_registered_client(self):
		"""Query the clients by their email address"""
		return ClientAdmins().get_client_by_email(self.mydict["admin_email"])

	def is_registered_corporate(self):
		"""Query the companies by their corporate name"""
		return Corporates().get_corp_by_name(self.mydict["corporate_name"])

	def check_dual_registration(self):
		"""
		Validates that a user cannot register as an admin and  as a client.

		If a user is registered as an administratorr, checks if the same
		user(email adress) is registered as a client. If so, return an error
		message indicating the case. Otherwise return an sqlalchemy querry
		object for an administrator or client. If all the tests fail then
		return unregisterd email.

		Args:
			None

		Returns:
			Error message (str): Dual registration error.
			sqlalcehmy object (obj): An sqlalcehmy object
			unregistrered email (str): Unregistered email.

		"""
		admin_status = self.is_registered_admin()
		client_status = self.is_registered_client()

		if admin_status != None and client_status != None:
			return "Dual registration error."
		elif admin_status != None:
			return admin_status
		elif client_status != None:
			return client_status
		else:
			return "Unregistered email. Please register the user first."


	def update_admins_on_check(self):
		"""
		Helper function used to change the checked status in the Administrators
		table.
		"""
		try:
			(
			  db.session.query(Administrators).
			  filter(Administrators.admin_email == self.mydict["admin_email"]).
			  update({Administrators.status_id: 7})
			)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			return False

	def update_clients_on_check(self):
		"""
		Helper function used to change the checked status in the ClientAdminis
		table.
		"""
		try:
			(
				db.session.query(ClientAdmins).
				filter(ClientAdmins.client_email == self.mydict["admin_email"]).
				update({ClientAdmins.status_id: 7})
			)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			return False


	def check_admin(self):
		"""
		checker_id: The id of the person doing the checking
		checked_id: The id of the persron being checked
		"""
		is_valid_inputs = super().produce_output(self.mydict)
		if is_valid_inputs != True:
			return {
						"status": False,
						"message": is_valid_inputs
					}
		current_status = self.check_dual_registration()
		if isinstance(current_status, str):
			return {
						"status": False,
						"message": current_status
					}

		checked_id = current_status.user_id
		role_id = current_status.role_id
		has_been_checked = current_status.status_id

		# Extract the status id using a method inherited from ValidInputs
		checked_from = super().get_status_id(self.mydict["checked_from"])
		checked_to = super().get_status_id(self.mydict["checked_to"])

		if has_been_checked == 7:
			return {
						"status": False,
						"message": "Already checked."
					}
		if has_been_checked == 2:
			return {
						"status":False,
						"message":"Already checked and approved."
					}
		if has_been_checked != 7:
			check = AdminChecks(
									client_being_checked = checked_id,
									checker_id = self.mydict["checker_id"],
									checked_from = checked_from,
									checked_to = checked_to
								)
			if role_id <= 2:
				updated_status = self.update_admins_on_check()
			if role_id == 3 or role_id == 4:				
				updated_status = self.update_clients_on_check()
			if updated_status == True:
				db.session.add(check)
				db.session.commit()
				return {
							"status": True,
							"message":"successfully checked."
						}
			else:
				db.session().rollback()
				return {
							"status": False,
				 			"message": "Administrators table not checked."
				 		}
		else:
			db.session().rollback()
			return {
						"status":False,
						"message": "For some reason the check was not completed"
				   }


	def update_corp_on_check(self):
		"""
		Query the database for a company with the provided corporate_name,
		and update the status_id, the person doing the checking and the
		in the table the date and time as the current time.

		Corporates.checked_by: checker_id,
		Corporates.corporate_date_checked: current_time

		"""
		try:
			(
			  db.session.query(Corporates).
			  filter(Corporates.corporate_name == self.mydict["corporate_name"]).
			  update({Corporates.status_id: 7})
			)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			return False

	def check_company(self):
		"""
		
		approver_id: The id of the person doing the aproval
		approved_id: The id of the persron being approved.
		"""
		is_valid_inputs = super().produce_output(self.mydict)
		if is_valid_inputs != True:
			return {
						"status": False,
						"message":is_valid_inputs
					}

		current_status = self.is_registered_corporate()
		if current_status is None:
			return {
						"status": False,
						"message": current_status
					}

		has_been_checked = current_status.status_id
		corporate_id = current_status.corporate_id
		corp_name = current_status.corporate_name

		# Extract the status id using a method inherited from ValidInputs
		checked_from = super().get_status_id(self.mydict["checked_from"])
		checked_to = super().get_status_id(self.mydict["checked_to"])
		
		if has_been_checked == 7:
			return 	{
						"status": False,
						"message": "Already checked."
					}
		if has_been_checked == 2:
			return {
						"status": False,
						"message": "Already checked and approved."
					}
		if has_been_checked != 7:
			check = CorporateChecks(
										corp_being_checked = corporate_id,
										checker_id = self.mydict["checker_id"],
										checked_from = checked_from,
										checked_to = checked_to
									)
			updated_status = self.update_corp_on_check()
			if updated_status == True:
				db.session.add(check)
				db.session.commit()
				return {
							"status": True,
							"message": "Corporate successfully checked."
						}
			else:
				db.session().rollback()
				return {
							"status": False,
							"message": "Corporate not updated to checked."
						}
				
		else:
			db.session().rollback()
			return {
						"status": False,
						"message": "For a reason the check was not completed."
					}


class Approvals(ValidInputs):
	"""docstring for CreatedUsers"""
	def __init__(self, mydict, required_inputs=None):
		ValidInputs.__init__(self, required_inputs)
		self.mydict = mydict
	
	def is_correct_details(self):
		return super().produce_output(self.mydict)

	def is_registered_admin(self):
		return Administrators().get_admin_by_email(self.mydict["admin_email"])

	def is_registered_client(self):
		return ClientAdmins().get_client_by_email(self.mydict["admin_email"])

	def is_registered_corporate(self):
		return Corporates().get_corp_by_name(self.mydict["corporate_name"])

	def check_dual_registration(self):
		admin_status = self.is_registered_admin()
		client_status = self.is_registered_client()

		if admin_status != None and client_status != None:
			return "Dual registration error."
		elif admin_status != None:
			return admin_status
		elif client_status != None:
			return client_status
		else:
			return "Unregistered email."

	def update_admins_on_approval(self):
		"""
		Helper function used to change the approval status in the Administrators
		table.
		"""
		status_id = super().get_status_id(self.mydict["approved_to"])
		try:
			(
			  db.session.query(Administrators).
			  filter(Administrators.admin_email == self.mydict["admin_email"]).
			  update({Administrators.status_id: status_id})
			)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			return False

	def update_clients_on_approval(self):
		"""
		Helper function used to change the checked status in the Administrators
		table.
		"""
		approved_to = super().get_status_id(self.mydict["approved_to"])
		try:
			(
				db.session.query(ClientAdmins).
				filter(ClientAdmins.client_email == self.mydict["admin_email"]).
				update({ClientAdmins.status_id: approved_to})
			)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			return False

	def approve_admin(self):
		"""
		apprver_id: The id of the person doing the aproval
		apprvd_email: The email of the person being approved.
		"""
		is_valid_inputs = super().produce_output(self.mydict)
		if is_valid_inputs != True:
			return is_valid_inputs

		current_status = self.check_dual_registration()
		if isinstance(current_status, str):
			return {"status": False, "message":current_status}

		approved_id = current_status.user_id
		has_been_checked = current_status.status_id

		approved_from = super().get_status_id(self.mydict["approved_from"])
		approved_to = super().get_status_id(self.mydict["approved_to"])

		if has_been_checked == 2:
			return {
						"status": False,
						"message":"Already approved."
					}
		elif has_been_checked != 7:
			return {
						"status": False,
						"message":"Check the administrator first."
					}
		elif has_been_checked == 7:
			approval = AdminApprovals(
							admin_being_approved = approved_id,
									approver_id= self.mydict["approver_id"], 
									approved_from = approved_from,
									approved_to = approved_to
						 )
			if current_status.role_id == 1 or current_status.role_id == 2:
				updated_status = self.update_admins_on_approval()
			if current_status.role_id == 3 or current_status.role_id == 4:
				updated_status = self.update_clients_on_approval()
			if updated_status:
				db.session.add(approval)
				db.session.commit()
				return {
						 "status": True,
						 "message": "User approved successfully"
						}
			else:
				db.session.commit()
				return {
							"status": False,
							"message":"Administrators table not updated to approved."
						}
		else:
			db.session().rollback()
			return {
						"status": False,
						"message":"For some reason the approval was not successfull."
					}

	def update_corp_on_approval(self):
		"""
		Helper function used to change the approval status in the Corporates
		table.
		"""
		approved_to = super().get_status_id(self.mydict["approved_to"])
		try:
			(
				db.session.query(Corporates).
				filter(Corporates.corporate_name == self.mydict["corporate_name"]).
				update({Corporates.status_id: approved_to})
			)
			db.session.commit()
			return True
		except:
			db.session().rollback()


	def approve_company(self):
		"""
		
		approver_id: The id of the person doing the aproval
		approved_id: The id of the persron being approved.
		"""
		confirm = self.is_registered_corporate()
		if confirm is None:	
			return {
						"status": False,
						"message":"Company not registered."
					}

		has_been_checked = confirm.status_id
		approved_from = super().get_status_id(self.mydict["approved_from"])
		approved_to = super().get_status_id(self.mydict["approved_to"])

		if has_been_checked != 7:
			return {
						"status": False,
						"message":"Check the company first."
					}

		elif has_been_checked == 2:
			return {
						"status": False,
						"message":"Already approved."
					}
		elif has_been_checked == 7:
			app = CorporateApprovals(
							corp_being_approved = confirm.corporate_id,
							approver_id = self.mydict["approver_id"], 
							approved_from = approved_from,
							approved_to = approved_to
						 )
			updated_status = self.update_corp_on_approval()			
			if updated_status == True:
				db.session.add(app)
				db.session.commit()
				return {
							"status": True,
							"message":"company successfully approved"
						}
			else:
				db.session().rollback()
				return {
							"status": False,
							"message":"company not updated to approved."
						}
		else:
			db.session().rollback()
			return {
						"status": False,
						"message":"For some reason the company was not approved."
					}

