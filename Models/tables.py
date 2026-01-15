import datetime


from datetime import timedelta

from sqlalchemy import (
							Column,
							Integer,
							String,
							exc,
							Table,
							ForeignKey,
							Float, inspect,
							and_)
from sqlalchemy.orm import relationship, sessionmaker


from Models.__init__ import db


class Roles(db.Model):
	"""
	This table stores all the roles in the database
	"""
	__tablename__ = 'Roles'
	role_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	role_name = db.Column(
							String(500),
							default="client_staff",
							nullable=False,
							unique=True)
	role_date_created = db.Column(
									db.DateTime,
									default=datetime.datetime.now(),
									nullable=False
								  )
	role_admins_relation = db.relationship(
											"Administrators",
											backref='Roles',
											cascade="all, delete-orphan",
											passive_deletes=True
										 )
	@classmethod
	def get_by_role_id(cls, role_id):
		"""
		
		Query user by their user_id
		
		Args:
			role_id(int): The role id from this table
		Returns:
			An sqlalchemy query.

		"""
		sql_query = (db.session.query(Roles).
					filter(Roles.role_id==role_id).first())
		db.session.commit()
		return 


class Status(db.Model):
	"""
	
	The status id for the application
	
	"""
	__tablename__ = 'Status'
	status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	status_name= db.Column(
								String(500),
								default="awaiting_approval",
								nullable = False,
								unique=True
						   )
	status_date_created = db.Column(
										db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
								   )
	status_admins_relation = db.relationship(
												"Administrators",
												backref='Status',
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	status_corp_relation = db.relationship(
												"Corporates",
												backref='Status',
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	@classmethod
	def get_by_status_id(cls, status_id):
		"""Query user by their user_id."""
		sql_query = (db.session.query(Status).
					filter(Status.status_id==status_id).first())
		db.session.commit()
		return sql_query


class ScoreTypes(db.Model):
	"""
	
	"""
	__tablename__ = 'ScoreTypes'
	service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	score_name= db.Column(
								String(500),
								nullable = False,
								unique=True
						   )
	cost_of_score = db.Column(Float, nullable=False)
	score_date_created = db.Column(
										db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
								   )
	score_deductions_rel = db.relationship(
												"ClientDeductions",
												backref='ScoreTypes',
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	@classmethod
	def get_by_score_name(cls, score_name):
		"""Query user by their user_id"""
		(db.session.query(ScoreTypes).
					filter(ScoreTypes.score_name==score_name).first())
		db.session.commit()
		return sql_query


class Users(db.Model):
	"""
	Stores unique details for every db user administrators and clients.
	"""
	__tablename__ = 'Users'
	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_identity = db.Column(db.Integer, nullable=False, unique=True)
	user_names = db.Column(String(500), nullable = False, unique=False)
	user_date_created = db.Column(
									db.DateTime,
									default=datetime.datetime.now(),
									nullable=False
								  )
	user_admin_relation = db.relationship(
											"Administrators",
											backref="Users",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )
	user_client_relation = db.relationship(
											"ClientAdmins",
											backref="Users",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )

	@classmethod
	def get_by_user_id(cls, user_id):
		"""Query user by their user_id"""
		sql_query = (db.session.query(Users).
						filter(Users.user_id==user_id).first())
		db.session.commit()
		return sql_query

	@classmethod
	def get_by_user_identity(cls, user_identity):
		"""Querry the user by their identity"""
		sql_query = (db.session.query(Users).
					filter(Users.user_identity==user_identity).first())
		db.session.commit()
		return sql_query


class Administrators(db.Model):
	"""
	
	"""
	__tablename__ = 'Administrators'
	admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	admin_email = db.Column(String(500), nullable = False, unique=True)
	admin_password = db.Column(String(500), nullable = False)
	admin_date_created = db.Column(
									db.DateTime,
									default=datetime.datetime.now(),
									nullable=False
								  )
	role_id = db.Column(
							db.Integer,
							db.ForeignKey('Roles.role_id',
											ondelete='CASCADE'),
							nullable = False
						)
	status_id = db.Column(
							db.Integer,
							db.ForeignKey('Status.status_id',
							ondelete='CASCADE'),
							nullable = False
						  )
	user_id = db.Column(
							db.Integer,
							db.ForeignKey('Users.user_id',
							ondelete='CASCADE'),
							nullable = False
						)
	corporate_id = db.Column(db.Integer, default=1)
	admins_logged_relation = db.relationship(
												"LoggedAdmins",
												backref="Administrators",
												cascade="all, delete-orphan",
												passive_deletes=True
											 )
	

	@classmethod
	def get_admin_by_id(cls, admin_id):
		"""Query user by their user_id"""
		sql_query = (db.session.query(Administrators).
					filter(Administrators.admin_id==admin_id).first())
		db.session.commit()
		return sql_query

	@classmethod
	def get_admin_by_email(cls, admin_email):
		"""Query the Administrators by their email address"""
		sql_query = (db.session.query(Administrators).
					filter(Administrators.admin_email==admin_email).first())
		db.session.commit()
		return sql_query


class Corporates(db.Model):
	"""
	Null indicates that a corporate has not been checked or approved.
	After being checked or approved the column is updated with
	the id for the admin who did the cehcking and approval.
	"""
	__tablename__ = 'Corporates'
	corporate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	corporate_pin = db.Column(String(500), unique=True, nullable=False)
	corporate_name = db.Column(String(500), nullable = False, unique=True)
	status_id = db.Column(
							db.Integer,
							db.ForeignKey('Status.status_id',
											ondelete='CASCADE'),
							nullable=False,
							default=1
						  )

	created_by = db.Column(
								db.Integer,
								db.ForeignKey('Administrators.admin_id',
												ondelete='CASCADE'),
								nullable=False
							)
	corporate_date_created = db.Column(
										db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
									  )
	corp_kyc_relation = db.relationship(
											"KycData",
											backref="Corporates",	
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	corp_deposits_relation = db.relationship(
												"DepositsData",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True
											 )
	corp_savings_relation = db.relationship(
												"SavingsData",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	corp_withdrawals_relation = db.relationship(
												"WithdrawalsData",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True
												)
	corp_loans_relation = db.relationship(
											"LoansData",
											backref="Corporates",
											cascade="all, delete-orphan",
											passive_deletes=True
										 )
	corp_installments_relation = db.relationship(
												  "InstallmentsData",
												  backref="Corporates",
												  cascade="all, delete-orphan",
												  passive_deletes=True
												)
	corp_mpesa_relation = db.relationship(
											"MpesaData",
											backref="Corporates",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )
	corp_image_relation = db.relationship(	
											"ImageData",
											backref="Corporates",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )
	corp_message_relation = db.relationship(
												"MessageData",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True)
	corp_music_relation = db.relationship(
											"MusicData",
											backref="Corporates",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )
	corp_video_relation = db.relationship(
											"VideoData",
											backref="Corporates",
											cascade="all, delete-orphan",
											passive_deletes=True
										 )
	corp_score_relation = db.relationship(
											"CreditScores",
											backref="Corporates",
											cascade="all, delete-orphan",
											passive_deletes=True,
										 )
	corp_payment_relation = db.relationship(
												"ClientPayments",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	corp_wallet_relation = db.relationship(
												"ClientWallet",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	corp_deduction_relation = db.relationship(
												"ClientDeductions",
												backref="Corporates",
												cascade="all, delete-orphan",
												passive_deletes=True
											  )

	@classmethod
	def get_corporate_by_pin(cls, corporate_pin):
		"""Query user by their corporate_pin"""
		sql_query = (db.session.query(Corporates).
					filter(Corporates.corporate_pin==corporate_pin).first())
		db.session.commit()
		return sql_query

	@classmethod
	def get_corp_by_name(cls, corporate_name):
		"""Query the Adminostrators by their email address"""
		sql_query = (db.session.query(Corporates).
					filter(Corporates.corporate_name==corporate_name).first())
		db.session.commit()
		return sql_query

	@classmethod
	def get_corp_by_id(cls, corporate_id):
		"""Query user by their corporate_pin"""
		sql_query = (db.session.query(Corporates).
					filter(Corporates.corporate_id==corporate_id).first())
		db.session.commit()
		return sql_query


class ClientAdmins(db.Model):
	"""
	We cannot add a checked by and an approved by columns to this table
	because we need those columns to be related with the admin_id, which
	is in this table. 

	"""
	__tablename__ = 'ClientAdmins'
	client_id = db.Column(db.Integer, nullable=False, primary_key=True)
	client_email = db.Column(String(500), nullable = False, unique=True)
	client_password = db.Column(String(500), nullable = False)
	client_date_created = db.Column(
									db.DateTime,
									default=datetime.datetime.now(),
									nullable=False
								  )
	role_id = db.Column(
							db.Integer,
							db.ForeignKey('Roles.role_id',
											ondelete='CASCADE'),
							nullable = False
						)
	status_id = db.Column(
							db.Integer,
							db.ForeignKey('Status.status_id',
							ondelete='CASCADE'),
							nullable = False
						  )
	user_id = db.Column(
							db.Integer,
							db.ForeignKey('Users.user_id',
											ondelete='CASCADE'),
							nullable = False,
							unique = False
						)
	corporate_id = db.Column(
								db.Integer,
								db.ForeignKey(Corporates.corporate_id,
									ondelete='CASCADE'),
								nullable = False,
								unique = False
								)
	corp_client = db.relationship("Corporates", foreign_keys=[corporate_id])
	
	client_logs_relation = db.relationship(
												"LoggedClients",
												backref="ClientAdmins",
												cascade="all, delete-orphan",
												passive_deletes=True
											 )

	@classmethod
	def get_client_by_id(cls, client_id):
		"""Query user by their corporate_pin"""
		sql_query = (db.session.query(ClientAdmins).
					filter(ClientAdmins.client_id==client_id).first())
		db.session.commit()
		return sql_query


	@classmethod
	def get_client_by_email(cls, client_email):
		"""Query the Adminostrators by their email address"""
		sql_query = (db.session.query(ClientAdmins).
					filter(ClientAdmins.client_email==client_email).first())
		db.session.commit()
		return sql_query


class AdminApprovals(db.Model):
	"""
	This table tells us whether or not a user has been approved and
	who made the approval.
	"""
	__tablename__ = 'AdminApprovals'
	approval_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# who is being approved
	admin_being_approved = db.Column(		
									  db.Integer,
									  db.ForeignKey('Users.user_id',
														 ondelete='CASCADE'),
									  nullable=False,
									  unique=False
									)
	"""Who is doing the approval"""
	approver_id = db.Column(		
								db.Integer,
								db.ForeignKey('Users.user_id',
													ondelete='CASCADE'),
								nullable=False,
								unique=False
							)
	approved_from = db.Column(db.Integer, db.ForeignKey(Status.status_id))
	approved_to = db.Column(db.Integer, db.ForeignKey(Status.status_id))

	status_approved_from = db.relationship("Status", foreign_keys=[approved_from])					  
	status_approved_to = db.relationship("Status", foreign_keys=[approved_to])
	approval_date_created = db.Column(
										db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
									  )


class AdminChecks(db.Model):
	"""This table tells us whether an admin has been checked by an infotrace
	employee and who did the checking. A detail is moved to this table
	only after the user is checked."""
	__tablename__ = 'AdminChecks'
	check_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# Who is being checked
	client_being_checked = db.Column(		
										db.Integer,
										db.ForeignKey('Users.user_id',
										ondelete='CASCADE'),
										nullable=False,
										unique=False
									)
	# Who is doing the checking
	checker_id = db.Column(		
								db.Integer,
								db.ForeignKey('Users.user_id',
								ondelete='CASCADE'),
								nullable = False,
								unique=False
						   )
	checked_from = db.Column(db.Integer, db.ForeignKey(Status.status_id))
	checked_to = db.Column(db.Integer, db.ForeignKey(Status.status_id))

	status_checked_from = db.relationship("Status",	foreign_keys=[checked_from])
	status_checked_to = db.relationship("Status", foreign_keys=[checked_to])
	checked_date_created = db.Column( db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
									)


class CorporateChecks(db.Model):
	"""
	This table tells us whether an admin has been checked by an infotrace
	employee and who did the checking. A detail is moved to this table
	only after the user is checked."""
	__tablename__ = 'CorporateChecks'
	check_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# Which company is being checked
	corp_being_checked = db.Column(		
										db.Integer,
										db.ForeignKey('Corporates.corporate_id',
										ondelete='CASCADE'),
										nullable=False,
										unique=False
									)
	# Who is doing the checking
	checker_id = db.Column(		
									db.Integer,
									db.ForeignKey('Users.user_id',
									ondelete='CASCADE'),
									nullable = False,
									unique=False
								)
	checked_from = db.Column(db.Integer, db.ForeignKey(Status.status_id))
	checked_to = db.Column(db.Integer, db.ForeignKey(Status.status_id))

	status_checked_from = db.relationship("Status",	foreign_keys=[checked_from])
	status_checked_to = db.relationship("Status", foreign_keys=[checked_to])
	checked_date_created = db.Column( db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
									)

	@classmethod
	def get_by_corp_id(cls, corp_id):
		"""Query the Adminostrators by their email address"""
		sql_query = (
						db.session.query(CorporateChecks).
						filter(CorporateChecks.corp_being_checked==corp_id).
						first()
					)
		db.session.commit()
		return sql_query

class CorporateApprovals(db.Model):
	"""
	This table tells us whether or not a user has been approved and
	who made the approval.
	"""
	__tablename__ = 'CorporateApprovals'
	approval_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# which company is being approved
	corp_being_approved = db.Column(		
									  db.Integer,
									  db.ForeignKey('Corporates.corporate_id',
														 ondelete='CASCADE'),
									  nullable=False,
									  unique=False
									)
	# Who is doing the approval
	approver_id = db.Column(		
								db.Integer,
								db.ForeignKey('Users.user_id',
													ondelete='CASCADE'),
								nullable=False,
								unique=False
							)
	approved_from = db.Column(db.Integer, db.ForeignKey(Status.status_id))
	approved_to = db.Column(db.Integer, db.ForeignKey(Status.status_id))

	status_approved_from = db.relationship(
											"Status",
											foreign_keys=[approved_from]
											)					  
	status_approved_to = db.relationship("Status", foreign_keys=[approved_to])
	approval_date_created = db.Column(
										db.DateTime,
										default=datetime.datetime.now(),
										nullable=False
									  )

	@classmethod
	def get_by_corp_id(cls, corp_id):
		"""Query the Adminostrators by their email address"""
		sql_query = (	
						db.session.query(CorporateApprovals).
						filter(CorporateApprovals.corp_being_approved==corp_id).
						first()
				    )
		db.session.commit()
		return sql_query





class Borrowers(db.Model):
	__tablename__ = 'Borrowers'
	borrower_id = db.Column(db.Integer, primary_key=True)
	borrower_date_of_birth = db.Column(db.DateTime)
	borrower_county = db.Column(String(200), nullable = False)
	borrower_gender =   db.Column(String(10), nullable = False)
	borrower_date_created = db.Column(db.DateTime,
									  default=datetime.datetime.now())
	bor_kyc_relation = db.relationship(
											"KycData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
									   )
	bor_deposits_relation = db.relationship(
												"DepositsData",
												backref="Borrowers",
												cascade="all, delete-orphan",
												passive_deletes=True
											)
	bor_savings_relation = db.relationship(
											"SavingsData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )
	bor_withdrawals_relation = db.relationship(
												"WithdrawalsData",
												backref="Borrowers",
												cascade="all, delete-orphan",
												passive_deletes=True
											  )
	bor_loans_relation = db.relationship(
											"LoansData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	bor_instals_relation = db.relationship(
											"InstallmentsData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										  )
	bor_mpesa_relation = db.relationship(
											"MpesaData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	bor_image_relation = db.relationship(
											"ImageData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	bor_message_relation = db.relationship(
											"MessageData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										   )
	bor_music_relation = db.relationship(
											"MusicData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	bor_video_relation = db.relationship(
											"VideoData",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	bor_score_relation = db.relationship(
											"CreditScores",
											backref="Borrowers",
											cascade="all, delete-orphan",
											passive_deletes=True
										)
	@classmethod
	def borrower_by_id(cls, borrower_id):
		"""Query the Adminostrators by their email address"""
		sql_query = (	
						db.session.query(Borrowers).
						filter(Borrowers.borrower_id==borrower_id).
						first()
				    )
		db.session.commit()		
		borrower = sql_query.borrower_id
		return borrower


###############################################################################
class LoggedAdmins(db.Model):
	__tablename__ = 'LoggedAdmins'
	loggedId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	admin_id =  db.Column(
							db.Integer,
							 db.ForeignKey('Administrators.admin_id',
											 ondelete='CASCADE')
						  )
	logInDate = db.Column(db.DateTime, default=datetime.datetime.now())
	logoutDate = db.Column(	
								db.DateTime,
								default=datetime.datetime.now() +
										 timedelta(minutes=200)
							)
	
	

class LoggedClients(db.Model):
	__tablename__ = 'LoggedClients'
	loggedId = db.Column(db.Integer, autoincrement=True, primary_key=True)
	client_id =  db.Column(
							db.Integer,
							 db.ForeignKey('ClientAdmins.client_id',
											 ondelete='CASCADE')
						  )
	logInDate = db.Column(db.DateTime, default=datetime.datetime.now())
	logoutDate = db.Column(	
								db.DateTime,
								default=datetime.datetime.now() +
										 timedelta(minutes=200)
							)

class BlacklistedTokens(db.Model):
	__tablename__ = 'BlacklistedTokens'
	token_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	token = db.Column(String(500), nullable = False)
	time_blacklisted = db.Column(db.DateTime, default=datetime.datetime.now())

	@classmethod
	def get_by_token(cls, token):
		"""Query table by token"""
		sql_query = (
						db.session.query(BlacklistedTokens).
						filter(BlacklistedTokens.token==token).first()
					)
		db.session.commit()
		return sql_query


class KycData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'KycData'
	kyc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
									db.Integer,
									db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
								 )
	corporate_id = db.Column(
								db.Integer,
							 	db.ForeignKey('Corporates.corporate_id',
											ondelete='CASCADE')
							)
	borrower_phone_number = db.Column(db.String(12), nullable = True)
	kyc_default_status = db.Column(db.Integer, nullable=False)
	kyc_date_created = db.Column(db.DateTime, default=datetime.datetime.now())


	@classmethod
	def get_by_borrower_id(cls, borrower_id):
		"""
		Fetches all data belonging to a borrower from the Kyc table.
		
		Args:
			borrower_id (int): The national id of the borrower. 

		Returns:
			sql_querry: an sqlalchemy obejct.
		"""
		sql_query = (	
						db.session.query(Borrowers).
						filter(Borrowers.borrower_id==borrower_id).
						all()
				    )
		db.session.commit()
		return sql_query


class DepositsData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'DepositsData'
	deposit_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
									db.Integer,
									db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
								 )
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
							 ondelete='CASCADE'))
	date_of_deposit = db.Column(db.DateTime, nullable = True)
	deposit_channel = db.Column(String(200), nullable = True)
	deposit_amount = db.Column(db.Float, nullable = False)
	deposit_description = db.Column(String(200), nullable=False)
	deposit_date_created = db.Column(db.DateTime,
									 default=datetime.datetime.now())


class SavingsData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'SavingsData'
	savings_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
								ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
							 ondelete='CASCADE'))
	date_of_savings = db.Column(db.DateTime, nullable = True)
	savings_channel = db.Column(String(200), nullable = True)
	savings_amount = db.Column(db.Float, nullable = False)
	savings_type = db.Column(String(200), nullable=False)
	savings_date_created = db.Column(db.DateTime,
									 default=datetime.datetime.now())


class WithdrawalsData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'WithdrawalsData'
	withdrawals_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(db.Integer,
							db.ForeignKey('Borrowers.borrower_id',
							ondelete='CASCADE'))
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
							 ondelete='CASCADE'))
	date_of_withdrawals = db.Column(db.DateTime, nullable = True)
	withdrawals_channel = db.Column(String(200), nullable = True)
	withdrawals_amount = db.Column(db.Float, nullable = False)
	withdrawals_description = db.Column(String(200), nullable=False)
	withdrawals_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())


class LoansData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'LoansData'
	loan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	date_of_loan = db.Column(db.DateTime, nullable = False)
	loan_period = db.Column(db.Integer, nullable = False)
	loan_amount = db.Column(db.Float, nullable = False)
	loan_installment_frequency = db.Column(db.Integer, nullable=False)
	loan_interest = db.Column(db.Float, nullable = False)
	date_of_loan_completion = db.Column(db.DateTime, nullable = False)
	loan_date_created = db.Column(db.DateTime, default=datetime.datetime.now())
	loan_installments_relation = db.relationship(
												   "InstallmentsData",
												   backref="LoansData",
												   cascade="all, delete-orphan",
												   passive_deletes=True
												 )


class InstallmentsData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'InstallmentsData'
	installment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	installment_loan_id = db.Column(
										db.Integer,
									 	db.ForeignKey('LoansData.loan_id',
										ondelete='CASCADE')
									)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
														  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
							 ondelete='CASCADE'))
	date_of_installment = db.Column(db.DateTime, nullable = False)
	installment_amount = db.Column(db.Float, nullable = False)
	installment_loan_balance  = db.Column(db.Float, nullable = False)
	installment_type = db.Column(String(200), nullable=False)
	installment_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())

