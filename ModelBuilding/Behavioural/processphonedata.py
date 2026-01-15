"""
Prepares phone data

"""

import pandas as pd
import numpy as np
import datetime


"""
Phone types is used in validating the correct type of data in 
every column. In case the data changes remember to update it.

"""
phone_types = {
				'borrower_id': 'int',
				'mpesa_amount': 'float',
				'mpesa_time_stamp': 'datetime',
				'month': 'str',
				'year': 'int', 
				'mpesa_airtime': 'int',
				'mpesa_banking': 'int',
				'mpesa_fuliza': 'int',
				'mpesa_gambling': 'int',
				'mpesa_incoming': 'int',
				'mpesa_loans': 'int',
				'mpesa_outgoing_sent_to': 'int', 
				'mpesa_utilities': 'int',
				'mpesa_withdrawal': 'int',
				'image_id': 'int',
				'image_date_added': 'datetime',
				'image_size': 'float',
				'image_gif': 'int',
				'image_heic': 'int',
				'image_jpeg': 'int',
				'image_jpg': 'int',
				'image_png': 'int',
				'image_webp': 'int',
				'image_x-ms-bmp': 'int',
				'message_id': 'int',
				'message_length': 'float',
				'message_time_stamp': 'datetime',
				'message_INCOMING': 'int',
				'message_OUTGOING': 'int', 
				'music_id': 'int',
				'music_date_added': 'datetime',
				'music_size': 'float',
				'music_3gpp': 'int',
				'music_aac': 'int',
				'music_aac-adts': 'int',
				'music_adpcm': 'int', 
				'music_amr': 'int',
				'music_amr-wb': 'int',
				'music_application/aac': 'int',
				'music_application/ogg': 'int',
				'music_flac': 'int',
				'music_m4a': 'int',
				'music_mp3': 'int',
				'music_mp4': 'int',
				'music_mpeg': 'int',
				'music_ogg': 'int',
				'music_quicktime': 'int',
				'music_wav': 'int',
				'music_x-matroska': 'int',
				'music_x-ms-wma': 'int',
				'music_x-wav': 'int',
				'video_id': 'int',
				'video_date_added': 'datetime',
				'video_size': 'float',
				'video_3gpp': 'int',
				'video_avi': 'int',
				'video_mp2ts': 'int',
				'video_mp4': 'int',
				'video_mpeg': 'int',
				'video_quicktime': 'int',
				'video_webm': 'int',
				'video_x-matroska': 'int'
				}

