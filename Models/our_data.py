# TODO consider a situation where the borrower county has changed.
import datetime
import pandas as pd
import numpy as np

from dateutil.relativedelta import relativedelta
from sqlalchemy import inspect
from sqlalchemy import exc

from Models.__init__ import db

from Models.others import check_borrower
from Models.tables import(
									Borrowers,
									DepositsData,
									ImageData,
									InstallmentsData,
									KycData,
									MessageData,
									MpesaData,
									MusicData,
									LoansData,
									SavingsData,
									VideoData,
									WithdrawalsData
								)

def object_as_dict(obj):
	"""
	This function is used to convert an sqlalchemy query from a
	list to a dictionary.
	"""
	return {c.key: getattr(obj, c.key)
			for c in inspect(obj).mapper.column_attrs}


def confirm_no_duplicate_kyc(borrower_id):
	"""
	Confirms that a user does not belong to the same corporate twice.
	
	Given a borrower identity fetch the borrowers detail from the
	KycData table. Check if the corporate trying to register the 
	borrower has already registered the borrower if so return False
	and return True otherwise.

	Args:
		borrower_id(int): 
	
	
	"""
	already_existing = []
	sql_query = (
					db.session.query(KycData).
					filter(KycData.borrower_id==borrower_id).
					all()
				)
	for item in sql_query:
		if item.corporate_id in already_existing:
			return False
		already_existing.append(item.corporate_id)
	return True


def push_kyc_to_db(borrower_id, data, user_index):
	registered_borrower = check_borrower(data['borrower_id'][user_index])
	try:
		if registered_borrower is False:
			ed_borrower = Borrowers(
							borrower_id = data['borrower_id'][user_index],
							borrower_gender = data['borrower_gender'][user_index],
							borrower_date_of_birth = data['borrower_date_of_birth'][user_index],
							borrower_county = data['borrower_county'][user_index]
									)
			db.session.add(ed_borrower)
			ed_kyc = KycData(
						borrower_id = data['borrower_id'][user_index],
						corporate_id = data['corporate_id'][user_index],
						kyc_default_status = data['kyc_default_status'][user_index],
						borrower_phone_number = data['borrower_phone_number'][user_index],
						kyc_date_created = data['kyc_date_created'][user_index]
						)
			db.session.add(ed_kyc)
		# If the we already have the borrower details
		elif registered_borrower != Fals:
			ed_kyc = KycData(
						borrower_id = data['borrower_id'][user_index],
						corporate_id = data['corporate_id'][user_index],
						kyc_default_status = data['kyc_default_status'][user_index],
						borrower_phone_number = data['borrower_phone_number'][user_index],
						kyc_date_created = data['kyc_date_created'][user_index]
						)
			db.session.add(ed_kyc)
		db.session.commit()
		return True
	except exc.IntegrityError:
		db.session.rollback()
		return False


def push_deposits_to_db(data, user_index):
	try:
		ed_kyc = DepositsData(
					borrower_id = data['borrower_id'][user_index],
					corporate_id = data['corporate_id'][user_index],
					deposit_channel = data['deposit_channel'][user_index],
					date_of_deposit =data['date_of_deposit'][user_index],
					deposit_amount =data['deposit_amount'][user_index],
					deposit_description = data['deposit_description'][user_index]
					)
		db.session.add(ed_kyc)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		return False


def push_savings_to_db(data, user_index):
	try:
		ed_kyc = SavingsData(
					borrower_id = data['borrower_id'][user_index],
					corporate_id = data['corporate_id'][user_index],
					savings_channel = data['savings_channel'][user_index],
					date_of_savings =data['date_of_savings'][user_index],
					savings_amount =data['savings_amount'][user_index],
					savings_type = data['savings_type'][user_index]
					)
		db.session.add(ed_kyc)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		return False


def push_withdrawals_to_db(data, user_index):
	try:
		ed_kyc = WithdrawalsData(
					borrower_id = data['borrower_id'][user_index],
					corporate_id = data['corporate_id'][user_index],
					withdrawals_channel = data['withdrawals_channel'][user_index],
					date_of_withdrawals =data['date_of_withdrawals'][user_index],
					withdrawals_amount =data['withdrawals_amount'][user_index],
					withdrawals_description = data['withdrawals_description'][user_index]
					)
		db.session.add(ed_kyc)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		return False


