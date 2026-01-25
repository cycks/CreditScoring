"""Module Containing my Users"""
import datetime, json, os, random
import pandas as pd

from dateutil.relativedelta import relativedelta



from flask import Blueprint, jsonify, request
from flask_cors import cross_origin



from Models.model_users import save_admins, LoggedUsers, Authentication
from Models.others import (	
								check_borrower,
								check_corp_by_name,
								check_score_type
							)


from Models.payments import (
								deduct_service_cost,
								displayed_companies,
								save_credit_score,
								enter_payment
								
							)



from ModelBuilding.Behavioural.prepare_default import (
														create_default_df,
														predict_default,
														grade_probabilities
													   )
from ModelBuilding.Behavioural.prepare_limit import (
														create_limit_df,
														predict_limit
													)



users_routes = Blueprint("users_routes", __name__)




@users_routes.route('/api/v1/', methods=['GET'])
@cross_origin(supports_credentials=True)
def home():
	"""Directs to the landing page of the application"""
	return jsonify({"message": "Welcome to my home page"}), 200



@users_routes.route('/api/v1/register_admin', methods=['POST'])
@cross_origin(supports_credentials=True)
def register_super_admin():
	details = Authentication()
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."})
	mydict = {	
				"user_identity": details.get_user_identity, # National_id
				"admin_names": details.get_admin_names,
				"admin_email": details.get_admin_email,
				"admin_password": details.get_password1,
				"admin_role": details.get_admin_role,
				"corporate_name": details.get_corporate_name
			 }
	
	# check if the email is valid
	if details.check_valid_email(details.get_admin_email) is True:
		# use saved_status from models to save user to db
		secret = os.getenv('SECRET_KEY')
		saved_status = save_admins(mydict, secret)
		return jsonify(saved_status)
	else:
		return jsonify({
						"status": False,
						"message": "Invalid email format"
						}), 400
	

@users_routes.route('/api/v1/confirm_email/<string:token>', methods=['GET'])
def confirm_email(token):
	email_from_token = confirm_token(token)
	is_confirmed_updated = confirm_email(email_from_token)
	if is_confirmed_updated == True:
		# return render_template('confirm_email.html')
		# After processing the request I need to direct the user
		# to say the dashboard or login page
		return jsonify({"message": "Your email has been confirmed"})
	else:
		# return render_template('confirm_email.html')
		return jsonify({"message": "Your email has not been confirmed"})


@users_routes.route('/api/v1/login_admin', methods=['POST'])
@cross_origin(supports_credentials=True)
def login_admin():
	details = Authentication()
	if not details.is_valid_data():
		return jsonify({
							"status": False,
							"message": "Your data is invalid."
						})
	mydict = {
				"admin_email":details.get_admin_email,
				"password1": details.get_password1
			 }
	required_inputs = ["admin_email", "password1"]
	login_user = LoggedUsers(mydict, required_inputs)
	response = login_user.log_in_admin()
	return jsonify(response)


@users_routes.route('/api/v1/display_companies', methods=['GET'])
@cross_origin(supports_credentials=True)
def display_companies():
	all_companies = displayed_companies()
	return jsonify(all_companies)
	

@users_routes.route('/api/v1/login_client', methods=['POST'])
@cross_origin(supports_credentials=True)
def log_in_client():
	details = Authentication()
	if not details.is_valid_data():
		return jsonify({
							"status": False,
							"message": "Your data is invalid."
						})
	mydict = {
				"admin_email":details.get_admin_email,
				"password1": details.get_password1
			 }
	required_inputs = ["admin_email", "password1"]
	login_user = LoggedUsers(mydict, required_inputs)
	response = login_user.log_in_client()
	return jsonify(response)