class WrappedPhone():
	"""
	A blueprint for preparing data.
	
	"""

	def impute_missing_columns(self, df, required_columns):
		"""
		Inserts missing columns in a data set.

		Given a dataframe extract and sort columns present in the
		dataframe. Compare it to the required columns and insert
		any columns that is required but missing with default
		values extracted from phone types.

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
				if phone_types[str(item)] == 'int' and item != 'year':
					df[str(item)] = 0
				if phone_types[str(item)] == 'float':
					df[str(item)] = 0
				if phone_types[str(item)] == 'datetime':
					df[str(item)] = datetime.datetime.now()
				if str(item) == 'month':
					df[str(item)] = datetime.datetime.now().month
				if str(item) == 'year':
					df[str(item)] = datetime.datetime.now().year
		return df


	def prepare_mpesa(self, df):
		"""
		Prepares mpesa data

		Covnvert columns to their appropirate data types and convert
		categorical variables to dummy variables. Remember when 
		fetching data there were columns that were missing. So drop
		any such columns in addition to the corporate_id and
		mpesa_spec_loc. Using the impute_missing_columns method
		defined in this class, repalce missing columns and remove
		unwanted columns.

		Args:
			df (obj): The mpesa data set
		
		Returns:
			df (obj): Cleaned dataset.
		"""
		mpesa = df
		mpesa['mpesa_time_stamp'] = pd.to_datetime(mpesa['mpesa_time_stamp'])
		mpesa['mpesa_type'] = mpesa['mpesa_type'].astype('str')
		mpesa = pd.get_dummies(mpesa,  columns=['mpesa_type'], prefix='mpesa')
		mpesa = mpesa.drop(columns=["corporate_id", 'mpesa_spec_loc'])
		# drop columns that contain the word missing
		mpesa = mpesa[mpesa.columns.drop(list(df.filter(regex='missing')))]
		required_columns = ['borrower_id', 'mpesa_amount', 'mpesa_time_stamp',
							'month', 'year', 'mpesa_airtime', 'mpesa_banking',
							'mpesa_fuliza', 'mpesa_gambling', 'mpesa_incoming',
							'mpesa_loans', 'mpesa_outgoing_sent_to', 
							'mpesa_utilities', 'mpesa_withdrawal']
		required_columns = sorted(required_columns)                   
		mpesa = self.impute_missing_columns(mpesa, required_columns)
		return mpesa 


	def sum_mpesa_amounts(self, df):
		"""
		Sums mpesa transactions.

		Extracts the month and year from the time_stamp. Replaces
		the amount spent with the actual amount spent, drop the 
		mpesa_id and timesamp, groupby the borrower_id, month,
		and year then find the sum for all the transactions.

		Args:
			df (obj): The mpesa data set

		Returns:
			df (obj): Cleaned dataset.
		"""
		mpesa = df
		mpesa['month'] = (
							pd.DatetimeIndex(mpesa['mpesa_time_stamp']).
							month_name()
						 )

		mpesa['year'] = pd.DatetimeIndex(mpesa['mpesa_time_stamp']).year
		mpesa["mpesa_airtime"] = mpesa["mpesa_airtime"] * mpesa["mpesa_amount"]
		mpesa["mpesa_fuliza"] = mpesa["mpesa_fuliza"] * mpesa["mpesa_amount"]
		mpesa["mpesa_gambling"] = (
									mpesa["mpesa_gambling"] * 
									mpesa["mpesa_amount"]
								   )
		mpesa["mpesa_incoming"] = (
										mpesa["mpesa_incoming"] * 
										mpesa["mpesa_amount"]
									)
		mpesa["mpesa_outgoing_sent_to"] = (
											mpesa["mpesa_outgoing_sent_to"] *
											 mpesa["mpesa_amount"]
											)
		mpesa["mpesa_utilities"] = (
										mpesa["mpesa_utilities"] * 
										mpesa["mpesa_amount"]
									)
		mpesa = mpesa.drop(columns=["mpesa_id", 'mpesa_time_stamp'])
		mpesa_sums = mpesa.groupby(['borrower_id', 'year', 'month']).agg({'mpesa_airtime':'sum', 
									'mpesa_fuliza':'sum',
									"mpesa_gambling":'sum', 
									"mpesa_incoming":'sum',
									'mpesa_outgoing_sent_to': 'sum',
									"mpesa_utilities":"sum"}
								 ).reset_index()
		mpesa_sums.rename(
					 columns={'mpesa_airtime':'mpesa_airtime_sum', 
							  "mpesa_fuliza":'mpesa_fuliza_sum',
							  "mpesa_gambling":"mpesa_gambling_sum",
							  "mpesa_loans":"mpesa_loans_sum",
							  "mpesa_incoming": "mpesa_incoming_sum",
							  "mpesa_outgoing_sent_to":"outgoing_sent_to_sum",
							  "mpesa_utilities":"mpesa_utilities_sum"},
							  inplace=True)
		return mpesa_sums


	def count_mpesa_amounts(self, df):
		"""
		Counts the number of mpesa transactions.

		Extracts the month and year from the time_stamp. Replaces
		the amount spent with the actual amount spent, drop the 
		mpesa_id and timesamp, groupby the borrower_id, month,
		and year then find the sum for all the transactions.
		
		Args:
			df (obj): The mpesa data set
		
		Returns:
			df (obj): Cleaned dataset.
		"""
		df['month'] = pd.DatetimeIndex(df['mpesa_time_stamp']).month_name()
		df['year'] = pd.DatetimeIndex(df['mpesa_time_stamp']).year
		df = df.drop(columns=["mpesa_id", 'mpesa_time_stamp'])
		df1_counts = (df.groupby(['borrower_id', 'year', 'month']).
								agg({'mpesa_airtime':'sum', 
								 "mpesa_fuliza":'sum', "mpesa_gambling":'sum',
								 'mpesa_incoming':'sum',
								 "mpesa_outgoing_sent_to":'sum',
								 "mpesa_utilities":'sum',
								  "mpesa_withdrawal":'sum'}
								 ).reset_index())
		df1_counts.rename(
					 columns={'mpesa_airtime':'mpesa_airtime_count',
							  'mpesa_fuliza': 'mpesa_fuliza_count', 
							  'mpesa_gambling': 'mpesa_gambling_count',
							  'mpesa_incoming':'mpesa_incoming_count',
							  'mpesa_outgoing_sent_to':'outgoing_sent_to_count',
							  'mpesa_utilities': 'mpesa_utilities_count'},
							  inplace=True)
		return df1_counts


	def summarize_mpesa(self, df, borrower_id):
		"""
		Combines mpesa counts and sums.

		Remove any missing columns created when fetching data,
		prepare the data set, call sum and counts methods merge the
		resulting data sets and convert the result to json.

		Args:
			df (obj): The mpesa data set.
			borrower_id (int): The person seeking the loan

		Returns:
			json: A json object for the summarised data set.
		"""
		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		df = df.loc[df['borrower_id'] == borrower_id]
		df1 = self.prepare_mpesa(df)
		df_sums = self.sum_mpesa_amounts(df1)
		df2 = self.prepare_mpesa(df)
		df_counts = self.count_mpesa_amounts(df2)
		df3 = pd.merge(
							df_sums, df_counts, how='left',
							on=['borrower_id', 'year', 'month']
						)
		df_tojson = df3.to_json(orient='records')[1:-1].replace('},{', '} {')
		return df_tojson


	def prepare_images(self, df):
		"""
		Prepares images data for prediction

		Remove image/ from the image_file_type column, convert the 
		same column to categorical variables using pd.get_dummies,
		drop the corporate_id and remove columns with the string
		missing. Confirm that no columns are missing or addtiional
		unwanted columns are present and retrun the final df.

		Args:
			df (obj): the images dataframe

		Returns:
			df (obj): A prepared dataframe
		"""

		images = df[df["image_file_type"] != 'image/*']
		images['image_file_type'] = (images['image_file_type'].
										str.replace('image/', ''))
		images = pd.get_dummies(
									images, columns=['image_file_type'],
									prefix = 'image'
								)
		images = images.drop(columns=["corporate_id"])
		images = (
					images[images.columns.
					drop(list(images.filter(regex='missing')))]
				 )
		required_columns = ['image_id', 'image_date_added', 'image_size',
							'borrower_id', 'image_gif', 'image_heic',
							'image_jpeg', 'image_jpg', 'image_png', 
							'image_webp', 'image_x-ms-bmp']
		required_columns = sorted(required_columns)
		images = self.impute_missing_columns(images, required_columns)
		return images

	def summarize_images(self, df, borrower_id):
		"""
		Sums image sizes.

		Removes any columns with the string 'missing'. Extracts
		the month name and year from image_date_added. Removes the
		string 'image/' form the image_file_type column. calculate
		statistics from the dataset and return the finals dataframe
		as json.

		Args:
			df (obj): The images data set

		Returns:
			df (obj): image summarised dataset.
		"""

		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		df['month'] = pd.DatetimeIndex(df['image_date_added']).month_name()
		df['year'] = pd.DatetimeIndex(df['image_date_added']).year
		df = df[df["image_file_type"] != 'image/*']
		df = df.loc[df['borrower_id'] == borrower_id] # filter for member_id
		# Agregate and find
		lastdf = (df.groupby(['image_file_type', 'year', 'month'],
								as_index=False).agg({'image_size':['sum',
								'mean', 'std', 'min', 'max', 'count']}))
		lastdf.columns = lastdf.columns.map('_'.join)
		lastdf = lastdf.fillna(0)
		# convert to json
		lastdf = lastdf.to_json(orient='records')[1:-1].replace('},{', '} {')
		return lastdf

	def prepare_messages(self, df):
		"""
		Prepare messages for prediction.

		Drop the corporate_id column, convert message_type and the
		message_direction columns to a string, the message_time_stamp
		column to date and do a pd.get dummies on message_type and 
		message_direction. Drop the message_INBOX column, extract
		month and year from message_time_stamp, and drop columns 
		the string 'missing'. Remove any additional columns and 
		insert any required columns that are missing.

		Args:
			df (obj): The images data set

		Returns:
			df (obj): image summarised dataset.
		"""
		df = df.drop(columns=["corporate_id"])
		df['message_type'] = df['message_type'].astype('str')
		df['message_direction'] = df['message_direction'].astype('str')
		df['message_time_stamp'] = pd.to_datetime(df['message_time_stamp'])
		df = pd.get_dummies(
								df,
								columns=['message_type', "message_direction"],
								prefix='message'
							)
		try:
			df = df.drop(columns=["message_INBOX"])
		except KeyError:
			pass
		df['month'] = pd.DatetimeIndex(df['message_time_stamp']).month_name()
		df['year'] = (pd.DatetimeIndex(df['message_time_stamp']).year)
		df = df.loc[:,~df.columns.str.contains('missing')]
		required_columns = [
								'message_id', 'message_length',
							 	'message_time_stamp',
								'borrower_id', 'message_INCOMING',
								'message_OUTGOING'
							]
		required_columns = sorted(required_columns)
		df = self.impute_missing_columns(df, required_columns)
		return df

	def summarize_messages(self, df, borrower_id):
		"""
		Sums messages sizes.

		Removes any columns with the string 'missing'. Extracts
		the month name and year from message_time_stamp. Calculate
		statistics from the dataset and return the finals dataframe
		as json.

		Args:
			df (obj): The messages data set

		Returns:
			df (obj): messages summarised dataset.
		"""
		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		df = df.loc[df['borrower_id'] == member_id] # filter for member_id
		# Agregate and find
		df['month'] = pd.DatetimeIndex(df['message_time_stamp']).month_name()
		df['year'] = pd.DatetimeIndex(df['message_time_stamp']).year
		lastdf = (df.groupby(['message_direction', 'year', 'month'],
								as_index=False).
								agg({'message_length':['sum', 'mean',
								'std', 'min', 'max', 'count']}))
		lastdf.columns = lastdf.columns.map('_'.join)
		lastdf = lastdf.fillna(0)
		# convert to json
		lastdf = lastdf.to_json(orient='records')[1:-1].replace('},{', '} {')
		return lastdf

	def prepare_music(self, df):
		"""
		Prepares music data for prediction

		Remove audio/ from the music_file_type column, convert the 
		same column to categorical variables using pd.get_dummies, drop
		the corporate_id and remove columns with the string missing.
		Convert the music_file_type columns to dummy variables and 
		confirm that no columns are missing or addtiional unwanted 
		columns are present and retrun the final df.

		Args:
			df (obj): the music dataframe

		Returns:
			df (obj): A prepared music dataframe
		"""
		music = df[df["music_file_type"] != 'audio/*']
		music['music_file_type'] = (
										music['music_file_type'].
										str.replace('audio/', '')
									)
		music = pd.get_dummies(
								music, 
								columns=['music_file_type'],
								prefix = 'music'
							  )
		music = music.drop(columns=["corporate_id"])
		music = music[music.columns.drop(list(music.filter(regex='missing')))]
		music['month'] = (
							pd.DatetimeIndex(music['music_date_added']).
							month_name()
						)
		music['year'] = pd.DatetimeIndex(music['music_date_added']).year
		required_columns = ['music_id', 'music_date_added', 'music_size',
							'borrower_id', 'music_3gpp', 'music_aac',
							'music_aac-adts', 'music_adpcm', 'music_amr',
							'music_amr-wb', 'music_application/aac', 
							'music_application/ogg', 'music_flac', 'music_m4a',
							'music_mp3', 'music_mp4', 'music_mpeg', 'music_ogg',
							'music_quicktime', 'music_wav', 'music_x-matroska',
							'music_x-ms-wma', 'music_x-wav', 'month', 'year']
		required_columns = sorted(required_columns)
		music = self.impute_missing_columns(music, required_columns)
		return music

	def summarize_music(self, df, borrower_id):
		"""
		Summarizes music data.

		Removes any columns with the string 'missing'. Removes the
		string 'image/' form the music_file_type column. Extracts
		the month name and year from music_date_added. calculate
		statistics from the dataset and return the finals dataframe
		as json.

		Args:
			df (obj): The images data set

		Returns:
			df (obj): image summarised dataset.
		"""
		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		df = df.loc[df['borrower_id'] == borrower_id] # filter for 
		df['music_file_type'] = df['music_file_type'].str.replace('audio/','')

		# Agregate and find
		df['month'] = pd.DatetimeIndex(df['music_date_added']).month_name()
		df['year'] = pd.DatetimeIndex(df['music_date_added']).year
		lastdf = (df.groupby(
								['music_file_type', 'year', 'month'],
								as_index=False).
								agg({'music_size':['sum', 'mean',
								'std', 'min', 'max', 'count']})
					)
		lastdf.columns = lastdf.columns.map('_'.join)
		lastdf = lastdf.fillna(0)
		# convert to json
		lastdf = lastdf.to_json(orient='records')[1:-1].replace('},{', '} {')
		return lastdf


	def prepare_videos(self, df):
		"""
		Prepares video data for prediction

		Remove video/ from the video_file_type column, convert the 
		same column to categorical variables using pd.get_dummies, drop
		the corporate_id and remove columns with the string missing.
		Convert the music_file_type columns to dummy variables and 
		confirm that no columns are missing or addtiional unwanted 
		columns are present and retrun the final df.

		Args:
			df (obj): the music dataframe

		Returns:
			df (obj): A prepared music dataframe
		"""
		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		videos = df
		videos['video_file_type'] = (
										videos['video_file_type'].
										str.replace('video/', '')
									)
		videos = pd.get_dummies(
									videos,
									columns=['video_file_type'],
									prefix = 'video'
								)
		videos = videos.drop(columns=["corporate_id"])
		videos = videos[
							videos.columns.drop(
								list(videos.filter(regex='missing'))
								)
						]
		videos['month'] = (
							pd.DatetimeIndex(videos['video_date_added']).
							month_name()
						  )
		videos['year'] = pd.DatetimeIndex(videos['video_date_added']).year
		required_columns = ['video_id', 'video_date_added', 'video_size',
							'borrower_id', 'video_3gpp', 'video_avi', 
							'video_mp2ts', 'video_mp4', 'video_mpeg',
							'video_quicktime', 'video_webm',
							'video_x-matroska']
		required_columns = sorted(required_columns)
		videos = self.impute_missing_columns(videos, required_columns)
		return videos


	def summarize_videos(self, df, borrower_id):
		"""
		Sumarizes video data.

		Extracts the month name and year from video_date_added. 
		Removes any columns with the string 'missing'. Removes the
		string 'video/' from the image_file_type column. calculate
		statistics from the dataset and return the final dataframe
		as json.

		Args:
			df (obj): The images data set

		Returns:
			df (obj): image summarised dataset.
		"""
		df = df.loc[df['borrower_id'] == borrower_id] # filter for member_id
		df['month'] = pd.DatetimeIndex(df['video_date_added']).month_name()
		df['year'] = pd.DatetimeIndex(df['video_date_added']).year
		df = df[df.columns.drop(list(df.filter(regex='missing')))]
		df['video_file_type'] = df['video_file_type'].str.replace('video/', '')
		# Agregate and find
		lastdf = df.groupby(['video_file_type', 'year', 'month'],
								as_index=False).agg({'video_size':['sum', 'mean',
								'std', 'min', 'max', 'count']})
		lastdf.columns = lastdf.columns.map('_'.join)
		lastdf = lastdf.fillna(0)
		# convert to json
		lastdf = lastdf.to_json(orient='records')[1:-1].replace('},{', '} {')
		return lastdf

