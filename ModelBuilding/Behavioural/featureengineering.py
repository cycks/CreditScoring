"""
This module is used for feature engineering.

During feature engineering separate limit from default engineering.
For default engineering: The kyc is the first entity set
For limit engineering: The loan is the first entity set
"""

import numpy as np
import pandas as pd

import featuretools as ft
import featuretools.variable_types as vtypes

from collections import defaultdict



	
def create_default_kyc_entity(df):
	"""
	Create an entity set for kyc

	Creates a kyc entitty set used in predicting the default.
	Initalize an empty called borrowers, decalare all variable
	types using featuretools then add the resultting entity set
	to the borrowers entity set declared earlier.

	Args:
		df: The Kyc data set.
	Returns:
		obj: An entity set(featuretools object)
	"""
	es = ft.EntitySet(id = 'borrowers')
	# decalare variable types
	borrower_types = {
						'borrower_id': vtypes.Index,
						'kyc_id': vtypes.Id,
						'borrower_date_created': vtypes.TimeIndex,
						'borrower_date_of_birth': vtypes.DateOfBirth,
						'age': vtypes.Numeric,
						'province_Central': vtypes.Boolean, 
						'province_Coast': vtypes.Boolean,
						'province_Eastern': vtypes.Categorical,
						'province_Nairobi': vtypes.Boolean,
						'province_NorthEastern': vtypes.Boolean,
						'province_Nyanza': vtypes.Boolean,
						'province_RiftyValley': vtypes.Boolean,
						'province_Western': vtypes.Boolean,
						'gender_f': vtypes.Boolean,
						'gender_m': vtypes.Boolean
				}
	# add the information to the entity set es
	es = es.entity_from_dataframe(entity_id = 'kyc_data',
								  dataframe = df,
								  index = 'borrower_id',
								  variable_types = borrower_types)
	return es


def create_limit_kyc_entity(es, df):
	"""
	Creates a kyc entity set for limit prediction.

	Note:
		Unlike the create_default_kyc_entity function, this
		one does not initalize an empty entity set because that
		is done in the loan entity set.
	Given an entity set and a dataframe create borrower types and
	add the data from the df to the entity set provided. 
	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a kyc data set.
	Returns:
		es(obj): An entity set
	"""
	
	borrower_types = {
						'borrower_id': vtypes.Index,
						'kyc_id': vtypes.Id,
						'borrower_date_created': vtypes.TimeIndex,
						'borrower_date_of_birth': vtypes.DateOfBirth,
						'age': vtypes.Numeric,
						'province_Central': vtypes.Boolean, 
						'province_Coast': vtypes.Boolean,
						'province_Eastern': vtypes.Categorical,
						'province_Nairobi': vtypes.Boolean,
						'province_NorthEastern': vtypes.Boolean,
						'province_Nyanza': vtypes.Boolean,
						'province_RiftyValley': vtypes.Boolean,
						'province_Western': vtypes.Boolean,
						'gender_f': vtypes.Boolean,
						'gender_m': vtypes.Boolean
				}
	# add the information ot the entity set es
	es = es.entity_from_dataframe(entity_id = 'kyc',
								  dataframe = df,
								  index = 'kyc_id',
								  variable_types = borrower_types)
	return es


def create_deposits_entity(es, df):
	"""
	Creates a deposits entity set.

	Given an entity set and a dataframe create deposit types and
	add the data from the df to the entity set provided. 
	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a deposits data set.
	Returns:
		es(obj): An entity set
	"""
	deposit_types = {
						'deposit_id': vtypes.Index,
						'borrower_id': vtypes.Id,
						'date_of_deposit': vtypes.TimeIndex, 
						'deposit_amount': vtypes.Numeric,
						'deposit_channel_Airtel': vtypes.Boolean,
						'deposit_channel_Bank': vtypes.Boolean,
						'deposit_channel_Mpesa': vtypes.Boolean, 
						'deposit_description_Installments': vtypes.Boolean,
						'deposit_description_Savings': vtypes.Boolean
					 }
	es = es.entity_from_dataframe(
									entity_id = 'deposits',
									dataframe = df,
									index = 'deposit_id',
									variable_types = deposit_types
								  )
	return es

