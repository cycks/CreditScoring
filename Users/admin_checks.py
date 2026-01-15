"""
Module Containing Checks

This file contains endpoints used to make checks.
The following endpoints are pressent in this module

	1.check_super_admin
	2.check_info_admin
	3.check_client_admin
	4.check_client_staff
"""

import json


from flask import jsonify, Blueprint
from flask_cors import cross_origin


from Models.model_users import Authentication
from Models.checks_n_approvals import Checks

				   

check_routes = Blueprint("check_routes", __name__)


@check_routes.route('/api/v1/check_super_admin', methods=['PUT'])
@cross_origin(supports_credentials=True)
def check_super_admin():
	"""
	Used to check super admins.

	Authenticate the user by checking that their role id is 1 using the
	Authentication class that was imported from Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. checker_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    checked).
		3. checked_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. checked_to (what status are we approving to?)

	Using the Cheks class imported from Models.checks_n_approvals
	return the appropriate response.

	Args:
		None
	Returns:
		A dictionary containing the status and the appropriate 
		response.
	Note:
		This endpoint is only accessible to super admins.
	"""
	details = Authentication(1)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403

	required_inputs = [	"checker_id", "admin_email", "checked_from",
						"checked_to"]
	mydict = {	
				"checker_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"checked_from": details.get_checked_from,
				"checked_to": details.get_checked_to
			 }
	is_checked = Checks(mydict, required_inputs).check_admin()
	return jsonify(is_checked)
	


@check_routes.route('/api/v1/check_info_admin', methods=['PUT'])
@cross_origin(supports_credentials=True)
def check_info_admin():
	"""
	Used to check infotrace staff.

	Authenticate the user by checking that their role id is 2 or 1
	using the Authentication class that was imported from 
	Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. checker_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    checked).
		3. checked_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. checked_to (what status are we approving to?)

	Using the Cheks class imported from Models.checks_n_approvals
	return the appropriate response.

	Args:
		None
	Returns:
		A dictionary containing the status and the appropriate 
		response.
	Note:
		This endpoint is only accessible to super admins and 
		infotrace staff.
	"""
	details = Authentication(2)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403

	required_inputs = [	"checker_id", "admin_email", "checked_from",
							"checked_to"]
	# TODO consider not updating the administrators to checked
	mydict = {	
				"checker_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"checked_from": details.get_checked_from,
				"checked_to": details.get_checked_to
			 }
	is_checked = Checks(mydict, required_inputs).check_admin()
	return jsonify(is_checked)
	


# Accesible to the infotrace and super admin only. checks an infotrace admin
@check_routes.route('/api/v1/check_client_admin', methods=['PUT'])
@cross_origin(supports_credentials=True)
def check_client_admin():
	"""
	Used to check client_admins.

	Authenticate the user by checking that their role id is 1 using the
	Authentication class that was imported from Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. checker_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    checked).
		3. checked_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. checked_to (what status are we approving to?)

	Using the Cheks class imported from Models.checks_n_approvals
	return the appropriate response.

	Args:
		None
	Returns:
		A dictionary containing the status and the appropriate 
		response.
	Note:
		Note:
		This endpoint is only accessible to super admins and 
		infotrace staff.
	"""
	details = Authentication(2)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403

	required_inputs = [	"checker_id", "admin_email", "checked_from",
				"checked_to"]
	# TODO consider not updating the administrators to checked
	mydict = {	
				"checker_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"checked_from": details.get_checked_from,
				"checked_to": details.get_checked_to
			 }
	is_checked = Checks(mydict, required_inputs).check_admin()
	return jsonify(is_checked)



@check_routes.route('/api/v1/check_client_staff', methods=['PUT'])
@cross_origin(supports_credentials=True)
def check_client_staff():
	"""
	Used to check client staff.

	Authenticate the user by checking that their role id is 1 using the
	Authentication class that was imported from Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. checker_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    checked).
		3. checked_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. checked_to (what status are we approving to?)

	Using the Cheks class imported from Models.checks_n_approvals
	return the appropriate response.

	Args:
		None
	Returns:
		A dictionary containing the status and the appropriate 
		response.
	Note:
		This endpoint is only accessible to super admins.
	"""
	details = Authentication(3)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	
	required_inputs = [	"checker_id", "admin_email", "checked_from",
				"checked_to"]
	
	# TODO consider not updating the administrators to checked
	mydict = {	
				"checker_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"checked_from": details.get_checked_from,
				"checked_to": details.get_checked_to
			 }
	is_checked = Checks(mydict, required_inputs).check_admin()
	return jsonify(is_checked)