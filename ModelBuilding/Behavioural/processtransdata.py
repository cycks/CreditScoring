"""
Prepares Transactional data

The tra
"""

import datetime
import numpy as np
import pandas as pd
import re



transactional_types = {
						'borrower_id': 'int',
						'kyc_id': 'int',
						'default_status': 'int',
						'borrower_date_created': 'datetime',
						'borrower_date_of_birth': 'datetime',
						'gender_f': 'int',
						'gender_m': 'int',
						'province_Central': 'int',
						'province_Coast': 'int',
						'province_Eastern': 'int',
						'province_Nairobi': 'int',
						'province_NorthEastern': 'int',
						'province_Nyanza': 'int',
						'province_RiftyValley': 'int',
						'province_Western': 'int',
						'age': 'int',
						'deposit_id': 'int',
						'date_of_deposit': 'datetime',
						'deposit_amount': 'float',
						'deposit_channel_Airtel': 'int',
						'deposit_channel_Bank': 'int',
						'deposit_channel_Mpesa': 'int',
						'deposit_description_Installments': 'int',
						'deposit_description_Savings': 'int',
						'withdrawals_id': 'int',
						'date_of_withdrawals': 'datetime',
						'withdrawals_amount': 'float',
						'withdrawals_channel_Mfanisi': 'int',
						'withdrawals_channel_Mpesa': 'int',
						'withdrawals_description_Installments': 'int',
						'withdrawals_description_Savings': 'int',
						'savings_id': 'int',
						'date_of_savings': 'datetime',
						'savings_amount': 'float',
						'savings_channel_Mfanisi': 'int',
						'savings_channel_Mpesa': 'int',
						'savings_type_current': 'int',
						'savings_type_fixed': 'int',
						'loan_id': 'int',
						'date_of_loan': 'datetime',
						'loan_period': 'int',
						'loan_amount': 'float',
						'loan_interest': 'float',
						'date_of_loan_completion': 'datetime',
						'loan_installment_1': 'int',
						'loan_installment_2': 'int',
						'loan_installment_3': 'int',
						'installment_id': 'int',
						'installments_loan_id': 'int',
						'corporate_id': 'int',
						'date_of_installment': 'datetime',
						'installment_amount': 'float',
						'installment_loan_balance': 'float',
						'installment_type_debt_collection': 'int',
						'installment_type_interest': 'int',
						'installment_type_principal': 'int'
					   }

