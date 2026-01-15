"""
Validate the correct datatypes 
"""
class ValidInputs():
	"""	
	Validates data types from inputs.
	
	1. dirty_values is a class variable. 
	2. required_inputs default is none but must be 
		provided.
	3. valid_inputs is a dictionary of inputs
		and thier associated data types.
	"""

	def __init__(self, required_inputs=None):
		self.required_inputs = required_inputs
		self.dirty_values = {}

	@property
	def valid_inputs(self):
		return {
					
					"admin_email": "string",					
					"admin_id": "int",
					"admin_names": "string",
					"admin_password": "string",	
					"admin_status": "string",
					"admin_role": "string",					
					"amount_uploaded": "float",		
					"approved_from": "string", 
					"approved_to": "string",
					"approver_id": "int",					
					"borrower_id":"int",
					"checker_id":"int",			
					"checked_from": "string",
					"checked_to":"string",						
					"corporate_id": "int",
					"corporate_name": "string",
					"corp_name": "string",					
					"corporate_pin": "string",
					"password1": "string",
					"password2": "string",
					"role_id": "int",
					"score_name": "string",		
					"status_id": "int",
					"user_identity": "int",	
					"user_name": "string",
				}



	def is_valid_input(self, mydict):
		"""
		Validates the data type of an input
		
		Loops through the dictionary provided, extracts
		a key from the dictionary. Using the extracted
		key, extracts the values with the same key from
		valid_inputs then checks for the appropriate data
		type.

		Args:
			mydict: a dictionary of inputs to be validated.
		Returns
			None 
		"""
		for key, value in mydict.items():
			required_type = self.valid_inputs[key]
			if required_type == "string":
				if not isinstance(value, str):
					required_type = "should be " + required_type 
					self.dirty_values[key] = required_type
			elif required_type == "int":
				try:
					int(value)
				except ValueError as e:
					required_type = "should be " + required_type 
					self.dirty_values[key] = required_type
			elif required_type == "float":
				try:
					float(value)
				except ValueError as e:
					required_type = "should be " + required_type 
					self.dirty_values[key] = required_type
			else:
				None
		return None


	@property
	def current_roles(self):
		"""
		User roles and asssociated ids.
		
		Args: 
			None
		Returns:
			A dictionary of roles and ids.
		"""
		admin_roles = {
							"super_admin": 1, "infotrace_admin":2,
							"client_admin":3, "client_staff":4
					  }
		return admin_roles


	@property
	def current_status(self):
		"""		
		User status and asssociated ids.
		
		Args: 
			None
		Returns:
			A dictionary of status and ids.
		"""
		admin_status = {
							"awaiting_approval": 1, "approved": 2, "dormant":3,
							"blocked": 4, "decision_rescinded": 5,
							"to_be_checked": 6, "checked": 7
						}
		return admin_status


	def get_role_id(self, role_name):
		"""		
		Extracts and validates the role id.

		Given a role_name such as super_admin extract the value
		assocaited with the role_name(i.e the role_id). Note
		that the order of the role names is in the same order as
		the Roles table in the database.
		
		Args: 
			role_name: a string of the role_name
		Returns:
			role_id (int): of the associated role_name
		"""
		return self.current_roles[role_name]


	def get_status_id(self, status_name):
		"""
		Extracts and validates the status_id.
		
		Given a status_name such as awaiting_approvale extract the 
		value assocaited with the role_name(i.e the role_id). Note
		that the order of the role names is in the same order as
		the Roles table in the database.

		Args: 
			status_name: a string of the status_name
		Returns:
			An id (int): of the associated status_name
		"""
		return self.current_status[status_name]

	
	def find_missing_values(self, mydict):
		"""
		
		Check that we do not have missing inputs.
		

		Given a dictionary, checks that no dictionary 
		value is missing. It also compares the dictionary
		keys with required inputs to ensure that the data
		submited from the front end has the required. If 
		their is a mistake in any of the inputs it 
		appends the input with the mistake to dirty_values

		Philosophy: An endpoint will have required inputs
		A user will provide inputs. This function then checks
		that the inputs provided by the user are the required
		inputs in the endpoint.

		Args:
			mydict: A dictionary containing iputs from the user
		Retruns:
			None
		"""
		for key, value in mydict.items():
			if value == None:
				self.dirty_values[key] = "is_missing"
		for item in self.required_inputs:
			if item not in mydict.keys():
				self.dirty_values[item] = "is_missing"
		return None

	def produce_output(self, mydict):
		"""
		The Mother of all methods in this class.
		
		Method called to do the validation. using the 
		find_missing_values method in this class, checks
		for any missing values. If any of the inputs are
		missing return a dictionary of inputs and missing
		values. 

		Also checks to ensure that all of the inputs have
		the correct data types using the is_valid_input
		method in this class. If any of the inputs is not
		valid, appends the input to dirty_values.

		If data passes all validations returns True.

		Args:
			mydict: A dictionary containing user inputs
		Returns:
			A dictionary if any input is missing
			A dictionary if any input is bad data type
			True if the data is valid
		"""
		invalid_inputs = self.find_missing_values(mydict)
		if len(self.dirty_values) >= 1:
			return self.dirty_values
		invalid_inputs = self.is_valid_input(mydict)
		if len(self.dirty_values) >= 1:
			return self.dirty_values
		else:
			return True