import datetime, json


from sqlalchemy import exc


from Models.__init__ import db


from Models.tables import (
							Corporates,
							ClientPayments,
							ClientWallet,
							ScoreTypes, 
							CreditScores
					)


def approve_payment(approver_id, corporate_name, amount_uploaded):
	"""
	Approves a payment.

	Helper function used to approve a payment after it has been uploaded.
	Query client payment, filter where corporate name is corporate_name
	uploaded_by is not null, and approved_by is null. Update the approved_by
	column, then send the same amount to the client wallet table.

	Args:
		approver_id (int): The admin_id for the person approving the 
							payment.
		corporate_name (str): The company that has made the payment.
		amount_uploaded (float): The amount uploaded to the wallet

	Returns:
		boolean(bool): True for success.
		This company is not registered(str): If company is unknown.
	"""
	try:
		is_registered = (
						   db.session.query(Corporates).
						   filter(Corporates.corporate_name==corporate_name).
						   first()
						)
	except:
		db.session.rollback()
	if is_registered == None:
		return "This company is not registered."
	try:
		to_approve = (
						db.session.query(ClientPayments).
						filter(
								ClientPayments.corporate_name == corporate_name,
								ClientPayments.approved_by == None,
								ClientPayments.uploaded_by != None
							  )
					  )
	except:
		db.session.rollback()
	payment_id = to_approve.payment_id
	upload_to_wallet(amount_uploaded, is_registered.corporate_id)
	to_approve.approved_by = approver_id
	to_approve.payment_date_approved = datetime.datetime.now()
	db.session.commit()
	return True


def displayed_companies():
	"""
	Helper function used to display registered companies.

	This function does not require authentication to access it.
	Fetch all companies from the Corporates table, convert the
	result into a dictionary using a list comprehension, convert
	the resulting dictionary into a string dictinary. Finally,
	convert the result to json using json.loads

	This function can never return None because company data is
	inserted into the companies table when the app starts.

	TODO:
		Consider removing this endpoint or authenticating it
	Args:
		None
	Returns:
		dictionary(dict): dictionary in json format.
	"""
	all_companies = db.session.query(Corporates.corporate_name).all()
	# Create a string representation of a dictionary
	companies_list = json.dumps([row._asdict() for row in all_companies])
	# convert to json
	companies_list = json.loads(companies_list)
	return companies_list


def deduct_service_cost(score_name, corporate_id, admin_role):
	"""
	Deducts the cost of service from the wallet.

	Validation of a registered company and the score name is made
	in the make_payment endpoint. 

	To make a deduction find the current amount for the company from
	the ClientWallet table. Set the amount deducted as the cost
	of the score type, which is retrieved from the ScoreTypes table,
	get the current amount from the ClientWallet table, update the
	amount in the wallet, and update the ClientWallet and ClientDeductions
	tables
	
	Args:
		score_name (str): The type of score that is requested,
		corp_name (str): The name of the company that sent the request
	Returns:
		boolean(bool): True if the admin is an infotrace admin and 
						True after the deduction is made.

	"""
	is_correct_score = (
							db.session.query(ScoreTypes).
							filter(ScoreTypes.score_name == score_name).first()
						)
	fetched_amount = (
					   db.session.query(ClientWallet).
					   filter(ClientWallet.corporate_id == corporate_id).first()
					)
	
	amount_deducted = is_correct_score.cost_of_score
	if fetched_amount != None:
		amount_b4_deduction = fetched_amount.current_amount
	elif fetched_amount == None and admin_role not in [1,2]:
		return "Zero in account update your account."
	amount_b4_deduction = 0
	cost_of_score = is_correct_score.cost_of_score
	# Update the curent_amount in the ClientWallet
	if fetched_amount != None:
		fetched_amount.current_amount = amount_b4_deduction - cost_of_score
	# The company that is being deducted is below.
	amount_after_deduction = amount_b4_deduction - cost_of_score
	# if the admin_role is an infotrace_admin or superadmin don't deduct
	if admin_role == 2 or admin_role == 1:
		return True
	ed_user = ClientDeductions(
								corporate_id = corporate_id,
								amount_b4_deduction = amount_b4_deduction,
								amount_deducted = amount_deducted,
								amount_after_deduction = amount_after_deduction,
								service_id = is_correct_score.service_id
							)
	db.session.add(ed_user)
	db.session.commit()
	return True