def create_withdrawals_entity(es, df):
	"""
	Creates a withdrawals entity set.

	Given an entity set and a dataframe create withdrawals types and
	add the data from the df to the entity set provided. 
	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a withdrawals data set.
	Returns:
		es(obj): An entity set
	"""
	withdrawal_types = {
							"withdrawals_id": vtypes.Index,
							"borrower_id": vtypes.Id,
							"withdrawals_amount": vtypes.Numeric,
							"withdrawals_channel_Mfanisi": vtypes.Boolean,
							"date_of_withdrawals": vtypes.TimeIndex,
							"withdrawals_channel_Mpesa": vtypes.Boolean,
							"withdrawals_description_Installments": vtypes.Boolean,
							"withdrawals_description_Savings": vtypes.Boolean
						}
	# add the information to the entity set es
	es = es.entity_from_dataframe(
									entity_id = "withdrawal",
									dataframe = df,
									index = "withdrawals_id",
									variable_types = withdrawal_types
								 )
	return es


def create_savings_entity(es, df):
	"""
	Creates a savings entity set.

	Given an entity set and a dataframe create savings types and
	add the data from the df to the entity set provided. 
	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a savings data set.
	Returns:
		es(obj): An entity set
	"""
	savings_types = {
						'savings_id': vtypes.Index,
						'borrower_id': vtypes.Id, 
						'date_of_savings': vtypes.TimeIndex,
						'savings_amount': vtypes.Numeric,
						'savings_channel_Mfanisi': vtypes.Boolean,
						'savings_channel_Mpesa': vtypes.Boolean,
						'savings_type_current': vtypes.Boolean,
						'savings_type_fixed':vtypes.Boolean
					}
	es = es.entity_from_dataframe(
									entity_id = 'savings',
									dataframe = df,
									index = 'savings_id',
									variable_types = savings_types
								)
	return es


def create_default_loans_entity(es, df):
	"""
	Creates a loans entity set for predicting default.

	Given an entity set and a dataframe create loans types and
	add the data from the df to the entity set provided. 
	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a loan data set.
	Returns:
		es(obj): An entity set
	"""
	loan_types = {
					  'loan_id':  vtypes.Index,
					  'borrower_id':  vtypes.Id,
					  'date_of_loan': vtypes.TimeIndex,
					  'loan_period': vtypes.Categorical,
					  'loan_amount': vtypes.Numeric,
					  'date_of_loan_completion': vtypes.Datetime,
					  'loan_installment_1': vtypes.Boolean,
					  'loan_installment_2': vtypes.Boolean,
					  'loan_installment_3': vtypes.Boolean
				  }
	es = es.entity_from_dataframe(
									entity_id = 'loans',
									dataframe = df,
									index = 'loan_id',
									variable_types = loan_types
								  )
	return es


def create_limit_loans_entity(df):
	"""
	Creates a loans entity set for limit prediction.

	Note:
		An entity set has not been provided here

	Initialize an empty entity set called loans create loans
	types and add the data from the df to the empty entity set
	initiated.

	Args:
		df: a dataframe in this case a loans data set.
	Returns:
		es(obj): An entity set
	"""
	es = ft.EntitySet(id = 'loans')
	loan_types = {
					  'borrower_id':  vtypes.Index,
					  'date_of_loan': vtypes.TimeIndex,
					  'loan_period': vtypes.Categorical,
					  'date_of_loan_completion': vtypes.Datetime,
					  'loan_installment_1': vtypes.Boolean,
					  'loan_installment_2': vtypes.Boolean,
					  'loan_installment_3': vtypes.Boolean
				  }
	es = es.entity_from_dataframe(
									entity_id = 'loans',
									dataframe = df,
									index = 'borrower_id',
									variable_types = loan_types
								  )
	return es

