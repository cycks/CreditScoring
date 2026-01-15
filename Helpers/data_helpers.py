"""
Validates data sent to the backend

Contains value_types variable
Contains the DataTypes class
Contains the DataSent class
"""
import datetime, json

import pandas as pd

from flask import request, jsonify

value_types = {
	"borrower_id": "integer",
	"corporate_id": "integer",
	"borrower_county": "string",
	"borrower_gender": "string",
	"borrower_county": "string",
	"borrower_date_of_birth": "date",
	"borrower_phone_number": "string",
	"corporate_pin": "string",
	"kyc_default_status": "integer",
	"kyc_date_created": "date",
	"registration_date": "date",
	"deposit_amount": "float",
	"date_of_deposit": "date",
	"deposit_description": ["installment", "savings"],
	"deposit_channel": ["airtel", "mpesa", "bank"],
	"date_of_savings": "date",
	"savings_amount": "float",
	"savings_type": ["fixed", "current"],
	"savings_channel": ["airtel", "mpesa", "bank", "mobile_app"],
	"date_of_withdrawals": "date",
	"withdrawals_amount":"float",
	"withdrawals_description": ["current", "savings", "fixed"],
	"withdrawals_channel": ["airtel", "mpesa", "bank", "mobile_app"],
	"date_of_loan": "date",
	"loan_amount": "float",
	"loan_interest": "float",
	"loan_period": "integer",
	"loan_installment_frequency": "integer",
	"date_of_loan_completion": "date",
	"installment_loan_id": "integer",
	"date_of_installment": "date",
	"installment_amount": "float",
	"installment_loan_balance": "float",
	"installment_type": ["interest", "debtcollection", "principal"]
}



class DataTypes():
	"""
	Validates Data and Used in SentData Package
	
	A class used to validate Transactional data sent
	by the client. The class must be instantiated by 
	providing the value_types and data.

	Args:
		data: A json object
		value_types: A dictionar defining the data type
						of each column
	"""
	

	def __init__(self, data, value_types):
		self.data = data
		self.value_types = value_types
		self.dirty_columns = []


	def validate_integer(self, integer_list):
		"""		
		Validates integer columns 
		
		Checks columns that must be integers to ensure
		that all values in the column are integers.

		Args:
			List containing integers
		Returns:
			False if any value in the list is not an int.
		"""
		check_col = all(isinstance(item, int) for item in integer_list)
		if not check_col:
			return False


	def validate_float(self, float_list):
		"""
		Validates float columns

		Checks the data sent to ensure all values in 
		float_list are floats or can be converted to 
		float.

		Args:
			float_list : list
			A list containing floats
		Returns:
			False if any of the value in the float_list
			cannot be converted to float.
		"""
		try:
			float_list = [float(item) for item in float_list]
		except ValueError as e:
			return False

	def validate_string(self, string_list):
		"""
		Validates string columns 

		Checks the data sent to ensure all values in 
		string_list are string or can be converted to 
		strings.

		Args:
			string_list: A list containing strings
		Returns:
			False if any of the values are strings
		"""
		string_list = ([str(item) for item in string_list])
		check_column = all(isinstance(item, str) for item in string_list)
		if not check_column:
			return False


	def validate_dates(self, date_list):
		"""
		Validates date columns

		Checks a column to ensure all variables can be 
		converted to dates.

		arg1 : list
			A list containing date_list
		Returns
			False if any of the date columns cannot be
			converted to dates.
		"""
		df = pd.DataFrame (date_list, columns=['my_dates'])
		try:
			df['my_dates'] = df['my_dates'].astype('datetime64[ns]')
		except:
			return False


	def to_camelcase(self, string):
		"""
		Method used to convert words to title case

		Args:
			string: a string to be converted to camelcase
		Returns
			A string
		"""
		return ' '.join([t.title() for t in str.split(string)])


	def validate_options(self, options_list, options):
		"""
		Method used to validate options.

		Checks that a list of options provided are all
		required. For Example the Installment_type can
		only be interest, debtcollection, or principal

		Args:
			options_list: A list from the data provided
			options: The default values allowed.
		Returns:
			bool: True if all items in options_list are in
			the default options
			bool: False if any of the items in options_list
			are in options.
		"""
		for item in options_list:
			if item.lower() not in options:
				return False
		return True

	def make_validation(self, data):
		"""
		Method used to triger data validation.

		Given data, runs all the type validations in this 
		class. If any of the methods returs False,
		it appends the column name to dirty columns 
		declared before the __init__ method.

		Args: 
			data: A dictionary containing data to be
			validated.
		Returns:
			An empty list if all the data is ok
			Returns a list of columns with invalid data

		"""
		for key, value in self.data.items():
			if self.value_types[key] == "integer":
				if self.validate_integer(self.data[key]) is False:
					self.dirty_columns.append(key)
			elif self.value_types[key] == "float":
				if self.validate_float(self.data[key]) is False:
					self.dirty_columns.append(key)
			elif self.value_types[key] == "string":
				if self.validate_string(self.data[key]) is False:
					self.dirty_columns.append(key)
			elif self.value_types[key] == "date":
				if self.validate_dates(self.data[key])is False:
					self.dirty_columns.append(key)
			else:
				if self.validate_options(self.data[key],
										 self.value_types[key])is False:
					self.dirty_columns.append(key)
		return self.dirty_columns



