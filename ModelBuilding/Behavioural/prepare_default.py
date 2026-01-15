"""
Prepares data for default prediction.

"""


import pickle
import pandas as pd
import numpy as np
import sklearn


from Models.our_data import FetchedData


from ModelBuilding.Behavioural.processtransdata import WrappedTransactional
from ModelBuilding.Behavioural.processphonedata import WrappedPhone
from ModelBuilding.Behavioural.featureengineering import (
									create_default_kyc_entity,
									create_deposits_entity,
									create_withdrawals_entity,
									create_default_loans_entity,
									create_installments_entity,
									create_savings_entity,
									create_mpesa_entity,
									create_images_entity,
									create_music_entity,
									create_messages_entity,
									create_videos_entity,
									add_default_relations_to_entityset,
									do_default_feature_engineering
								)
from ModelBuilding.Behavioural.required_default import required_columns



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
	for item in missing_columns:
		final_df[str(item)] = 0
	return final_df



def create_default_df(borrower_id, corporate_id):
	"""
	Fetch the Required datasets from the database.
	
	Fetch the required data sets from the database, prepare the
	datasets, create an entity set from the data sets, add
	relationships to the entity set create additional features
	from the dataframe using feature tools, replace missing and
	required columns from the dataset and return the final
	dataframe.

	Args:
		borrower_id(int): The id for the borrower
		corporate_id (int): The corporate id for the organization
		seeking the dataset.
	Returns:
		obj: A dataframe ready for prediction.

	"""
	fetch_data_instance = FetchedData(borrower_id, corporate_id)
	kyc_data = fetch_data_instance.fetch_kyc_data()
	borrower_data = fetch_data_instance.fetch_borrower_data()
	deposits = fetch_data_instance.fetch_deposits_data()
	savings = fetch_data_instance.fetch_savings_data()
	withdrawals = fetch_data_instance.fetch_withdrawal_data()
	loans = fetch_data_instance.fetch_loans_data()
	installments = fetch_data_instance.fetch_installments_data()
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
	loans = trans_instance.prepare_loan_4_classification(loans)
	installments = trans_instance.prepare_installments(installments)

	# prepare phone data

	phonedata_instance = WrappedPhone()
	mpesa = phonedata_instance.prepare_mpesa(mpesa)
	images = phonedata_instance.prepare_images(images)
	messages = phonedata_instance.prepare_messages(messages)
	music = phonedata_instance.prepare_music(music)
	videos = phonedata_instance.prepare_videos(videos)

	es = create_default_kyc_entity(kyc_data)
	es = create_deposits_entity(es, deposits)
	es = create_withdrawals_entity(es, withdrawals)
	es = create_savings_entity(es, savings)
	es = create_default_loans_entity(es, loans)
	es = create_installments_entity(es, installments)
	es = create_mpesa_entity(es, mpesa)
	
	es = create_images_entity(es, images)
	es = create_music_entity(es, music)
	es = create_messages_entity(es, messages)
	es = create_videos_entity(es, videos)

	es = add_default_relations_to_entityset(es)

	final_df = do_default_feature_engineering(es)	
	final_df = check_required_columns(final_df, required_columns)
	return final_df



def predict_default(df):
	"""
	Predicts defaulters

	open the pickled file from the home directory, load the model
	from the file and close the file. Make the prediction,
	extract the default status and the probability of default and
	the probability of payment from the prediction and return a 
	dictionary.

	Args:
		df(dataframe): A dataframe prepared for prediction

	Returns:
		probs(dict): A dictionary with the probability of deffault,
		payment, and the default status.

	"""
	# Import the model that was dumped into a file called default_prediction
	infile = open("saved_default_model.pkl",'rb')
	# infile2 = open("saved_default_model.pkl",'rb')
	# load the model from the file
	saved_default_model = pickle.load(infile)
	# close the file
	infile.close()

	# make a prediction
	default_model = saved_default_model['behavioural_default']
	
	y_pred = default_model.predict(df).tolist()
	predicted_probabilities = default_model.predict_proba(df).tolist()

	final_result = {"default_status": y_pred,
					"probability_of_default": predicted_probabilities}
	probability_of_payment = final_result["probability_of_default"][0][0]
	probability_of_default = final_result["probability_of_default"][0][1]
	default_status =  final_result["default_status"][0]
	probabilities = {
						"probability_of_payment": probability_of_payment,
					 	"probability_of_default": probability_of_default,
					 	"predicted_default_status": default_status
					 }
	return probabilities


def grade_probabilities(pdf, pdo, best_score):
	"""If a scorecard were being scaled where the user wanted 
	odds of 10,000:1 at 800 points and wanted the odds to 
	double every 20 points (i.e., pdo = 20), the factor and 
	offset would be:
	Factor = 20/Ln(2) = 28.85
	Offset = 800- 28.85 * Ln (10,000) = 534.29.
	In our case we want one default 0out of 200.
	To find the odds go back to the test data set,
	find the number of people who defaulted within a given 
	probability range and the number of people who paid
	their loans within the same range.  use this to find the odds.

	Args:
		pdf(float): The predicted probability from the model
		pdo(int): Points to double the odss
		best_score: What our best score should be.
	
	"""

	odds = (pdf-0.25)/1-(pdf-0.25)
	numerator = pdf-0.25
	denominator = 1 - numerator
	odds = numerator/denominator
	factor = pdo/ np.log(2)
	offset = best_score - factor*np.log(odds)
	score  = offset + factor * np.log(odds)
	return score