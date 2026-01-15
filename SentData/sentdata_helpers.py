"""
Used in the send_endpoints module to save data in the 
database. 

Uses functions defined in myapp.Models.our_data module
to persist data in the db.

"""

from Models.our_data import(
									push_kyc_to_db,
									push_deposits_to_db,
									push_savings_to_db,
									push_withdrawals_to_db,
									push_loans_to_db,
									push_installments_to_db
								)



the_list = [
				"254701", "254702", "254703", "254704", "254705", "254706",
				"254707", "254708", "254710", "254709", "254711", "254712",
				"254713", "254714", "254715", "254716", "254717", "254718",
				"254719", "254720", "254721", "254722", "254723", "254724",
				"254725", "254726", "254728", "254729", "254740", "254741",
				"254742", "254743", "254726", "254703", "254790", "254791",
				"254792", "254793", "254794", "254795", "254796", "254797",
				"254798", "254799", "254110", "254111", "254730", "254731",
				"254734", "254735", "254736", "254737", "254738", "254739",
				"254750", "254751", "254752", "254752", "254753"
			]



def validate_phone_number(my_number):
	to_check = str(my_number[:6])
	if to_check in the_list and len(my_number) == 12:
		return True
	try:
		int(my_number)
	except Exception as e:
		return False
	return False



def save_kyc_data(data):
	"""Extract the first column from the post request, use the
	length of the column to loop through every list item in the
	post request and saving all list items in the same index
	to the database dynamically."""
	user_index = 0
	dataframe_columns = list(data.values())
	first_column_values = dataframe_columns[0]
	for item in first_column_values:
		borrower_id = data['borrower_id'][user_index]
		saved_kyc_data = push_kyc_to_db(borrower_id, data, user_index)
		if saved_kyc_data:
			user_index += 1
		else:
			raise LookupError("user data not saved in kyc_table.")
	return True


def save_deposits_data(data):
	"""Extract the first column from the post request, use the
	length of the column to loop through every list item in the
	post request and saving all list items in the same index
	to the database dynamically."""
	user_index = 0
	dataframe_columns = list(data.values())
	first_column_values = dataframe_columns[0]
	for item in first_column_values:
		borrower_id = data['borrower_id'][user_index]
		saved_deposits_data = push_deposits_to_db(data, user_index)
		if saved_deposits_data:
			user_index += 1
		else:
			raise LookupError("user data not saved in kyc_table.")
	return True


def save_savings_data(data):
	"""Extract the first column from the post request, use the
	length of the column to loop through every list item in the
	post request and saving all list items in the same index
	to the database dynamically."""
	user_index = 0
	dataframe_columns = list(data.values())
	first_column_values = dataframe_columns[0]
	for item in first_column_values:
		borrower_id = data['borrower_id'][user_index]
		saved_deposits_data = push_savings_to_db(data, user_index)
		if saved_deposits_data:
			user_index += 1
		else:
			raise LookupError("user data not saved in kyc_table.")
	return True


def save_withdrawals_data(data):
	"""Extract the first column from the post request, use the
	length of the column to loop through every list item in the
	post request and saving all list items in the same index
	to the database dynamically."""
	user_index = 0
	dataframe_columns = list(data.values())
	first_column_values = dataframe_columns[0]
	for item in first_column_values:
		borrower_id = data['borrower_id'][user_index]
		saved_deposits_data = push_withdrawals_to_db(data, user_index)
		if saved_deposits_data:
			user_index += 1
		else:
			raise LookupError("user data not saved in kyc_table.")
	return True


def save_loans_data(data):
	"""Extract the first column from the post request, use the
	length of the column to loop through every list item in the
	post request and saving all list items in the same index
	to the database dynamically."""
	user_index = 0
	dataframe_columns = list(data.values())
	first_column_values = dataframe_columns[0]
	for item in first_column_values:
		borrower_id = data['borrower_id'][user_index]
		saved_deposits_data = push_loans_to_db(data, user_index)
		if saved_deposits_data:
			user_index += 1
		else:
			raise LookupError("user data not saved in kyc_table.")
	return True


def save_installments_data(data):
	"""Extract the first column from the post request, use the
	length of the column to loop through every list item in the
	post request and saving all list items in the same index
	to the database dynamically."""
	user_index = 0
	dataframe_columns = list(data.values())
	first_column_values = dataframe_columns[0]
	for item in first_column_values:
		installment_loan_id = data['installment_loan_id'][user_index]
		saved_deposits_data = push_installments_to_db(data, user_index)
		if saved_deposits_data:
			user_index += 1
		else:
			raise LookupError("user data not saved in kyc_table.")
	return True