def create_installments_entity(es, df):
	"""
	Creates an installments entity set.

	Given an entity set and a dataframe create an installments types
	and add the data from the df to the entity set provided.

	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a installments data set.
	Returns:
		es(obj): An entity set
	"""
	installment_types = {
							'installment_id': vtypes.Index,
							'installments_loan_id': vtypes.Id,
							'borrower_id': vtypes.Id,
							'date_of_installment': vtypes.TimeIndex,
							'installment_amount': vtypes.Numeric,
							'installment_loan_balance': vtypes.Numeric, 
							'installment_type_debt_collection': vtypes.Boolean, 
							'installment_type_interest': vtypes.Boolean,
							'installment_type_principal': vtypes.Boolean
						}
	es = es.entity_from_dataframe(
									entity_id = 'installments',
									dataframe = df,
									index = 'installment_id',
									variable_types = installment_types
								 )
	return es


def create_mpesa_entity(es, df):
	"""
	Creates an mpesa entity set.

	Given an entity set and a dataframe create mpesa types and
	add the data from the df to the entity set provided.

	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a mpesa data set.
	Returns:
		es(obj): An entity set
	"""
	mpesa_types  = {
					'mpesa_id': vtypes.Index,
					'borrower_id':  vtypes.Id,
					'mpesa_amount': vtypes.Numeric, 
					'mpesa_time_stamp': vtypes.TimeIndex, 
					'mpesa_airtime': vtypes.Boolean,
					'mpesa_banking': vtypes.Boolean, 
					'mpesa_fuliza': vtypes.Boolean,
					'mpesa_gambling': vtypes.Boolean,
					'mpesa_incoming': vtypes.Boolean,
					'mpesa_loans': vtypes.Boolean,
					'mpesa_outgoing_sent_to': vtypes.Boolean,
					'mpesa_utilities': vtypes.Boolean,
					'mpesa_withdrawal': vtypes.Boolean
				}
	# add the information ot the entity set es
	es = es.entity_from_dataframe(
									entity_id = 'mpesa',
									dataframe = df,
									index = 'mpesa_id',
									variable_types = mpesa_types
								  )
	return es


def create_images_entity(es, df):
	"""
	Creates an immages entity set.

	Given an entity set and a dataframe create an images types and
	add the data from the df to the entity set provided. 
	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a images data set.
	Returns:
		es(obj): An entity set
	"""
	image_types = {
					'image_id': vtypes.Index,
					'image_date_added': vtypes.TimeIndex,
					'image_size': vtypes.Numeric,
					'borrower_id': vtypes.Id,
					'image_heic': vtypes.Boolean,
					'image_jpeg': vtypes.Boolean,
					'image_jpg': vtypes.Boolean,
					'image_png': vtypes.Boolean,
					'image_webp': vtypes.Boolean,
					'image_x-ms-bmp': vtypes.Boolean
				  }
	es = es.entity_from_dataframe(
									entity_id = 'images',
									dataframe = df,
									index = 'id',
									variable_types = image_types
								 )
	return es


def create_music_entity(es, df):
	"""
	Creates a music entity set.

	Given an entity set and a dataframe create music types and
	add the data from the df to the entity set provided.

	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a kyc data set.
	Returns:
		es(obj): An entity set
	"""
	music_types = {
					'music_id': vtypes.Index,
					'music_date_added': vtypes.TimeIndex,
					'music_size': vtypes.Numeric,
					'borrower_id': vtypes.Id,
					'music_3gpp': vtypes.Boolean,
					'music_aac': vtypes.Boolean,
					'music_aac-adts': vtypes.Boolean,
					'music_adpcm': vtypes.Boolean,
					'music_amr': vtypes.Boolean,
					'music_amr-wb': vtypes.Boolean,
					'music_application/aac': vtypes.Boolean,
					'music_application/ogg': vtypes.Boolean,
					'music_flac': vtypes.Boolean,
					'music_m4a': vtypes.Boolean,
					'music_mp3': vtypes.Boolean,
					'music_mp4': vtypes.Boolean,
					'music_mpeg': vtypes.Boolean,
					'music_ogg': vtypes.Boolean,
					'music_quicktime': vtypes.Boolean,
					'music_wav': vtypes.Boolean,
					'music_x-matroska': vtypes.Boolean,
					'music_x-ms-wma': vtypes.Boolean,
					'music_x-wav': vtypes.Boolean
			  }
	es = es.entity_from_dataframe(
									entity_id = 'music',
									dataframe = df,
									index = 'id',
									variable_types = music_types
								  )
	return es