class WrappedTransactional():

	def impute_missing_columns(self, df, required_columns):
		"""
		Handles missing and unawanted columns.

		Check columns present in the dataframe sort it and
		compare it to a sorted list of required columns.
		If any of the required columns are missing replace them
		with default values.

		Args:
			df(obj): A dataframe
			required_columns (list): A list containing columns that
			must be present in the dataframe:

		Returns:
			obj: A dataframe.

		"""
		columns_present = sorted(list(df.columns))
		if columns_present != required_columns:
			missing_columns = list(set(required_columns) - set(columns_present))
			for item in missing_columns:
				if transactional_types[str(item)] == 'int' and item != 'year':
					df[str(item)] = 0
				if transactional_types[str(item)] == 'float':
					df[str(item)] = 0
				if transactional_types[str(item)] == 'datetime':
					df[str(item)] = datetime.datetime.now()
				if str(item) == 'month':
					df[str(item)] = datetime.datetime.now().month
				if str(item) == 'year':
					df[str(item)] = datetime.datetime.now().year
		return df



	def prepare_borrower_data(self, df):
		"""
		Prepares borrower data.

		Given a dataframe convert date columns to appropriate types
		then convert counties to their respective provinces.

		Args:
			df (obj): A dataframe preferable the borrower df.

		Returns:
			df (obj): A cleaned borrower data.

		"""
		df["borrower_date_of_birth"] = pd.to_datetime(df["borrower_date_of_birth"])
		df["borrower_date_created"] = pd.to_datetime(df["borrower_date_created"])
		df["borrower_county"] = (df["borrower_county"].map({"Kakamega": "Western",
									"Bungoma": "Western", "Busia": "Western",
									"Vihiga": "Western", "Kisii": "Nyanza", 
									"Kisumu": "Nyanza", "Migori": "Nyanza",
									"Homabay": "Nyanza", "Siaya": "Nyanza",
									"Nyamira": "Nyanza", "Bomet": "RiftyValley",
									"Elgeyo-Marakwet": "RiftyValley", 
									"West Pokot": "RiftyValley", "Kericho": "RiftyValley",
									"Nandi": "RiftyValley", "Uasin Gishu": "RiftyValley",
									"Nakuru": "RiftyValley", "Samburu": "RiftyValley",
									"Narok": "RiftyValley", "Baringo": "RiftyValley",
									"Trans Nzoia": "RiftyValley", "Kajiado": "RiftyValley",
									"Laikipia": "RiftyValley", "Turkana": "RiftyValley",
									"Nairobi": "Nairobi",
									"Kiambu": "Central", "Nyeri": "Central",
									"Kirinyaga": "Central", "Nyandarua": "Central",
									"Muranga'a": "Central", "Kwale": "Coast",
									"Taita-Taveta": "Coast", "Mombasa": "Coast",
									"Kilifi": "Coast", "Lamu": "Coast",
									"Tana River": "Coast",
									"Machakos":"Eastern", "Meru": "Eastern",
									"Embu": "Eastern",
									"Tharaka-Nithi": "Eastern", "Kitui": "Eastern",
									"Makueni": "Eastern", "Marsabit": "Eastern",
									"Isiolo": "Eastern",
									"Garissa": "NorthEastern", "Wajir": "NorthEastern",
									"Mandera": "NorthEastern"}))
		return df



	def create_target_df(self, df, borrower_id, target_column):
		"""
		Creates a df with the predictor variable and an id.

		Args:
			df (obj): A dataframe.
			borrower_id (int): Self explanatory
			target_column (str): The response variable.

		Returns:
			dataframe

		"""
		myTarget = df[[str(borrower_id), str(target_column)]]
		return myTarget


	def prepare_kyc_data(self, df, borrower_df):
		"""
		Prepares the kyc_data

		Given a borrower_df prepare it using the method using the
		prepare_borrower_data defined in this class. Cleaning in 
		this method is self explanatory easily readable.

		Args:
			df (obj): Kyc dataframe
			borrower_df (df): The borrower dataframe.

		Returns:
			df (obj): A prepared dataframe
		"""
		borrower_df = self.prepare_borrower_data(borrower_df) 
		df1 = df.drop(columns=["kyc_id", "corporate_id"])
		df1 = df.merge(borrower_df, how="left")
		df1 = df1.rename(columns={"kyc_default_status": "default_status"})
		try:
			 df1 = df.drop(columns=["default_status",
												'borrower_phone_number'])
		except:
			pass        
		df2 = pd.get_dummies(df1, columns=["borrower_gender"], prefix="gender")
		df2 = pd.get_dummies(
								df2, columns=["borrower_county"],
								prefix="province"
							)
		df2["Today"] =  pd.to_datetime("today")
		df2["age"] = (
						df2["Today"].dt.year - 
						df2["borrower_date_of_birth"].dt.year
					 )
		# df2 = df2[df2.columns.drop(list(df2.filter(regex='missing')))]
		df2 = df2.drop(columns=["Today", "corporate_id", "kyc_id"])
		df2 = df2[df2.columns.drop(list(df2.filter(regex='missing')))]
		del df1
		required_columns = ['kyc_id', 'borrower_id', 
							 'borrower_date_created', 'borrower_date_of_birth',
							 'gender_f', 'gender_m', 'province_Central',
							 'province_Coast', 'province_Eastern', 
							 'province_Nairobi', 'province_NorthEastern',
							 'province_Nyanza', 'province_RiftyValley',
							 'province_Western', 'age']
		required_columns = sorted(required_columns)                   
		kyc_data2 = self.impute_missing_columns(df2, required_columns)
		return kyc_data2


	def summarize_kyc(self, df, borrower_df, borrower_id):
		"""
		Summarizes the kyc df.

		Given a dataframe, prepare it. No idea of the logic
		used here for now. Will need to check later

		Args:
			df (obj): The kyc dataframe
			borrower_df (obj): The borrower df
			borrower_id (int): The borrowers id

		Returns:
			df (obj): A summarized dataframe.
		"""
		df = self.prepare_kyc_data(df, borrower_df)
		df = df.loc[df["borrower_id"] == borrower_id] # filter for borrower_id
		df = df.loc[:, (df != 0).any(axis=0)]
		df = df.drop(columns=["borrower_id"])
		df_tojson = df.to_json(orient="records")[1:-1].replace("},{", "} {")
		del df
		return df_tojson 

	
	def prepare_deposits(self, df):
		"""
		Prepares the deposit data.

		Create dummy variables form the deposit channel column, convert
		the data_of_deposit to datetime, drop the corporate_id and any
		columns containing the 'missing'. Confirm that no required
		columns are missing or any unwanted columns are present.

		Args:
			df (obj): The deposits data frame

		Returns:
			df (obj): The prepared deposits dataframe.
		"""
		deposits = pd.get_dummies(
									df,
									columns=["deposit_channel"],
									prefix="deposit_channel"
								  )
		deposits["date_of_deposit"] = pd.to_datetime(
											deposits["date_of_deposit"]
										)
		deposits = pd.get_dummies(
									deposits,
									columns=["deposit_description"],
									prefix="deposit_description"
								 )
		deposits = deposits.drop(columns=["corporate_id"])
		deposits = deposits[
								deposits.columns.drop(
									list(deposits.filter(regex='missing'))
									)
							]
		required_columns = ['deposit_id', 'borrower_id', 'date_of_deposit',
							'deposit_amount', 'deposit_channel_Airtel',
							'deposit_channel_Bank', 'deposit_channel_Mpesa',
							'deposit_description_Installments',
							'deposit_description_Savings']
		required_columns = sorted(required_columns)                   
		deposits = self.impute_missing_columns(deposits, required_columns)
		return deposits

	def sum_deposit_amounts(self, df):
		"""
		Group by month, year, and id and find sum

		Extract month and year from date of deposit, and add amounts
		to the repective columns by multiplying the amount by the 
		dummy variables. Group by month, year and borrower_id, find
		the sum and rename the final columns.

		Args:
			df (obj): The deposits dataframe.

		Returns:
			df (obj): summarised deposits data.

		"""
		df["month"] = pd.DatetimeIndex(df["date_of_deposit"]).month_name()
		df["year"] = pd.DatetimeIndex(df["date_of_deposit"]).year
		df["deposit_channel_Airtel"] = (
											df["deposit_channel_Airtel"] * 
											df["deposit_amount"]
										)
		df["deposit_channel_Bank"] = (
										df["deposit_channel_Bank"] * 
										df["deposit_amount"]
									  )
		df["deposit_Mpesa"] = df["deposit_Mpesa"] * df["deposit_amount"]
		df["deposit_description_Savings"] = (
										df["deposit_description_Savings"] * 
										df["deposit_amount"]
										)
		df["deposit_description_Installments"] = (
								df["deposit_description_Installments"] * 
								df["deposit_amount"]
												  )
		df = df.drop(columns=["date_of_deposit", "deposit_id"])
		df1_sums = df.groupby(
								["borrower_id", "year", "month"]
							  ).agg(
									  {
										"deposit_channel_Airtel":"sum", 
										"deposit_channel_Bank":"sum",
										"deposit_Mpesa":"sum",
										"deposit_description_Savings":"sum",
										"deposit_description_Installments":"sum"
									  }
									).reset_index()
		df1_sums.rename(
					  columns={
								"deposit_channel_Airtel":"deposit_Airtel_sum",
								"deposit_channel_Bank":"deposit_Bank_sum",
								"deposit_Mpesa": "deposit_Mpesa_sum",
								"deposit_description_Savings": "Savings_sum",
						"deposit_description_Installments": "Installments_sum"
						  },
						inplace=True)
		return df1_sums


	def count_deposit_amounts(self, df):
		"""
		Group by year, month, and borrower_id and find counts.

		Extract month and year from date of deposit, count the 
		occurrence of each dummy column by summing them up. 

		Args:
			df (obj): The deposits dataframe.

		Returns:
			df (obj): counts deposits data.

		"""

		df["month"] = pd.DatetimeIndex(df["date_of_deposit"]).month_name()
		df["year"] = pd.DatetimeIndex(df["date_of_deposit"]).year
		df = df.drop(columns=["date_of_deposit", "deposit_id", "deposit_amount"])
		df1_counts = df.groupby(
								["borrower_id", "year", "month"]
								).agg(
									  {
										"deposit_channel_Airtel":"sum", 
										"deposit_channel_Bank":"sum",
										"deposit_Mpesa":"sum",
										"deposit_description_Savings":"sum",
										"deposit_description_Installments":"sum"
									  }
								).reset_index()
		df1_counts.rename(
					 columns={
								"deposit_channel_Airtel":"depositAirtel_count",
								"deposit_channel_Bank":"deposit_Bank_count",
								"deposit_Mpesa": "deposit_Mpesa_count",
								"deposit_description_Savings": "Savings_count",
					"deposit_description_Installments": "Installments_count"
							  },
						  inplace=True)
		return df1_counts


	def summarize_deposits(self, df, borrower_id):
		"""
		Summarize the counts and sums in deposit data.

		Given a dataframe find the sums and counts from the
		data frame, join the resulting dataframes and convert the
		final dataframe to json.

		Args:
			df (obj): The deposits dataframe.
			borrower_id (int): The borrower_id for the loan seeker

		Returns:
			df (json): A json object from the final dataframe.
		"""
		df = df.loc[df["borrower_id"] == borrower_id]
		df1 = self.prepare_deposits(df)
		df_sums = self.sum_deposit_amounts(df1)
		df2 = self.prepare_deposits(df)
		df_counts = self.count_deposit_amounts(df2)
		df = pd.merge(df_sums, df_counts, how="left", on=["borrower_id", "year", "month"])
		df_tojson = df.to_json(orient="records")[1:-1].replace("},{", "} {")
		return df_tojson
