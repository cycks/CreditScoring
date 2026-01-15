"""
Prepares data for limit prediction
"""

import pickle
import pandas as pd
import numpy as np

from Models.our_data import  FetchedData


from ModelBuilding.Behavioural.processtransdata import WrappedTransactional
from ModelBuilding.Behavioural.processphonedata import WrappedPhone
from ModelBuilding.Behavioural.featureengineering import (
									create_limit_kyc_entity,
									create_deposits_entity,
									create_withdrawals_entity,
									create_limit_loans_entity,
									create_installments_entity,
									create_savings_entity,
									create_mpesa_entity,
									create_images_entity,
									create_music_entity,
									create_messages_entity,
									create_videos_entity,
									add_limit_relations_to_entityset,
									do_limit_feature_engineering
								)
from ModelBuilding.Behavioural.required_limit import required_columns


def check_required_columns(df, required_columns):
	"""
	Validates columns required for prediction.

	Given a dataframe and the required columns that the dataframe
	must have, extract columns from the dataframe, drop any columns
	that are in the dataframe, but are not required for prediction.
	Find columns that should be in the dataframe but are missing
	and add the missing columns by replacing them with zero.

	Args:
		df(obj): dataframe
		required_columns(list): A list of columns that must be
		present in the dataframe

	Returns:
		df(obj): A dataframe with all the required columns.
	"""

	# Get a list of columns present in the data frame
	current_columns = list(df.columns)
	# Get columns common in the required_cols and the current cols
	# i.e drop any columns that are in current_columns but are not required
	current_required = list(set(required_columns).intersection(current_columns))
	# Find items that should be in current_columns but are missing
	missing_columns = list(set(required_columns) - set(current_columns))
	# Select the ones you want df1 = df[['a','d']]
	final_df = df[current_required]
	# Remember an item will only be missing if it is categorical.
	for item in missing_columns:
		final_df[str(item)] = 0
	return final_df



def create_limit_df(borrower_id, corporate_id, loan_data):
	"""
	Fetch the Required datasets from the database.
	
	Note:
		The loan dataset is created using details provided
		from the frontend.
	
	Fetch the required data sets from the database, prepare the
	datasets, create an entity set from the data sets, add
	relationships to the entity set create additional features
	from the dataframe using feature tools, replace missing and
	required columns from the dataset and return the final
	dataframe.

	Args:
		borrower_id (int): The id for the borrower
		corporate_id (int): The corporate id for the organization
		seeking the dataset.
		loan_date (obj): A loan dataset sent from the frontend
	Returns:
		obj: A dataframe ready for prediction.
	"""


	fetch_data_instance = FetchedData(borrower_id, corporate_id)
		
	kyc_data = fetch_data_instance.fetch_kyc_data()
	borrower_data = fetch_data_instance.fetch_borrower_data()
	deposits = fetch_data_instance.fetch_deposits_data()
	savings = fetch_data_instance.fetch_savings_data()
	withdrawals = fetch_data_instance.fetch_withdrawal_data()
	
	
	mpesa = fetch_data_instance.fetch_mpesa_data()
	images = fetch_data_instance.fetch_image_data()
	messages = fetch_data_instance.fetch_message_data()
	music = fetch_data_instance.fetch_music_data()
	videos = fetch_data_instance.fetch_video_data()

	# prepare transactional data
	trans_instance = WrappedTransactional()
	kyc_data = trans_instance.prepare_kyc_data(kyc_data, borrower_data)
	deposits = trans_instance.prepare_deposits(deposits)
	withdrawals = trans_instance.prepare_withdrawals(withdrawals)
	savings = trans_instance.prepare_savings(savings)
	loans = trans_instance.prepare_loan_4_regression(loan_data)


	# prepare phone data
	phonedata_instance = WrappedPhone()
	mpesa = phonedata_instance.prepare_mpesa(mpesa)
	images = phonedata_instance.prepare_images(images)
	messages = phonedata_instance.prepare_messages(messages)
	music = phonedata_instance.prepare_music(music)
	videos = phonedata_instance.prepare_videos(videos)



	es = create_limit_loans_entity(loans)
	# es = create_limit_kyc_entity(es, kyc_data)
	es = create_deposits_entity(es, deposits)
	es = create_withdrawals_entity(es, withdrawals)
	es = create_savings_entity(es, savings)
	
	es = create_mpesa_entity(es, mpesa)
	es = create_images_entity(es, images)
	es = create_music_entity(es, music)
	es = create_messages_entity(es, messages)
	es = create_videos_entity(es, videos)

	es = add_limit_relations_to_entityset(es)


	final_df = do_limit_feature_engineering(es)	
	final_df = check_required_columns(final_df, required_columns)
	return final_df



def predict_limit(df):
	"""
	Predicts the right loan limit

	Open the pickled file from the home directory, load the model
	from the file and close the file. Make the prediction, and 
	return the loan amount that should be given to a borrower.

	Args:
		df(dataframe): A dataframe prepared for prediction

	Returns:
		probs(dict): A dictionary with the probability of deffault,
		payment, and the default status.

	"""

	# Import the model that was dumped into a file called default_prediction
	infile = open("saved_limit_model.pkl",'rb')
	# infile2 = open("saved_default_model.pkl",'rb')
	# load the model from the file
	saved_limit_model = pickle.load(infile)
	# close the file
	infile.close()


	
	y_pred = saved_limit_model.predict(df).tolist()
	
	return y_pred