def save_credit_score(borrower_id, corporate_id, credit_score, score_name,
						credit_limit):
	"""
	Saves the credit score to the CrediScores table.

	Args:
		borrower_id(int): The user_identity of the borrower
		corporate_id(int): The corporate id of the employee that did 
							the fetching.
		credit_score(str): The score from the client.
		score_name(str): The name of the score sought.
		credit_limit(float): The maximum recommended limit.
	Returns:
		boolean(bool): Always returns True
	"""
	credit_score = CreditScores(
									borrower_id = borrower_id,
									corporate_id = corporate_id,
									credit_score = credit_score,
									score_name = score_name,
									credit_limit = credit_limit
								)
	try:
		db.session.add(credit_score)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		return False


# def upload_payment(uploader_id, corporate_name, amount_uploaded):
# 	"""
# 	Uploads the amount to the table.

# 	Helper function used to upload a payment in the database.
# 	Confirms that the coporate_name is registered before uploading
# 	the payment to the database.

# 	Args:
# 		uploader_id (int): The Infotrace admin uploading the payment.
# 		corporate_name: The company that owns the payment.
# 	Returns:
# 		boolean(bool): True for success.
# 		This company is not registered(str): If company is unknown.
# 	"""
# 	is_registered = (
# 					   db.session.query(Corporates).
# 					   filter(Corporates.corporate_name==corporate_name).first()
# 					)
# 	if is_registered_corp == None:
# 		return {
# 					"status": False,
# 					"message":"This company is not registered."
# 				}

# 	corporate_id = is_registered_corp.corporate_id
# 	paid = ClientPayments(
# 							corporate_id = corporate_id,
# 							payment_amount = amount_uploaded,
# 							uploaded_by = uploader_id,
# 							payment_date_created = datetime.datetime.now()
# 						 )
# 	try:
# 		db.session.add(ed_user)
# 		db.session.commit()
# 		return True
# 	except exc.IntegrityError as e:
# 		db.session().rollback()
# 		return False

def enter_payment(uploader_id, corporate_name, amount_uploaded):
	"""
	Uploads the amount to the table.

	Helper function used to upload a payment in the database.
	Confirms that the coporate_name is registered before uploading
	the payment to the database.

	Args:
		uploader_id (int): The Infotrace admin uploading the payment.
		corporate_name: The company that owns the payment.
	Returns:
		boolean(bool): True for success.
		This company is not registered(str): If company is unknown.
	"""
	is_registered = (
					   db.session.query(Corporates).
					   filter(Corporates.corporate_name==corporate_name).
					   first()
					)
	if is_registered == None:
		return {
					"status": False,
					"message":"This company is not registered."
				}

	corporate_id = is_registered.corporate_id
	paid = ClientPayments(
							corporate_id = corporate_id,
							payment_amount = amount_uploaded,
							uploaded_by = uploader_id,
							payment_date_created = datetime.datetime.now()
						 )
	try:
		db.session.add(paid)
		db.session.commit()
		return True
	except exc.IntegrityError as e:
		db.session().rollback()
		return False




def upload_to_wallet(amount_uploaded, corporate_id):
	"""
	Uploads payments to the wallet.

	Check if the company already has money in the wallet, if not insert the
	money in the wallet. If money is in the wallet take that amount in the
	wallet and add the amount that has been uploaded.

	Args:
		amount_uploaded (float): The amount uploaded to the wallet.
		corporate_id (int): The corporate_id for the paying company.
	Returns:
		boolean(bool): Always returns True.
	"""
	fetched_amount = (
					   db.session.query(ClientWallet).
					   filter(ClientWallet.corporate_id == corporate_id).first()
					)
	if fetched_amount != None:
		remaining_amount = fetched_amount.current_amount
		total_amount = remaining_amount + amount_uploaded
		fetched_amount.current_amount = total_amount
	if fetched_amount == None:
		fetched_amount.current_amount = amount_uploaded
	db.session.commit()
	return True