#################################################################################################

	def prepare_withdrawals(self, df):
		"""
		Prepares the withdrawals data.

		Create dummy variables form the withdrawal channel column, convert
		the date_of_withdrawal to datetime, drop the corporate_id and any
		columns containing the string 'missing'. Confirm that no required
		columns are missing or any unwanted columns are present.

		Args:
			df (obj): The deposits data frame

		Returns:
			df (obj): The prepared deposits dataframe.
		"""
		withdrawal = pd.get_dummies(
										df,
										columns=["withdrawals_channel"],
										prefix="withdrawals_channel"
									)
		withdrawal["date_of_withdrawals"] = (pd.to_datetime(
												withdrawal[
													"date_of_withdrawals"
												])
											)
		withdrawal = pd.get_dummies(
										withdrawal,
										columns=["withdrawals_description"],
										prefix="withdrawals_description"
									)
		withdrawal = withdrawal.drop(columns=["corporate_id"])
		withdrawal = (  withdrawal
							[
								withdrawal.columns.drop(
								list(withdrawal.filter(regex='missing'))
								)
							]
					)
		required_columns = [
							  'withdrawals_id', 'borrower_id',
							  'date_of_withdrawals', 'withdrawals_amount',
							  'withdrawals_channel_Mfanisi',
							  'withdrawals_channel_Mpesa',
							  'withdrawals_description_Installments',
							  'withdrawals_description_Savings'
							]
		required_columns = sorted(required_columns)
		withdrawal = self.impute_missing_columns(withdrawal, required_columns)
		return withdrawal  


	def sum_withdrawal_amounts(self, df):
		"""
		Group by month, year, and id and find sum

		Extract month and year from date of withdrawal, add amounts
		to the repective columns by multiplying the amount by the 
		dummy variables. Group by month, year and borrower_id, find
		the sum and rename the final columns.

		Args:
			df (obj): The deposits dataframe.

		Returns:
			df (obj): summarised deposits data.

		"""
		df["month"] = pd.DatetimeIndex(df["date_of_withdrawal"]).month_name()
		df["year"] = pd.DatetimeIndex(df["date_of_withdrawal"]).year
		df["withdrawal_Mfanisi"] = df["withdrawal_Mfanisi"] * df["withdrawal_amount"]
		df["withdrawal_Mpesa"] = df["withdrawal_Mpesa"] * df["withdrawal_amount"]
		df["withdrawal_Installments"] = df["withdrawal_Installments"] * df["withdrawal_amount"]
		df["withdrawal_Savings"] = df["withdrawal_Savings"] * df["withdrawal_amount"]
		df = df.drop(columns=["date_of_withdrawal", "withdrawal_id"])
		df1_sums = df.groupby(
								["borrower_id", "year", "month"]
							  ).agg(
									  {
										"withdrawal_Mfanisi":"sum", 
										"withdrawal_Mpesa":"sum",
										"withdrawal_Installments":"sum",
										"withdrawal_Savings":"sum"
									  }
									).reset_index()
		df1_sums.rename(
					 columns={
								"withdrawal_Mfanisi":"withdrawal_Mfanisi_sum",
								"withdrawal_Mpesa":"withdrawal_Mpesa_sum",
								"withdrawal_Installments": "withdrawal_Installments_sum",
								"withdrawal_Savings": "withdrawal_Savings_sum"
							  },
					  inplace=True)
		return df1_sums


	def count_withdrawal_amounts(self, df):
		"""
		Group by year, month, and borrower_id and find counts.

		Extract month and year from date of withdrawal, count the 
		occurrence of each dummy column by summing them up. 

		Args:
			df (obj): The deposits dataframe.

		Returns:
			df (obj): counts deposits data.

		"""
		df["month"] = pd.DatetimeIndex(df["date_of_withdrawal"]).month_name()
		df["year"] = pd.DatetimeIndex(df["date_of_withdrawal"]).year
		df = df.drop(columns=["date_of_withdrawal", "withdrawal_id", "withdrawal_amount"])
		df1_counts = df.groupby(
								  ["borrower_id", "year", "month"]
								).agg(
										{
										  "withdrawal_Mfanisi":"sum", 
										  "withdrawal_Mpesa":"sum",
										  "withdrawal_Installments":"sum",
										  "withdrawal_Savings":"sum"
										}
									  ).reset_index()
		df1_counts.rename(
							columns={
									  "withdrawal_Mfanisi":"withdrawal_Mfanisi_count",
									  "withdrawal_Mpesa":"withdrawal_Mpesa_count",
									  "withdrawal_Installments": "withdrawal_Installments_count",
									  "withdrawal_Savings": "withdrawal_Savings_count"
									},
							inplace=True
						  )
		return df1_counts


	def summarize_withdrawals(self, df, borrower_id):
		"""
		Summarize the counts and sums in withdrawals data.

		Given a dataframe find the sums and counts from the
		data frame, join the resulting dataframes and convert the
		final dataframe to json.

		Args:
			df (obj): The withdrawals dataframe.
			borrower_id (int): The borrower_id for the loan seeker

		Returns:
			df (json): A json object from the final dataframe.
		"""
		df = df.loc[df["borrower_id"] == borrower_id]
		df1 = self.prepare_withdrawals(df)
		df_sums = self.sum_withdrawal_amounts(df1)
		df2 = self.prepare_withdrawals(df)
		df_counts = self.count_withdrawal_amounts(df2)
		df = pd.merge(
						df_sums, df_counts, how="left",
						on=["borrower_id", "year", "month"]
					  )
		df_tojson = df.to_json(orient="records")[1:-1].replace("},{", "} {")
		return df_tojson

