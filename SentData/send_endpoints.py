"""
This module contains endpoints used to send transactional
data to the database. 


"""


import json


from flask import Blueprint, request, jsonify

from flask_cors import cross_origin


from Helpers.data_helpers import (
									value_types,
									DataSent,
									DataTypes
								)
						
					
from Models.model_users import Authentication
from Models.others import (
							confirm_registered_borrower,
							confirm_registred_corporates
						  )


from SentData.sentdata_helpers import (
								save_kyc_data,
								save_deposits_data,
								save_savings_data,
								save_withdrawals_data,
								save_loans_data,
								save_installments_data
							  )



send_data_routes = Blueprint("send_data_routes", __name__)

@send_data_routes.route('/api/v1/send_kyc_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_kyc_data():
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	required_columns = (["borrower_id",	"corporate_id", "borrower_gender",
						 "borrower_date_of_birth", "borrower_county",
						 "kyc_default_status", "borrower_phone_number",
						 "kyc_date_created"])
	test_101 = DataSent(required_columns).make_responses()
	if test_101 is not None:
		return jsonify(test_101), 422
	# check that all dictionary values have appropriate data types
	data = json.loads(request.get_data())
	all_columns = DataTypes(data, value_types)
	inapropriate_columns = all_columns.make_validation(data)
	if len(inapropriate_columns):
		return jsonify({
						"status":False,
						"Inapropriate data types in": inapropriate_columns
						})
	# Find unregistred corporates in the data set
	unregistered_corporates = confirm_registred_corporates(data)
	if unregistered_corporates:
		return jsonify({
						"status": False, 
						"corporates in this list are not registered":
		                 unregistered_corporates})
	# save data to the database
	if save_kyc_data(data):
		return jsonify({
						"status":True,
						"message": "Data successfully saved"
						})
	return jsonify({
					"status":False, 
					"message": "You have brocken my code. Reach out to me"
					})



@send_data_routes.route('/api/v1/send_deposit_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_deposit_data():
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	required_columns = (['borrower_id', 'corporate_id', 'date_of_deposit',
	                     'deposit_channel', 'deposit_amount',
	                     'deposit_description'])
	test_101 = DataSent(required_columns).make_responses()
	if test_101 is not None:
		return jsonify(test_101)
	# check that all dictionary values have appropriate data types
	data = json.loads(request.get_data())
	all_columns = DataTypes(data, value_types)
	inapropriate_columns = all_columns.make_validation(data)
	if len(inapropriate_columns):
		return jsonify({
						"status": False,
						"Inapropriate data types in": inapropriate_columns
						})
	# Confirm that all the borrowers are registrered in the database
	unregistered_borrowers = confirm_registered_borrower(data)
	if unregistered_borrowers:
		return jsonify({
						"status": False,
						"members in this list are not registered":
		                 unregistered_borrowers})
	# Find unregistred corporates in the data set
	unregistered_corporates = confirm_registred_corporates(data)
	if unregistered_corporates:
		return jsonify({
						"status": False,
						"corporates in this list are not registered":
		                 unregistered_corporates})
	# save data to the database
	if save_deposits_data(data):
		return jsonify({
						"status":True,
						"message": "Deposits data successfully saved"
						})
	return jsonify({
					"status":False, 
					"message": "You have brocken my code. Reach out to me"
					})



@send_data_routes.route('/api/v1/send_savings_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_savings_data():
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	required_columns = (['borrower_id', 'corporate_id', 'date_of_savings',
	                     'savings_channel', 'savings_amount', 'savings_type'])
	test_101 = DataSent(required_columns).make_responses()
	if test_101 is not None:
		return jsonify(test_101)
	# check that all dictionary values have appropriate data types
	data = json.loads(request.get_data())
	all_columns = DataTypes(data, value_types)
	inapropriate_columns = all_columns.make_validation(data)
	if len(inapropriate_columns):
		return jsonify({
						"status": False,
						"Inapropriate data types in": inapropriate_columns
						})
	# save data to the database
	unregistered_borrowers = confirm_registered_borrower(data)
	if unregistered_borrowers:
		return jsonify({
						"status": False,
						"members in the list are not registered":
		                 unregistered_borrower})
	# Find unregistred corporates in the data set
	unregistered_corporates = confirm_registred_corporates(data)
	if unregistered_corporates:
		return jsonify({"status": False,
						"corporates in this list are not registered":
		                unregistered_corporates})
	# check that all dictionary values have appropriate data types
	if save_savings_data(data):
		return jsonify({
						"status":True,
						"message": "Savings data successfully saved"
						})
	return jsonify({
					"status":False, 
					"message": "You have brocken my code. Reach out to me"
					})



@send_data_routes.route('/api/v1/send_withdrawals_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_withdrawals_data():
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	required_columns = (['borrower_id', 'corporate_id', 'date_of_withdrawals',
	                     'withdrawals_channel', 'withdrawals_amount',
	                     'withdrawals_description'])
	test_101 = DataSent(required_columns).make_responses()
	if test_101 is not None:
		return jsonify(test_101)
	# check that all dictionary values have appropriate data types
	data = json.loads(request.get_data())
	all_columns = DataTypes(data, value_types)
	inapropriate_columns = all_columns.make_validation(data)
	if len(inapropriate_columns):
		return jsonify({
						"status":False,
						"Inapropriate data types in": inapropriate_columns
						})
	# Find unregistred corporates in the data set
	unregistered_corporates = confirm_registred_corporates(data)
	if unregistered_corporates:
		return jsonify({
						"status": False,
						"corporates in this list are not registered":
		                 unregistered_corporates
		                })
	# Find unregistered borrowers in the data set
	unregistered_borrowers = confirm_registered_borrower(data)
	if unregistered_borrowers:
		return jsonify({
						"status": False,
						"members in the list are not registered":
		                 unregistered_borrowers
		                })
	# check that all dictionary values have appropriate data types
	if save_withdrawals_data(data):
		return jsonify({
						"status":True,
						"message": "Withrawal data successfully saved"
						})
	return jsonify({
					"status":False, 
					"message": "You have brocken my code. Reach out to me"
					})



@send_data_routes.route('/api/v1/send_loan_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_loans_data():
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	required_columns = (['borrower_id', 'corporate_id',
						 'date_of_loans', 'loan_interest',
	                     'loans_amount', 'loan_period',
	                     'loan_installment_frequency',
	                     'date_of_loan_completion'])
	test_101 = DataSent(required_columns).make_responses()
	if test_101 is not None:
		return jsonify(test_101)
	# check that all dictionary values have appropriate data types
	data = json.loads(request.get_data())
	all_columns = DataTypes(data, value_types)
	inapropriate_columns = all_columns.make_validation(data)
	if len(inapropriate_columns):
		return jsonify({
						"status": False,
						"Inapropriate data types in": inapropriate_columns
						})
	# Find unregistered borrowers in the dataset
	unregistered_borrowers = confirm_registered_borrower(data)
	if unregistered_borrowers:
		return jsonify({
						"status": False,
						"Unregistered are:": unregistered_borrower
						})
	# Find unregistred corporates in the data set
	unregistered_corporates = confirm_registred_corporates(data)
	if unregistered_corporates:
		return jsonify({
						"status":False,
						"corporates in this list are not registered":
		                 unregistered_corporates
		                })
	# check that all dictionary values have appropriate data types
	if save_loans_data(data):
		return jsonify({
						"status": True,
						"message": "Data successfully saved"
						})
	return jsonify({
						"status":False, 
						"message": "You have brocken my code. Reach out to me"
						})



@send_data_routes.route('/api/v1/send_installment_data', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_installments_data():
	details = Authentication(4)
	if not details.is_valid_data():
		return jsonify({"message": "Your data is invalid."}), 400
	if not details.is_valid_token():
	 	return jsonify({"message": "Please log in first."}), 401
	if not details.is_valid_role():
	 	return jsonify({"message": "You are not Authorised"}), 403
	required_columns = (['installment_loan_id', "borrower_id",
    					 'corprate_id', 'date_of_installment',
    					 'installment_amount',
		                 'installment_loan_balance', 'installment_type'])
	test_101 = DataSent(required_columns).make_responses()
	if test_101 is not None:
		return jsonify(test_101)
	# check that all dictionary values have appropriate data types
	data = json.loads(request.get_data())
	all_columns = DataTypes(data, value_types)
	inapropriate_columns = all_columns.make_validation(data)
	if len(inapropriate_columns):
		return jsonify({	
						"status": False,
						"Inapropriate data types in": inapropriate_columns
						})
	# Find unregistered borrowers in the dataset
	unregistered_borrowers = confirm_registered_borrower(data)
	if unregistered_borrowers:
		return jsonify({
						"status": False,
						"Unregistered are:": unregistered_borrower
						})
	# Find unregistred corporates in the data set
	unregistered_corporates = confirm_registred_corporates(data)
	if unregistered_corporates:
		return jsonify({
						"status": False,
						"unregistered corporates are": unregistered_corporates
						})
	if save_installments_data(data):
		return jsonify({
						"status": True,
						"message": "Data successfully saved"
						})
	return jsonify({
						"status": False,
						"message": "You have brocken my code. Reach out to me"
					})
