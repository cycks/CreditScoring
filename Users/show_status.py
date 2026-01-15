"""Module Containing my Users"""


from flask import jsonify, Blueprint, request

from flask_cors import cross_origin


from Models.model_users import Authentication
from Models.displays import DisplayedChecks,	DisplayedApprovals


display_routes = Blueprint("display_routes", __name__)

class Pagination:
	"""
	Class used for pagination.

	This class was not written from scratch. It was obtained from
	https://www.tutorialspoint.com/book-pagination-in-python.
	The very first page begins at Zero and not 1.

	"""
	
	def solve(self, to_paginate, start_from, number_of_items):
		l = start_from * number_of_items
		return to_paginate[l:l + number_of_items]

@display_routes.route('/api/v1/fetch_checks/<string:fetch_type>', methods=['GET'])
@cross_origin(supports_credentials=True)
def fetch_checks(fetch_type):
	details = Authentication()
	if not details.is_valid_token():
		return jsonify({"message": "Please log in first."}), 401

	admin_id = details.is_logged_in()
	role_id = details.get_admin_role # From the token
	corporate_id = details.get_corporate_id
	fetches = DisplayedChecks(fetch_type, role_id, corporate_id)
	current_checks = fetches.make_a_check_fetch()
	# Show and remove errors
	if role_id >= 4:
		return jsonify({"messge": "Wrong administrator role"})
	if current_checks is None or len(current_checks) == 0:
		return jsonify ({"message": "No checks for now"})
	if len(current_checks) >= 1:
		# paginate the results
		pages = Pagination()
		start_from = request.args.get("start_from")
		number_of_items = request.args.get("number_of_items")
		if start_from == None:
			start_from = 0
		if number_of_items == None:
			number_of_items = 10
		paginated_checks = pages.solve(current_checks, start_from, number_of_items)
		return jsonify(paginated_checks)


@display_routes.route('/api/v1/fetch_approvals/<string:fetch_type>', methods=['GET'])
@cross_origin(supports_credentials=True)
def fetch_approvals(fetch_type):
	details = Authentication()
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	
	admin_id = details.is_logged_in()
	role_id = details.get_admin_role # from the token
	corporate_id = details.get_corporate_id
	fetches = DisplayedApprovals(fetch_type, role_id, corporate_id)
	current_approvals = fetches.make_an_approval_fetch()
	# paginate the results
	if role_id == 1 or role_id == 3:
		if len(current_approvals) >= 1:
			pages = Pagination()
			start_from = request.args.get("start_from")
			number_of_items = request.args.get("number_of_items")
			if start_from == None:
				start_from = 0
			if number_of_items == None:
				number_of_items = 10
			paginated_approvals = pages.solve(
												current_approvals,
												start_from,
												number_of_items
											  )
			return jsonify(paginated_approvals)
		if current_approvals is None or len(current_approvals) == 0:
			return jsonify ({
								"status": True,
								"message": "No approvals for now"
							})
	elif role_id == 2 or role_id == 4:
		return jsonify({
						"status": False,
						"message": "Wrong administrator role"
						})
	else:
		return jsonify({"You have just brocken my code in fetch approvals"})
	