def create_messages_entity(es, df):
	"""
	Creates a message entity set.

	Given an entity set and a dataframe create message types and
	add the data from the df to the entity set provided.

	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a message data set.
	Returns:
		es(obj): An entity set
	"""
	message_types = {
						'message_id': vtypes.Index,
						'message_time_stamp': vtypes.TimeIndex,
						'message_length': vtypes.Numeric,
						'borrower_id': vtypes.Id,
						'message_INCOMING': vtypes.Boolean,
						'message_OUTGOING': vtypes.Boolean
					}
	es = es.entity_from_dataframe(
									entity_id = 'messages',
									dataframe = df,
									index = 'id',
									variable_types = message_types
								  )
	return es


def create_videos_entity(es, df):
	"""
	Creates a video entity set.

	Given an entity set and a dataframe create video types and
	add the data from the df to the entity set provided.

	Args:
		obj: es an entity set, which is a feature tools object.
		df: a dataframe in this case a video data set.
	Returns:
		es(obj): An entity set
	"""
	video_types={
					"video_id":vtypes.Index,
					"video_date_added":vtypes.TimeIndex, 
					"video_size":vtypes.Numeric, 
					"borrower_id":vtypes.Id,
					"video_3gpp":vtypes.Boolean, 
					"video_avi":vtypes.Boolean, 
					"video_mp2ts":vtypes.Boolean, 
					"video_mp4":vtypes.Boolean, 
					"video_mpeg":vtypes.Boolean,
					"video_quicktime":vtypes.Boolean, 
					"video_webm":vtypes.Boolean, 
					"video_x-matroska":vtypes.Boolean
				}
	es = es.entity_from_dataframe(
									entity_id = 'videos',
									dataframe = df,
									index = 'id',
									variable_types = video_types
								  )
	return es


def add_default_relations_to_entityset(es):
	"""
	Creates relationships between entity sets(default prediction).

	Give an entity set create relationships between different
	data sets in the entity set and add the relationships to the
	entity sets.

	Note:
		The relatinships used when predicting default is different 
		from the relationships used when predicting loan limits.

	Args:
		es(obj): Feature tools object
	Returns:
		es(obje): Featuretools object.
	"""
	r_kyc_deposits = ft.Relationship(es['kyc_data']['borrower_id'],
									 es['deposits']['borrower_id'])
	r_kyc_savings = ft.Relationship(es['kyc_data']['borrower_id'],
									es['savings']['borrower_id'])
	r_kyc_withdrawal = (ft.Relationship(es['kyc_data']['borrower_id'],
										es['withdrawal']['borrower_id']))
	r_kyc_loans = ft.Relationship(es['kyc_data']['borrower_id'],
								  es['loans']['borrower_id'])
	r_loans_installments = ft.Relationship(es['loans']['loan_id'],
										   es['installments']['installments_loan_id'])
	r_kyc_mpesa = ft.Relationship(es['kyc_data']['borrower_id'],
								  es['mpesa']['borrower_id'])
	r_kyc_images = ft.Relationship(es['kyc_data']['borrower_id'],
								   es['images']['borrower_id'])
	r_kyc_music = ft.Relationship(es['kyc_data']['borrower_id'],
								  es['music']['borrower_id'])
	r_kyc_messages = ft.Relationship(es['kyc_data']['borrower_id'],
									 es['messages']['borrower_id'])
	r_kyc_videos = (ft.Relationship(es['kyc_data']['borrower_id'],
									  es['videos']['borrower_id']))
	es = es.add_relationships(
								[	
									r_kyc_withdrawal, r_kyc_mpesa,
									r_kyc_deposits, r_kyc_loans,
									r_loans_installments, r_kyc_savings,
									r_kyc_images, r_kyc_music,
									r_kyc_messages,r_kyc_videos
								]
							  )
	return es