@users_routes.route('/api/v1/logout', methods=['GET'])
@cross_origin(supports_credentials=True)
def logout():
	"""
	Check if the token is still valid, if it is push it to the 
	blacklisted table. else do nothing.
	"""
	details = Authentication()
	mydict = {
				"admin_id": details.get_admin_id,
				"role_id": details.get_admin_role,
				"user_token": details.get_user_token
			 }
	logout_user = LoggedUsers(mydict)
	response = logout_user.logout()
	return jsonify(response)


@users_routes.route('/api/v1/reset_password', methods=['POST'])
def reset_password():
	details = Authentication()


@users_routes.route('/api/v1/get_behavioral_score', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_behavioral_score():
	"""
	corporate_name:
	borrower_id:
	score_type: 
	"""
	details = Authentication(4)
	if not details.is_valid_role():
		return jsonify({
						"status": False,
						"message": "You are not Authorised"
						}), 401
	if not details.is_valid_token():
		return jsonify({
						"status": False,
						"message": "Please log in first."
						}), 401

	# used for default prediction
	corporate_name = details.get_corporate_name
	borrower_id = details.get_borrower_id
	score_name =  details.get_score_name	
	
	borrower_is_registered = check_borrower(borrower_id)
	if not borrower_is_registered:
		return jsonify({
						"status": False,
						"message": "This borrower is not registered"
						}), 403

	is_registered_corporate = check_corp_by_name(corporate_name)
	corporate_id = is_registered_corporate
	if not is_registered_corporate:
		return jsonify({
						"status": False,
						"message": "This company is not registered"
						}), 403

	is_correct_score_name = check_score_type(score_name)
	if not is_correct_score_name:
		return jsonify({
						"status": False,
						"message": "Wrong score type provided"
						}), 403


	user_df = create_default_df(borrower_id, is_registered_corporate)
	user_score = predict_default(user_df)
		

	if user_score:
		pdf = user_score["probability_of_payment"]
		user_grade = grade_probabilities(pdf, 20, 800)
		return jsonify({
							"status": True,
							"credit_score": user_grade
						}), 200
	else:
		return jsonify({
						"status": False,
						"message": "Error: the score was not calculated"
						})



@users_routes.route('/api/v1/get_behavioral_limit', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_behavioral_limit():
	""" 	"""
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({
							"status": False,
							"message": "Your data is invalid."
						}), 400
	if not details.is_valid_token():
	 	return jsonify({
	 					"status": False,
	 					"message": "Please log in first."
	 					}), 401
	if not details.is_valid_role():
		return jsonify({
							"status": False,
							"message": "You are not Authorised"
						}), 403
	date_of_loan = datetime.datetime.now()
	loan_period = details.get_loan_period
	loan_frequency = details.get_loan_frequency
	final_date	= datetime.datetime.now() + relativedelta(months=loan_period)
	corporate_id = details.get_corporate_id
	borrower_id = details.get_borrower_id

	loan_data = {
					'loan_id': 0, 'borrower_id': borrower_id,
					'corporate_id': corporate_id,
					'date_of_loan': date_of_loan,
					'loan_period': loan_period, 'loan_amount': 0,
					'loan_installment_frequency': loan_frequency,
					'date_of_loan_completion': final_date,
					'is_defaulted_loan':0
				 }
	user_df = create_limit_df(
								borrower_id, 
								corporate_id,
								loan_data
							 )
	credit_limit = predict_limit(user_df)
	return jsonify({
						"status": True,
						"credit limit": credit_limit
					})



@users_routes.route('/api/v1/make_payment', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_payment():
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

	admin_id = details.is_logged_in()
	corporate_name = details.get_corporate_name
	amount_uploaded = details.get_amount_uploaded

	uploaded_status = enter_payment(admin_id, corporate_name, amount_uploaded)

	if uploaded_status == "This company is not registered.":
		return jsonify({
							"status": False,
							"message": "Unregistered company"
						})
	elif uploaded_status is True:
		return jsonify({
						"status": False,
						"message": "Payment uploaded successfully."
						})
	else:
		return jsonify({
						"status": False,
						"message": "Brocken code in make_payment."
						})