##################################################################################################
	def prepare_savings(self, df):
		"""
		Prepares the savings data.

		Create dummy variables form the withdrawal channel column, convert
		the date_of_withdrawal to datetime, drop the corporate_id and any
		columns containing the string 'missing'. Confirm that no required
		columns are missing or any unwanted columns are present.

		Args:
			df (obj): The deposits data frame

		Returns:
			df (obj): The prepared deposits dataframe.
		"""
		savings = pd.get_dummies(
									df,
									columns=["savings_channel"],
									prefix="savings_channel"
								)
		savings["date_of_savings"] = pd.to_datetime(savings["date_of_savings"])
		savings = pd.get_dummies(
									savings,
									columns=["savings_type"],
									prefix="savings_type"
								)
		savings = savings.drop(columns=["corporate_id"])
		savings = savings[
							savings.columns.drop(
								list(savings.filter(regex='missing'))
								)
						 ]
		required_columns = ['savings_id', 'borrower_id', 'date_of_savings',
							'savings_amount', 'savings_channel_Mfanisi',
							'savings_channel_Mpesa',
							'savings_type_current', 'savings_type_fixed'
							]
		required_columns = sorted(required_columns)
		savings = self.impute_missing_columns(savings, required_columns)
		return savings  


	def sum_savings_amounts(self, df):
		"""
		Group by month, year, and id and find sum

		Extract month and year from date of savings, add amounts
		to the repective columns by multiplying the amount by the 
		dummy variables. Group by month, year and borrower_id, find
		the sum and rename the final columns.

		Args:
			df (obj): The savings dataframe.

		Returns:
			df (obj): summarised savings data.

		"""
		df["month"] = pd.DatetimeIndex(df["date_of_savings"]).month_name()
		df["year"] = pd.DatetimeIndex(df["date_of_savings"]).year
		df["savings_channel_Mfanisi"] = df["savings_channel_Mfanisi"] * df["savings_amount"]
		df["savings_channel_Mpesa"] = df["savings_channel_Mpesa"] * df["savings_amount"]
		df["savings_current"] = df["savings_current"] * df["savings_amount"]
		df["savings_fixed"] = df["savings_fixed"] * df["savings_amount"]
		df = df.drop(columns=["date_of_savings", "savings_id"])
		df1_sums = df.groupby(
								["borrower_id", "year", "month"]
							  ).agg(
									  {
										"savings_channel_Mfanisi":"sum", 
										"savings_channel_Mpesa":"sum",
										"savings_current":"sum",
										"savings_fixed":"sum"
									  }
									).reset_index()
		df1_sums.rename(
						columns=
							  {
								"savings_channel_Mfanisi":"savings_Mfanisi_sum",
								"savings_channel_Mpesa":"savings_Mpesa_sum",
								"savings_current": "savings_current_sum",
								"savings_fixed": "savings_fixed_sum"
							  },
						inplace=True)
		return df1_sums


	def count_savings_amounts(self, df):
		"""
		Group by year, month, and borrower_id and find counts.

		Extract month and year from date of savings, count the 
		occurrence of each dummy column by summing them up. 

		Args:
			df (obj): The savings dataframe.

		Returns:
			df (obj): counts svings data.

		"""
		df["month"] = pd.DatetimeIndex(df["date_of_savings"]).month_name()
		df["year"] = pd.DatetimeIndex(df["date_of_savings"]).year
		df = df.drop(columns=["date_of_savings", "savings_id", "savings_amount"])
		df1_counts = df.groupby(
								  ["borrower_id", "year", "month"]
							   ).agg(
									  {
										"savings_channel_Mfanisi":"sum", 
										"savings_channel_Mpesa":"sum",
										"savings_current":"sum",
										"savings_fixed":"sum"
									  }
									).reset_index()
		df1_counts.rename(
						  columns=
								  {
							"savings_channel_Mfanisi":"savings_Mfanisi_count",
							"savings_channel_Mpesa":"savings_Mpesa_count",
							"savings_current": "savings_current_count",
							"savings_fixed": "savings_fixed_count"
								  }, inplace=True
						 )
		return df1_counts


	def summarize_savings(self, df, borrower_id):
		"""
		Summarize the counts and sums in svings data.

		Given a dataframe find the sums and counts from the
		data frame, join the resulting dataframes and convert the
		final dataframe to json.

		Args:
			df (obj): The savings dataframe.
			borrower_id (int): The borrower_id for the loan seeker

		Returns:
			df (json): A json object from the final dataframe.
		"""
		df = df.loc[df["borrower_id"] == borrower_id]
		df1 = self.prepare_savings(df)
		df_sums = self.sum_savings_amounts(df1)
		df2 = self.prepare_savings(df)
		df_counts = self.count_savings_amounts(df2)
		df = pd.merge(
						df_sums, df_counts, how="left",
						on=["borrower_id", "year", "month"]
					  )
		df_tojson = df.to_json(orient="records")[1:-1].replace("},{", "} {")
		return df_tojson


	def prepare_loan_4_classification(self, df):
		"""
		Prepares the loan data for classification.

		Create dummy variables from the loan_period column and the 
		loan_installment_frequency columns, convert the date_of_loan 
		and the date_of_loan_completion to datetime, drop the 
		corporate_id and any columns containing the string 
		'missing'. Confirm that no required columns are missing or 
		any unwanted columns are present.

		Args:
			df (obj): The loan data frame

		Returns:
			df (obj): The prepared loan dataframe.
		"""
		loan_data = pd.get_dummies(
									df,
									columns=["loan_period"],
									prefix="period"
								  )
		df["date_of_loan"] = pd.to_datetime(df["date_of_loan"])
		df["date_of_loan_completion"] =  (
											pd.to_datetime(
											df["date_of_loan_completion"]
													)    
										  )
		loan_data = pd.get_dummies(
									df,
									columns=["loan_installment_frequency"],
									prefix="loan_installment"
								   )
		loan_data = loan_data.drop(columns=["corporate_id"])
		loan_data = loan_data[
								loan_data.columns.drop(
									list(loan_data.filter(regex='missing'))
								)
							 ]
		required_columns = [
								'loan_id', 'borrower_id', 'date_of_loan',
								'loan_period', 'loan_amount', 
								'date_of_loan_completion', 'loan_installment_1',
								'loan_installment_2', 'loan_installment_3'
						   ]
		required_columns = sorted(required_columns)
		loan_data = self.impute_missing_columns(loan_data, required_columns)
		return loan_data


	def prepare_loan_4_regression(self, df):
		"""
		Prepares the loan data for regression.

		Create dummy variables from the loan_period column and the 
		loan_installment_frequency columns, convert the date_of_loan 
		and the date_of_loan_completion to datetime, drop the 
		corporate_id, is_defaulted_loan, loan_id and any columns 
		containing the string  'missing'. Confirm that no 
		required columns are missing or  any unwanted columns are 
		present.

		Args:
			df (obj): The loan data frame

		Returns:
			df (obj): The prepared loan dataframe.
		"""
		df =  pd.DataFrame([df])
		df = pd.get_dummies(
							df,
							columns=["loan_period"],
							prefix="period"
						  )
		df["date_of_loan"] = pd.to_datetime(df["date_of_loan"])
		df["date_of_loan_completion"] =  (
											pd.to_datetime(
											df["date_of_loan_completion"]
													)   
										  )
		loan_data = pd.get_dummies(
									df,
									columns=["loan_installment_frequency"],
									prefix="loan_installment"
								   )
		loan_data = loan_data[
								loan_data.columns.drop(
									list(loan_data.filter(regex='missing'))
								)
							 ]
		try:
			loan_data = loan_data.drop(
											columns=[
													"corporate_id",
													"is_defaulted_loan",
													"loan_id"
												]
										)
		except KeyError:
			pass
		required_columns = [
								'borrower_id', 'date_of_loan',
								'loan_period', 'loan_amount', 
								'date_of_loan_completion', 'loan_installment_1',
								'loan_installment_2', 'loan_installment_3'
						   ]
		required_columns = sorted(required_columns)
		loan_data = self.impute_missing_columns(loan_data, required_columns)
		return loan_data


	def prepare_installments(self, df):
		"""
		Prepares the installments data.

		Create dummy variables form the installments channel 
		and types column,  	convert the date_of_installment to 
		datetime, drop the 	corporate_id and any columns containing
		the string 'missing'. Confirm that no required columns are 
		missing or any unwanted columns are present.

		Args:
			df (obj): The deposits data frame

		Returns:
			df (obj): The prepared deposits dataframe.
		"""
		df["date_of_installment"] = pd.to_datetime(df["date_of_installment"])
		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		df = df.drop(columns=["corporate_id", "borrower_id"])
		installment_data = pd.get_dummies(
											df,
											columns=["installment_type"],
											prefix="installment_type"
										  )
		required_columns = [
								'installment_id', 'installments_loan_id',
								'corporate_id','date_of_installment',
								'installment_amount', 'borrower_id',
								'installment_loan_balance',
								'installment_type_debt_collection',
								'installment_type_interest',
								'installment_type_principal'
							]
		required_columns = sorted(required_columns)
		installment_data = self.impute_missing_columns(installment_data,
														required_columns)
		return installment_data