class MpesaData(db.Model):
	"""docstring for KycData"""
	__tablename__ = 'MpesaData'
	mpesa_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	mpesa_amount = db.Column(db.Float, nullable = False)
	mpesa_spec_loc = db.Column(String(200), nullable=False)
	mpesa_type = db.Column(String(200), nullable=False)
	mpesa_time_stamp = db.Column(db.DateTime, nullable = False)
	mpesa_date_created = db.Column(db.DateTime,
								   default=datetime.datetime.now())


class ImageData(db.Model):
	"""docstring for ImageData"""
	__tablename__ = 'ImageData'
	image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	image_size = db.Column(db.Float, nullable = False)
	image_file_type = db.Column(String(200), nullable=False)
	image_date_added = db.Column(db.DateTime, nullable = False)
	image_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())


class MessageData(db.Model):
	"""docstring for ImageData"""
	__tablename__ = 'MessageData'
	message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(	
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	message_length = db.Column(db.Float, nullable = False)
	message_type = db.Column(String(200), nullable=False)
	message_direction = db.Column(String(200), nullable=False)
	message_time_stamp = db.Column(db.DateTime, nullable = False)
	message_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())


class MusicData(db.Model):
	"""docstring for ImageData"""
	__tablename__ = 'MusicData'
	music_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	music_size = db.Column(db.Float, nullable = False)
	music_file_type = db.Column(String(200), nullable=False)
	music_date_added = db.Column(db.DateTime, nullable = False)
	music_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())