def add_limit_relations_to_entityset(es):
	"""
	Creates relationships between entity sets (limit prediction).

	Give an entity set create relationships between different
	data sets in the entity set and add the relationships to the
	entity sets.

	Note:
		The relationships used when predicting default is different 
		from the relationships used when predicting loan limits.

	Args:
		es(obj): Feature tools object
	Returns:
		es(obje): Featuretools object.
	"""
	r_loan_deposits = ft.Relationship(es['loans']['borrower_id'],
									  es['deposits']['borrower_id'])
	r_loan_savings = ft.Relationship(es['loans']['borrower_id'],
										 es['savings']['borrower_id'])
	r_loan_withdrawal = ft.Relationship(es['loans']['borrower_id'],
											 es['withdrawal']['borrower_id'])
	r_loan_mpesa = ft.Relationship(es['loans']['borrower_id'],
									  es['mpesa']['borrower_id'])
	r_loan_images = ft.Relationship(es['loans']['borrower_id'],
									   es['images']['borrower_id'])
	r_loan_music = ft.Relationship(es['loans']['borrower_id'],
										es['music']['borrower_id'])
	r_loan_messages = ft.Relationship(es['loans']['borrower_id'],
											es['messages']['borrower_id'])
	r_loan_videos = ft.Relationship(es['loans']['borrower_id'],
										   es['videos']['borrower_id'])
	es = es.add_relationships(
								[  
									r_loan_withdrawal, r_loan_mpesa,
									r_loan_deposits, r_loan_savings,
									r_loan_images, r_loan_music,
									r_loan_messages,r_loan_videos
								]
							)
	return es



def do_default_feature_engineering(es):
	"""
	Creates features from the entity set for default prediction.

	Declare the metrics used by feature tools to create features, do 
	feature engineering and a dataframe.

	Args:
		es(obj): Feature tools object.
	Returns:
		df(dataframe): a dataframe

	"""
	agg_primitives = (
						[
							"sum", "std", "max", "skew", "min", "mean",
							"count", "mode", 'Trend'
						]
			 )
	trans_primitives =  (["day", "year", "month", "weekday"])
	# es = add_default_relations_to_entityset(es)
	feat_matrix, feat_names = ft.dfs(
										entityset=es,
										target_entity='kyc_data',
										agg_primitives = agg_primitives,
										trans_primitives = trans_primitives,
										n_jobs = 1,
										verbose = 1,
										features_only = False
									) 
	feat_matrix.reset_index(inplace = True)
	feat_df = pd.DataFrame(feat_matrix)
	# drop any column containing the word _id
	feat_df = feat_df[feat_df.columns.drop(list(feat_df.filter(regex='_id')))]
	feat_df.fillna(0, inplace=True) # replace missing values
	return feat_df


def do_limit_feature_engineering(es):
	"""
	Creates features from the entity set for limit prediction.

	Declare the metrics used by feature tools to create features, do 
	feature engineering and a dataframe.Here the loan data is 
	provided by the user seeking the loan. For details check 
	Users.users module

	Args:
		es(obj): Feature tools object.
	Returns:
		df(dataframe): a dataframe	
	"""
	agg_primitives = (
						[
							"sum", "std", "max", "skew", "min", "mean",
							"count", "mode", 'Trend'
						]
			 )
	trans_primitives =  (["day", "year", "month", "weekday"])
	# es = add_limit_relations_to_entityset(es)
	feat_matrix, feat_names = ft.dfs(
										entityset=es,
										target_entity='loans',
										agg_primitives = agg_primitives,
										trans_primitives = trans_primitives,
										n_jobs = 1,
										verbose = 1,
										features_only = False
									)
	feat_matrix.reset_index(inplace = True)
	feat_df = pd.DataFrame(feat_matrix)
	# drop any column containing the word _id
	feat_df = feat_df[feat_df.columns.drop(list(feat_df.filter(regex='_id')))]
	feat_df.fillna(0, inplace=True) # replace missing values
	return feat_df