def push_loans_to_db(data, user_index):
	try:
		ed_kyc = ed_kyc = LoansData(
					borrower_id = data['borrower_id'][user_index],
					corporate_id = data['corporate_id'][user_index],
					date_of_loan =data['date_of_loan'][user_index],
					loan_amount = data['loan_amount'][user_index],
					loan_interest = data['loan_interest'][user_index],
					loan_period = data['loan_period'][user_index],
					loan_installment_frequency = data['loan_installment_frequency'][user_index],
					date_of_loan_completion = data['date_of_loan_completion'][user_index]
					)
		db.session.add(ed_kyc)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		return False


def push_installments_to_db(data, user_index):
	try:
		ed_kyc = InstallmentsData(
				installment_loan_id = data['installment_loan_id'][user_index],
				borrower_id = data['borrower_id'][user_index],
				corporate_id = data['corporate_id'][user_index],
				date_of_installment =data['date_of_installment'][user_index],
				installment_amount = data['installment_amount'][user_index],
				installment_loan_balance = data['installment_loan_balance'][user_index],
				installment_type = data['installment_type'][user_index]
				)
		db.session.add(ed_kyc)
		db.session.commit()
		return True
	except Exception as e:
		db.session.rollback()
		return False

todays_date = datetime.datetime.today()
three_months_ago = todays_date - relativedelta(months=3)