class VideoData(db.Model):
	"""docstring for ImageData"""
	__tablename__ = 'VideoData'
	video_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	video_size = db.Column(db.Float, nullable = False)
	video_file_type = db.Column(String(200), nullable=False)
	video_date_added = db.Column(db.DateTime, nullable = False)
	video_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())


###############################################################################
class CreditScores(db.Model):
	"""docstring for CreditScores"""
	__tablename__ = 'CreditScores'
	score_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	admin_id = db.Column(
							db.Integer, 
							db.ForeignKey(
											'Users.user_id',
											ondelete='CASCADE'
										 )
						)
	borrower_id = db.Column(
								db.Integer,
								db.ForeignKey('Borrowers.borrower_id',
													  ondelete='CASCADE')
							)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	credit_score = db.Column(db.Float, nullable = False)
	score_name = db.Column(String(200), nullable=False)
	credit_limit = db.Column(db.Float, nullable = False)
	score_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())


class ClientPayments(db.Model):
	"""Table contianing all payments."""
	__tablename__ = 'ClientPayments'
	payment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	corporate_id = db.Column(
								db.Integer,
								db.ForeignKey('Corporates.corporate_id',
											ondelete='CASCADE')
							 )
	payment_amount = db.Column(db.Float, nullable = False)
	uploaded_by = db.Column(
								db.Integer,
								db.ForeignKey('Administrators.admin_id',
												ondelete='CASCADE'),
								nullable=True
							)
	payment_date_created = db.Column(db.DateTime, nullable=True)
	aproved_by = db.Column(
							db.Integer,
							db.ForeignKey('Administrators.admin_id',
											ondelete='CASCADE'),
							nullable=True
						   )
	payment_date_approved = db.Column(db.DateTime, nullable=True)



class ClientWallet(db.Model):
	__tablename__ = 'ClientWallet'
	"""Table contianing the client wallet balance."""
	wallet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
											ondelete='CASCADE'))
	current_amount = db.Column(db.Float, nullable = False, default=0)
	amount_date_created = db.Column(db.DateTime,
										default=datetime.datetime.now())


class ClientDeductions(db.Model):
	"""Table contianing all deductions."""
	__tablename__ = 'ClientDeductions'
	deduction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	corporate_id = db.Column(db.Integer,
							 db.ForeignKey('Corporates.corporate_id',
										   ondelete='CASCADE'))
	amount_b4_deduction = db.Column(db.Float, nullable = False)
	amount_deducted = db.Column(db.Float, nullable = False)
	amount_after_deduction = db.Column(db.Float, nullable = False)
	service_id = db.Column(
							db.Integer,
							db.ForeignKey('ScoreTypes.service_id',
											ondelete='CASCADE'),
							nullable = False
						)
	deduction_date_created = db.Column(db.DateTime,
										 default=datetime.datetime.now())