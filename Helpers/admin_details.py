import json, jwt, os, re

from flask import request, jsonify


class AdminDetails:
	"""
	Extract data from a request.
	
	A class used to extract user details from a request
	If any input is added to the api, then 	this class 
	should be updated.

	TODO: consider a situation where the key is None

	"""
	def __init__(self, data=None):
		"""
		Check if the request contains data in the body
		if not then set the body of the data as an 
		empty dictionary. If the body is not empty
		then convert the body to a json object. 

		If the json.decoder.JSONDecodeError is raised
		then the data sent is not valid.

		TODO: Consider adding filetypes if the 
		application grows.
		"""
		try:
			self.data = request.get_data()
			if len(self.data) == 0:
				self.data = {}
			else:
				self.data = json.loads(self.data)
		except json.decoder.JSONDecodeError as e:
			return None

	
	@property
	def get_corporate_name(self):
		"""		
		Extracts corporate name from the request
		

		Args:
			None
		Returns:
			Corporate name(string) or None
		"""
		return self.data.get("corporate_name", None)
	

	
	@property
	def get_admin_names(self):
		"""
		Extracts admin names from the request.
		
		Args:
			None
		Returns:
			The admin names (str) or None
		"""
		return self.data.get("admin_names", None)
	

	@property
	def get_admin_email(self):
		"""
		Used to extract user's email,
		
		Args:
			None
		Returns:
			The admin email(str) or None
		"""
		return self.data.get("admin_email", None)


	@property
	def get_password1(self):
		"""		
		Used to extract user's password1
		
		Args:
			None
		Returns:
			The password(str) or None
		"""
		return self.data.get("password1", None)


	@property
	def get_user_name(self):
		"""
		Used to extract user's username.
		
		Args:
			None
		Returns:
			The user name(str) or None
		"""
		return self.data.get("user_name", None)


	
	@property
	def get_corporate_pin(self):
		"""		
		Used to extract user's username.
		
		Args:
			None
		Returns:
			The corporate_pin(str) or None
		"""
		return self.data.get("corporate_pin", None)


	
	@property
	def get_approved_from(self):
		"""		
		Extracts the approved_from from the request
		
		Args:
			None
		Returns:
			The approved_from (str) or None
		"""
		return self.data.get("approved_from", None)


	
	@property
	def get_approved_to(self):
		"""
		Extracts the approved_to from the request
		
		Args:
			None
		Returns:
			The approved_to (str) or None
		"""
		return self.data.get("approved_to", None)


	@property
	def get_checked_from(self):
		"""
		Extracts the checked_from from the request

		Args:
			None
		Returns:
			The chcked_from (str) or None
		"""
		return self.data.get("checked_from", None)


	@property
	def get_checked_to(self):
		"""
		Used to extract checked_to from the request.

		Args:
			None
		Returns:
			The check_to(string) or None
		"""
		return self.data.get("checked_to", None)


	@property
	def get_score_name(self):
		"""
		Used to extract score_name from the request.
		

		Args:
			None
		Return:
			The name of the score(string) or None
		"""
		return self.data.get("score_name", None)

	
	@property
	def get_borrower_id(self):
		"""
		Extracts borrower_id from the request.
		
		Args:
			None
		Returns:
			The borrower_id(int) or None
		"""
		# TODO: compare to get_user_identity
		return self.data.get("borrower_id", None)


	@property
	def get_amount_uploaded(self):
		"""
		Extracts the amount uploaded from the request.


		Args:
			None
		Returns:
			amount_uploaded or None
		"""
		return self.data.get("amount_uploaded", None)

	
	def check_valid_email(self, admin_email):
		"""		
		Check that an email is valid format
		
		Args:
			email
		Returns:
			Bool: True or False
		"""
		regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
		if(re.search(regex,admin_email)):
			return True
		else:
			return False


	@property
	def get_user_identity(self):
		"""
		Extracts The User_identity
		
		Check if the request has a corporate id in
		the body and return it. If the corporate 
		id is not in the body check that the id is
		in the header and return it if present. 
		Else return False.

		Args:
			None
		Returns:
			user_identity or None
		"""
		try:
			user_identity = self.data.get("user_identity", None)
			if user_identity:
				return user_identity
			else:
				user_token = request.headers.get("user_token")
				secret = os.getenv('SECRET_KEY')
				decoded_token = jwt.decode(user_token, secret)
				user_identity = decoded_token['user_identity']		  
				return user_identity
		except jwt.exceptions.DecodeError:
			return False
		except jwt.exceptions.ExpiredSignatureError:
			return False

	@property
	def get_borrower_id(self):
		"""
		Extracts The User_identity
		
		Check if the request has a corporate id in
		the body and return it. If the corporate 
		id is not in the body check that the id is
		in the header and return it if present. 
		Else return False.

		Args:
			None
		Returns:
			user_identity or None
		"""
		return self.data.get("borrower_id", None)

	
	@property
	def get_loan_period(self):
		"""
		Extract the loan_period from the request.

		Args:
			None
		Returns:
			The loan period (int) or None
		"""
		return self.data.get("loan_period", None)


	@property
	def get_loan_frequency(self):
		"""
		Extract the loan frequency from the request

		Args:
			None
		Returns:
			Thr loan frequency(int) or None
		"""
		return self.data.get("loan_frequency", None)
	
	@property
	def get_user_token(self):
		"""		
		Extract the user_token from the request.
		

		Check if the token is present, if the token is
		present and valid, return the user_token. If 
		the token is expired or missing 
		return the string 'expired token'.
		"""
		try:
			user_token = request.headers.get("user_token", None)
			secret = os.getenv('SECRET_KEY')
			return user_token
		except jwt.exceptions.ExpiredSignatureError:
			return "expired token"
	

	@property
	def get_corporate_id(self):
		"""
		Extract a corporate_id from the request.

		Check if the request has a corporate id in the
		body and return it. If the corporate id is not
		in the body check that the id is in the 
		user_token and return it if present.
		Else return False.
		"""
		try:
			corporate_id = self.data.get("corporate_id", None)
			if corporate_id:
				return corporate_id
			else:
				user_token = request.headers.get("user_token")
				secret = os.getenv('SECRET_KEY')
				decoded_token = jwt.decode(user_token, secret)
				corporate_id = decoded_token['corporate_id']		  
				return corporate_id
		except jwt.exceptions.DecodeError:
			return False
		except jwt.exceptions.ExpiredSignatureError:
			return False
			

	@property
	def get_admin_role(self):
		"""
		Extracts an admin_role from the request.

		Check if the request has an admin_role in the 
		body and return it. If the admin_role is not 
		in the body check that the id is in the 
		user_token and return it if present. Else return
		False. if the admin role is not in the dictionary
		called admin roles return invalid admin_role.
		"""
		try:
			admin_roles = 	{
								"client_staff":4, "client_admin":3, 
								"infotrace_admin":2, "super_admin":1
							}					
			admin_role = self.data.get("admin_role", None)
			if admin_role:
				if admin_role not in admin_roles.keys():
					return jsonify({"message": "Unknown admin role"})
				return admin_role
			else:
				user_token = request.headers.get("user_token", None)
				# use python-decouple to get secret key
				secret = os.getenv('SECRET_KEY')
				decoded_token = jwt.decode(user_token, secret)
				role = decoded_token['admin_role']
				if isinstance(role, str) and not role in admin_roles.keys():
					return jsonify({"message": "Unknown admin role"})
				elif isinstance(role, int) and not role in admin_roles.values():
					return jsonify({"message": "Unknown admin role"})	  
				return role
		except jwt.exceptions.DecodeError:
			return False
		except jwt.exceptions.ExpiredSignatureError:
			return False


	@property
	def get_admin_id(self):
		"""		
		Extracts an admin_id from the request.
		
		Check if the request has an admin_id in the 
		body and return it. If the corporate id is not
		in the body check that the id is in the 
		user_token and return it if present. Else return
		False.

		Args:
			None
		Returns:
			The admin_id(int) or False
		"""
		try:
			admin_id = self.data.get("admin_id", None)
			if admin_id:
				return admin_id
			else:
				user_token = request.headers.get("user_token", None)
				secret = os.getenv('SECRET_KEY')
				decoded_token = jwt.decode(user_token, secret)
				admin_id = decoded_token['admin_id']
				return admin_id
		except jwt.exceptions.DecodeError:
			return False
		except jwt.exceptions.ExpiredSignatureError:
			return False


	@property
	def get_admin_status(self):
		"""
		Extracts an admin_status from the request.
		
		Check if the request has an admin_status in the 
		body and return it. If the corporate id is not 
		in the body check that the id is in the header 
		and return it if present. Else return False.
		Args:
			None
		Returns:
			The status_id(str) if extracted from the body
			status_id(int) if extracted from the header
			False if the token is not valid or missing
		"""
		try:
			admin_status = self.data.get("admin_status", None)
			if admin_status:
				return admin_status
			else:
				user_token = request.headers.get("user_token", None)
				# use python-decouple to get secret key
				secret = os.getenv('SECRET_KEY')
				decoded_token = jwt.decode(user_token, secret)
				admin_status = decoded_token['admin_status']		  
				return admin_status
		except jwt.exceptions.DecodeError:
			return False
		except jwt.exceptions.ExpiredSignatureError:
			return False