class FetchedData():
	"""docstring for FetchedData"""
	def __init__(self, borrower_id, corporate_id=None):
		self.borrower_id = borrower_id
		self.corporate_id = corporate_id


	def filter_last_n_months(self, df, n_moths, column_to_filter):
		"""Sort dataframe by date column then select rows for the last 
		three months then drop any columns containinng date_created."""
		df_sorted = (
						df.sort_values(by=str(column_to_filter), ascending=True)
						.set_index(str(column_to_filter))
						.last(str(n_moths)+"M")
					).reset_index()
		df_sorted = df_sorted[
								df_sorted.columns.drop(
								list(df_sorted.filter(regex='date_created'))
								)
							 ]
		return df_sorted

		
	def fetch_kyc_data(self):
		user_data = KycData.query.filter(
									KycData.borrower_id == self.borrower_id,
									KycData.corporate_id == self.corporate_id	
										)
		df = pd.read_sql(user_data.statement, user_data.session.bind)		
		db.session.commit()
		df['kyc_id'] = df['kyc_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['kyc_default_status'] = df['kyc_default_status'].astype(str).astype(int)
		df['kyc_date_created'] = pd.to_datetime(df['kyc_date_created'])
		return df


	def fetch_borrower_data(self):
		user_data = Borrowers.query.filter(
									Borrowers.borrower_id == self.borrower_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['borrower_date_of_birth'] = pd.to_datetime(df['borrower_date_of_birth'])
		df['borrower_county'] = df['borrower_county'].astype(str)
		df['borrower_gender'] = df['borrower_gender'].astype(str)
		df['borrower_date_created'] = pd.to_datetime(df['borrower_date_created'])
		return df

	def fetch_deposits_data(self):
		user_data = DepositsData.query.filter(
								DepositsData.borrower_id == self.borrower_id,
								DepositsData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['deposit_id'] = df['deposit_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['date_of_deposit'] = pd.to_datetime(df['date_of_deposit'])
		df['deposit_channel'] = df['deposit_channel'].astype(str)
		df['deposit_amount'] = df['deposit_amount'].astype(str).astype(float)
		df['deposit_description'] = df['deposit_description'].astype(str)
		df['deposit_date_created'] = pd.to_datetime(df['deposit_date_created'])
		df = self.filter_last_n_months(df, 3, "date_of_deposit")
		if df.empty:
			df = df.append(
							{'deposit_id': 1, 
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'date_of_deposit': datetime.datetime.now(),
							 'deposit_channel': 'missing',
							 'deposit_amount': 0,
							 'deposit_description': 'missing'
							}, ignore_index=True)
		return df


	def fetch_savings_data(self):
		user_data = SavingsData.query.filter(
								SavingsData.borrower_id == self.borrower_id,
								SavingsData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['savings_id'] = df['savings_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['date_of_savings'] = pd.to_datetime(df['date_of_savings'])
		df['savings_channel'] = df['savings_channel'].astype(str)
		df['savings_amount'] = df['savings_amount'].astype(str).astype(float)
		df['savings_type'] = df['savings_type'].astype(str)
		df['savings_date_created'] = pd.to_datetime(df['savings_date_created'])
		df = self.filter_last_n_months(df, 3, "date_of_savings")
		if df.empty:
			df = df.append(
							{'savings_id': 1, 
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'date_of_savings': datetime.datetime.now(),
							 'savings_channel': 'missing',
							 'savings_amount': 0,
							 'savings_type': 'missing',
							 'savings_date_created':datetime.datetime.now()
							}, ignore_index=True)
		return df


	def fetch_withdrawal_data(self):
		user_data = WithdrawalsData.query.filter(
							WithdrawalsData.borrower_id == self.borrower_id,
							WithdrawalsData.corporate_id == self.corporate_id	
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['withdrawals_id'] = df['withdrawals_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['date_of_withdrawals'] = pd.to_datetime(df['date_of_withdrawals'])
		df['withdrawals_channel'] = df['withdrawals_channel'].astype(str)
		df['withdrawals_amount'] = df['withdrawals_amount'].astype(str).astype(float)
		df['withdrawals_description'] = df['withdrawals_description'].astype(str)
		df['withdrawals_date_created'] = pd.to_datetime(df['withdrawals_date_created'])
		df = self.filter_last_n_months(df, 3, "date_of_withdrawals")
		if df.empty:
			df = df.append(
							{'withdrawals_id': 1, 
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'date_of_withdrawals': datetime.datetime.now(),
							 'withdrawals_channel': 'missing',
							 'withdrawals_amount': 0,
							 'withdrawals_description': 'missing'
							}, ignore_index=True)
		return df


	def fetch_loans_data(self):
		user_data = LoansData.query.filter(
									LoansData.borrower_id == self.borrower_id,
									LoansData.corporate_id == self.corporate_id
										   )
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['loan_id'] = df['loan_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['loan_period'] = df['loan_period'].astype(str).astype(int)
		df['loan_amount'] = df['loan_amount'].astype(str).astype(float)
		df['loan_installment_frequency'] = df['loan_installment_frequency'].astype(str).astype(int)
		df['loan_interest'] = df['loan_interest'].astype(str).astype(float)
		df['date_of_loan_completion'] = pd.to_datetime(df['date_of_loan_completion'])
		df['loan_date_created'] = pd.to_datetime(df['loan_date_created'])
		df = self.filter_last_n_months(df, 3, "date_of_loan")
		if df.empty:
			df = df.append(
							{'loan_id': 1, 
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'date_of_loan': datetime.datetime.now(),
							 'loan_period': 'missing',
							 'loan_amount': 0,
							 'loan_interest': 0,
							 'loan_installment_frequency': 'missing',
							 'date_of_loan_completion': datetime.datetime.now()
							}, ignore_index=True)
		return df

	def fetch_installments_data(self):
		user_data = InstallmentsData.query.filter(
							InstallmentsData.borrower_id == self.borrower_id,
							InstallmentsData.corporate_id == self.corporate_id
						)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['installment_id'] = df['installment_id'].astype(str).astype(int)
		df['installment_loan_id'] = df['installment_loan_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['installment_amount'] = df['installment_amount'].astype(str).astype(float)
		df['installment_loan_balance'] = df['installment_loan_balance'].astype(str).astype(float)
		df['installment_type'] = df['installment_type'].astype(str)
		df['date_of_installment'] = pd.to_datetime(df['date_of_installment'])
		df['installment_date_created'] = pd.to_datetime(df['installment_date_created'])
		df = self.filter_last_n_months(df, 3, "date_of_installment")
		if df.empty:
			df = df.append(
							{'installment_id': 1,
							 'installment_loan_id': 1,
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'date_of_installment': datetime.datetime.now(),
							 'installment_amount': 0,
							 'installment_loan_balance': 0,
							 'installment_type': 'missing'
							}, ignore_index=True)
		return df

	def fetch_mpesa_data(self):
		user_data = MpesaData.query.filter(
									MpesaData.borrower_id == self.borrower_id,
									MpesaData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['mpesa_id'] = df['mpesa_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['mpesa_amount'] = df['mpesa_amount'].astype(str).astype(float)
		df['mpesa_spec_loc'] = df['mpesa_spec_loc'].astype(str)
		df['mpesa_type'] = df['mpesa_type'].astype(str)
		df['mpesa_time_stamp'] = pd.to_datetime(df['mpesa_time_stamp'])
		df['mpesa_date_created'] = pd.to_datetime(df['mpesa_date_created'])
		df = self.filter_last_n_months(df, 3, "mpesa_time_stamp")
		if df.empty:
			df = df.append(
							{'mpesa_id': 1,
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'mpesa_amount': 0,
							 'mpesa_spec_loc': 'missing',
							 'mpesa_type': 'missing',
							 'mpesa_time_stamp': datetime.datetime.now()
							}, ignore_index=True)
		return df

	def fetch_image_data(self):
		user_data = ImageData.query.filter(
									ImageData.borrower_id == self.borrower_id,
									ImageData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['image_id'] = df['image_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['image_size'] = df['image_size'].astype(str).astype(float)
		df['image_file_type'] = df['image_file_type'].astype(str)
		df['image_date_added'] = pd.to_datetime(df['image_date_added'])
		df['image_date_created'] = pd.to_datetime(df['image_date_created'])
		df = self.filter_last_n_months(df, 3, "image_date_added")
		if df.empty:
			df = df.append(
							{'image_id': 1,
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'image_size': 0,
							 'image_file_type': 'missing',
							 'image_date_added': datetime.datetime.now()
							}, ignore_index=True)
		return df

	def fetch_message_data(self):
		user_data = MessageData.query.filter(
								MessageData.borrower_id == self.borrower_id,
								MessageData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['message_id'] = df['message_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['message_length'] = df['message_length'].astype(str).astype(float)
		df['message_direction'] = df['message_direction'].astype(str)
		df['message_type'] = df['message_type'].astype(str)
		df['message_time_stamp'] = pd.to_datetime(df['message_time_stamp'])
		df['message_date_created'] = pd.to_datetime(df['message_date_created'])
		df = self.filter_last_n_months(df, 3, "message_time_stamp")
		if df.empty:
			df = df.append(
							{'message_id': 1,
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'message_length': 0,
							 'message_type': 'missing',
							 'message_direction': 'missing',
							 'message_time_stamp': datetime.datetime.now()
							}, ignore_index=True)
		return df

	def fetch_music_data(self):
		user_data = MusicData.query.filter(
									MusicData.borrower_id == self.borrower_id,
									MusicData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['music_id'] = df['music_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['music_size'] = df['music_size'].astype(str).astype(float)
		df['music_file_type'] = df['music_file_type'].astype(str)
		df['music_date_added'] = pd.to_datetime(df['music_date_added'])
		df['music_date_created'] = pd.to_datetime(df['music_date_created'])
		df = self.filter_last_n_months(df, 3, "music_date_added")
		if df.empty:
			df = df.append(
							{'music_id': 1,
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'music_size': 0,
							 'music_file_type': 'missing',
							 'music_date_added': datetime.datetime.now()
							}, ignore_index=True)
		return df

	def fetch_video_data(self):
		user_data = VideoData.query.filter(
									VideoData.borrower_id == self.borrower_id,
									VideoData.corporate_id == self.corporate_id
											)
		df = pd.read_sql(user_data.statement, user_data.session.bind)
		db.session.commit()
		df['video_id'] = df['video_id'].astype(str).astype(int)
		df['borrower_id'] = df['borrower_id'].astype(str).astype(int)
		df['corporate_id'] = df['corporate_id'].astype(str).astype(int)
		df['video_size'] = df['video_size'].astype(str).astype(float)
		df['video_file_type'] = df['video_file_type'].astype(str)
		df['video_date_added'] = pd.to_datetime(df['video_date_added'])
		df['video_date_created'] = pd.to_datetime(df['video_date_created'])
		df = self.filter_last_n_months(df, 3, "video_date_added")
		if df.empty:
			df = df.append(
							{'video_id': 1,
							 'borrower_id': self.borrower_id,
							 'corporate_id':self.corporate_id,
							 'video_size': 0,
							 'video_file_type': 'missing',
							 'video_date_added': datetime.datetime.now()
							}, ignore_index=True)
		return df
