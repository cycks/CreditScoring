"""
Contains

1. Corporate registration endpoints.
2. Corporate Checks endpoints.
3. Corporate approvals endpoints. 

The admin_status dictionary must always remain as it is because 
it contains ids as they are in the database.

"""


from flask import request, jsonify, Blueprint

from flask_cors import cross_origin


from Models.checks_n_approvals import Approvals, Checks
from Models.model_users import Authentication
from Models.others import save_company_details



company_routes = Blueprint("company_routes", __name__)



admin_status = {"awaiting_approval": 1, "approved": 2, "dormant":3,
				"blocked": 4, "decision_rescinded": 5, "to_be_checked": 6,
				"checked": 7}

@company_routes.route('/api/v1/register_company', methods=['POST'])
@cross_origin(supports_credentials=True)
def register_company():
	"""
	Company registration endpoint.
	
	This endpoint is used to register corporates. authenticate the user
	check that the user has role_id 2 or 1 using the Authentication class,
	and register the organization. The mydict contains details that are
	sent to the backend for registration,

	Args:
		None
	Returns:
		dict: A dictionary with status True and an appropriate message
		if the registration is successful.
		A dictionary with status False and an approproate message if 
		registration is unsucessful.
	"""
	details = Authentication(2)
	if not details.is_valid_data():
		return jsonify({
							"status": False,
							"message": "Your data is invalid."
						}), 400
	if not details.is_logged_in():
		return jsonify({
							"status": False,
							"message": "Please log in first."
						}), 401
	if not details.is_valid_role():
		return jsonify({
							"status": False,
							"message": "You are not Authorised"
						}), 403

	mydict = {
				"corporate_name": details.get_corporate_name,
				"corporate_pin": details.get_corporate_pin
			 }

	user_identity = details.is_logged_in()
	company_is_saved = save_company_details(mydict, user_identity)

	if company_is_saved == True:
		return jsonify({	
							"status": True,
							"message": "Registered. Wait for approval"
						}), 200
	elif company_is_saved == "Company already registered.":
		return jsonify({
							"status": False,
							"message": "Company name already taken."
						})
	else:
		return jsonify({
							"status": False,
							"message": "For for some reason"
						})



@company_routes.route('/api/v1/check_company', methods=['PUT'])
@cross_origin(supports_credentials=True)
def check_company():
	"""
	Checks the company status.

	This endpoint is used to check registered companies. It confirms
	that the person doing the checking has a role id 2 or 1 using the 
	Authentication class. mydict contains the information required to
	register the company. The required_inputs is used to check against
	data sent from the request to ensure that the enpoint recieves all
	the required inputs

	Args:
		None
	Returns:
		dict: A dictionary with status True and an appropriate message
		if the checking is successful.
		A dictionary with status False and an approproate message if 
		checking is unsucessful.
	"""
	details = Authentication(2)
	if not details.is_valid_data():
		return jsonify({
							"status": False,
							"message": "Your data is invalid."
						}), 400
	if not details.is_logged_in():
		return jsonify({
							"status": False,
							"message": "Please log in first."
						}), 401
	if not details.is_valid_role():
		return jsonify({
							"status": False,
							"message": "You are not Authorised"
						}), 403

	required_inputs = [	"checker_id", "corporate_name", "checked_from",
							"checked_to"]
	# TODO consider not updating the administrators to checked
	mydict = {	
				"corporate_name": details.get_corporate_name,
				"checker_id": details.is_logged_in(),
				"checked_from": details.get_checked_from,
				"checked_to": details.get_checked_to
			 }
	is_checked = Checks(mydict, required_inputs).check_company()
	return jsonify(is_checked)


@company_routes.route('/api/v1/approve_company', methods=['PUT'])
@cross_origin(supports_credentials=True)
def approve_company():
	"""
	Makes Corporate Approval

	Authenticates the user and confirms that the user has a role id 1.
	mydict contains information that is required to make an approval.
	The required_inputs is used to check against data sent from the
	request to ensure that the enpoint recieves all the required 
	inputs.

	Args:
		None
	Returns:
		dict: A dictionary with status True and an appropriate message
		if the checking is successful.
		A dictionary with status False and an approproate message if 
		checking is unsucessful.
	"""
	details = Authentication(1)
	if not details.is_valid_data():
		return jsonify({
							"status": False,
							"message": "Your data is invalid."
						}), 400
	if not details.is_logged_in():
		return jsonify({
							"status": False,
							"message": "Please log in first."
						}), 401
	if not details.is_valid_role():
		return jsonify({
							"status": False,
							"message": "You are not Authorised"
						}), 403


	required_inputs = [	"approver_id", "corporate_name", "approved_from",
							"approved_to"]
	# TODO consider not updating the administrators to checked
	mydict = {	
				"corporate_name": details.get_corporate_name,
				"approver_id": details.is_logged_in(),
				"approved_from": details.get_approved_from,
				"approved_to": details.get_approved_to
			 }
	is_approved = Approvals(mydict, required_inputs).approve_company()
	return jsonify({"message": is_approved})