# kyc_data = pd.read_csv("Transanctional/kyc_data.csv")
# borrowers_data = pd.read_csv("Transanctional/borrower.csv")
# deposits_data = pd.read_csv("Transanctional/deposits_data.csv")
# withdrawals_data = pd.read_csv("Transanctional/withdrawal_data.csv")
# savings_data = pd.read_csv("Transanctional/savings_data.csv")



# kyc_instance = WrappedTransactional()
# cleaned_kyc = kyc_instance.prepare_kyc_data(kyc_data, borrowers_data)
# print(cleaned_kyc.columns)


# summarize_kyc = kyc_instance.summarize_kyc(kyc_data, borrowers_data, 113)
# print(summarize_kyc)

# deposits_instance = WrappedTransactional()
# # print(deposits_instance)
# cleaned_deposits = deposits_instance.prepare_deposits(deposits_data)
# print(cleaned_deposits.head(10))
# # count_deposits = deposits_instance.count_deposit_amounts(deposits_data)
# # print(count_deposits.columns)

# summarized_deposits = deposits_instance.summarize_deposits(deposits_data, 113)
# print(summarized_deposits)


# withdrawals_instance = WrappedTransactional()
# cleaned_withdrawals = withdrawals_instance.prepare_withdrawals(withdrawals_data)
# # print(cleaned_withdrawals.head(10))
# count_withdrawals = withdrawals_instance.count_withdrawal_amounts(cleaned_withdrawals)
# print(count_withdrawals.head(5))

# summarized_withdrawals = withdrawals_instance.summarize_withdrawals(withdrawals_data, 113)
# print(summarized_withdrawals)


# savings_instance = WrappedTransactional()
# cleaned_savings = savings_instance.prepare_savings(savings_data)
# # print(cleaned_savings.head(10))
# # print(cleaned_savings.columns)
# count_savings = savings_instance.count_savings_amounts(cleaned_savings)
# # print(count_savings.head(5))

# summarized_savings = savings_instance.summarize_savings(savings_data, 113)
# print(summarized_savings)