class DataSent():
	"""
	Checks Column Names and Equal Column Lengths.

	This class must be instantiated using the args
	provided. 
	1. It checks that the data provided has the 
	required columns. 
	2. It also checks that any unrequired columns are 
	not present.
	3. Ensures all columns have equal lengths
	4. Checks that the json data provided has column
	values as lists.
	5. Uses the DataTypes class above to the data
	types provided.
	Remember it does not inherit from Datatypes. I
	don't know why I did this.I will check later.

	Args:
		required_columns: A list of required columns
		data: json data recieved in an endpoint.

	"""
	# TODO: Consider an edge case where data is None
	def __init__(self, required_columns, data=None):
		self.required_columns = required_columns
		self.data = json.loads(request.get_data())
		self.columns_present = list(self.data.keys())
		self.all_columns = DataTypes(self.data, value_types)


	def convert_unicode_string(self, string):
		"""
		Converts a unicode string from bytes.
		
		"""
		return unicodedata.normalize('NFKD', string).encode('ascii','ignore')

	def validate_wanted_columns(self):
		""" 
		Check that no required column is missing.

		Converts columns_present(from the __init__ method)
		to a list, and checks that columns_present is the
		same as required_columns. If not returns the 
		missing columns.

		Args:
			None
		Returns:
			A list of required columns.

		"""
		columns_present = ([item for item in self.columns_present])
		if len(self.required_columns) > len(columns_present):
			missing_columns =  (list(set(self.required_columns) -
											set(columns_present)))
			return missing_columns

	def validate_unwanted_columns(self):
		""" 
		Check that urequired columns are not present.
		
		Checks that columns_present is the same as 
		required_columns. If not returns the aditional
		columns.

		Args:
			None
		Returns:
			A list of columns that must be deleted.
		"""
		# TODO: consider deleting the unrequired columns.
		if len(self.columns_present) > len(self.required_columns):
			addtional_columns  = (list(set(self.columns_present) -
											set(self.required_columns)))
			return addtional_columns


	def check_dictionary_values(self):
		"""
		Check Columns are Lists.

		Ensures that all values are lists. Returns an 
		empty list if all values are lists and returns a 
		list of keys for values that are not lists. 

		Args:
			None
		Returns:
			An empty list if all values are lists
			A list of dictionary values that are not
			lists.

		"""
		not_list_columns = []
		for key, value in self.data.items():
			if not isinstance(value, list):
				not_list_columns.append(key)
		return not_list_columns

	def check_columns_length(self, data):
		"""
		Checks that all columns are eqaul in length

		Extracts the first value from data, compares the 
		length of the first value to all other values in 
		the dictionary. If all values in the dictionary 
		have equal lengths it returns true otherwise 
		returns false.

		Find columns present in the data recieved, extract
		the first column from the data, compare the length
		of the extracted column to all other columns in the
		data. If any of the length is present return True

		Args:
			data: The data recieved from a request
		Returns:
			Returns True if any of the columns is not
			equal to the first column and False otherwise.

		"""
		dataframe_columns = list(self.data.values())
		first_column = dataframe_columns[0]
		length = (all(len(value) == len(first_column)
						for value in self.data.values()))
		if length:
			return True
		return False


	def validate_dict_length(self):
		"""
		Checks length of columns

		Args:
			None
		Returns:
			False if all columns are equal
			True if any column has a different length

		"""
		return self.check_columns_length(self.data)


	def validate_dictionary_values(self):
		"""
		Checks Length of Columns

		Checks that all dictionary values have appropriate
		data types. Uses the make_validation from the 
		DataTypes class defined above.

		Args:
			None
		Returns:
			The number of columns with inapropriate data
			types

		"""
		inapropriate_columns = self.all_columns.make_validation(self.data)
		return len(inapropriate_columns)


	def make_responses(self):
		"""
		The Mother of All Methods in This Class
		
		This function uses other methods in this class to
		check for missing columns, additional columns,
		checks that all values in the json object are
		lists, compares length of lists.

		Args:
			None
		Returns:
			dict: A dictionary with the mistake as the value of
			the dictionary if any of the validations fail.
			bool: None if the data is ok.

		"""
		missing_columns = self.validate_wanted_columns()
		if missing_columns is not None:
			return {
						"status": False,
						"missing columns": missing_columns
					}
		addtional_columns = self.validate_unwanted_columns()
		if addtional_columns is not None:
			return {
						"status":False,
						"remove this additional columns": addtional_columns
					}
		not_list_columns = self.check_dictionary_values()
		if len(not_list_columns):
			return {
						"status": False,
						"These values are not lists": not_list_columns
					}
		equal_lengths = self.check_columns_length(self.data)
		if not equal_lengths:
			return {
						"status": False,
						"message": "dictionary values not equal in length"
					}
		return None
