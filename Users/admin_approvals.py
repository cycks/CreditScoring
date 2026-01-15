"""
Module Containing Approvals

This file contains endpoints used to make approvals.
The following endpoints are pressent in this module

	1.approve_super_admin
	2.approve_info_admin
	3.approve_client_admin
	4.approve_client_staff

"""


from flask import jsonify, Blueprint
from flask_cors import cross_origin



from Models.checks_n_approvals import  Approvals
from Models.model_users import Authentication


approve_routes = Blueprint("approve_routes", __name__)


@approve_routes.route('/api/v1/approve_super_admin', methods=['PUT'])
@cross_origin(supports_credentials=True)
def approve_super_admin():
	"""
	Used to approve super admins.

	Authenticate the user by checking that their role id is 1 using the
	Authentication class that was imported from Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. approver_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    approved).
		3. approved_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. apptoved_to (what status are we approving to?)

	Using the Approvals class imported from Models.checks_n_approvals
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
		return jsonify({"message": "Your data is  invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403

	required_inputs = ["approver_id", "admin_email", "approved_from",
						"approved_to"]
	mydict = {	
				"approver_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"approved_from": details.get_approved_from,
				"approved_to": details.get_approved_to
			 }
	is_approved = Approvals(mydict, required_inputs).approve_admin()
	return jsonify(is_approved)


"""
 Endpoint accesible to the super admin and infotrace admin.
 checks an infotrace admin
 """
@approve_routes.route('/api/v1/approve_info_admin', methods=['PUT'])
@cross_origin(supports_credentials=True)
def approve_info_admin():
	"""
	Used to approve Infotrace admins.

	Authenticate the user by checking that their role id is 1 using the
	Authentication class that was imported from Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. approver_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    approved).
		3. approved_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. apptoved_to (what status are we approving to?)

	Using the Approvals class imported from Models.checks_n_approvals
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

	required_inputs = ["approver_id", "admin_email", "approved_from",
						"approved_to"]
	mydict = {	
				"approver_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"approved_from": details.get_approved_from,
				"approved_to": details.get_approved_to
			 }
	is_approved = Approvals(mydict, required_inputs).approve_admin()
	return jsonify(is_approved)


@approve_routes.route('/api/v1/approve_client_admin', methods=['PUT'])
@cross_origin(supports_credentials=True)
def approve_client_admin():
	"""
	Used to approve client admins.

	Authenticate the user by checking that their role id is 1 using the
	Authentication class that was imported from Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. approver_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    approved).
		3. approved_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. apptoved_to (what status are we approving to?)

	Using the Approvals class imported from Models.checks_n_approvals
	return the appropriate response.

	Args:
		None
	Returns:
		A dictionary containing the status and the appropriate 
		response.
	Note:
		This endpoint is only accessible to infortaces admins and
		client admins.
	"""
	details = Authentication(1)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is  invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403

	required_inputs = ["approver_id", "admin_email", "approved_from",
						"approved_to"]
	mydict = {	
				"approver_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"approved_from": details.get_approved_from,
				"approved_to": details.get_approved_to
			 }
	is_approved = Approvals(mydict, required_inputs).approve_admin()
	return jsonify(is_approved)



@approve_routes.route('/api/v1/approve_client_staff', methods=['PUT'])
@cross_origin(supports_credentials=True)
def approve_client_staff():
	"""
	Used to approve client staff.

	Authenticate the user by checking that their role id is less than or
	equal to 3 using the Authentication class that was imported from 
	Models.model_users.

	The required inputs is a list of inputs required in this endpoint.
	in case the required inputs changes, remember to update this list.

	mydict is a dictionary containing the:
		1. approver_id (the admin id of the current user)
		2. admin_email (the admin email of the super admin being 
		    approved).
		3. approved_from (the latest status of the user. Remember 
		   if the current status is checked it will not show checked, 
		   instead it should show the recent status before checking)
		4. apptoved_to (what status are we approving to?)

	Using the Approvals class imported from Models.checks_n_approvals
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
		return jsonify({"message": "Your data is  invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	
	required_inputs = ["approver_id", "admin_email", "approved_from",
						"approved_to"]
	mydict = {	
				"approver_id": details.is_logged_in(),
				"admin_email": details.get_admin_email,
				"approved_from": details.get_approved_from,
				"approved_to": details.get_approved_to
			 }
	is_approved = Approvals(mydict, required_inputs).approve_admin()
	return jsonify(is_approved)
