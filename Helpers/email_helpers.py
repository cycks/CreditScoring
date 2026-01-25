"""
Responsible for sending emails
1. Sends email confirmation emails
2. Sends password reset emails.
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
	"""	
	Generates a token sent to the email.
	
	Using the URLSafeTimedSerializer and the secret 
	key imported from config.py using python-decouple
	Creates a token using the email and the secret
	key. Returns the generated token

	Args:
		email: The user's email meant to recieve an
				email from the app.
	Returns:
		token: A string generated.
	"""
	serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
	return serializer.dumps(email, salt=os.getenv('SECRET_KEY'))


def confirm_token(token, expiration=3600):
	"""	
	Validates tokens recived from emails.
	
	Using the URLSafeTimedSerializer decode the token
	sent from a users email.

	Args:
		token: A string sent from a users email.
		expiration: time to token expiration
	Returns:
		False: if the token is expired or wrong
		An email(str) if the token is valid	
	"""
	serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
	try:
		email = serializer.loads(
			token,
			salt=os.getenv('SECRET_KEY'),
			max_age=expiration
		)
	except:
		return False
	return email


def send_reg_email(email):
	"""
	Sends email confrimation message
	
	Generates a token using the email, provides a 
	link to process the confirmation, create a html
	head and tail messages creates a message by 
	conctenating the html_head, link and html_tail.
	
	Send the emai;l to the recipient.
	
	Args:
		email(str): The email awaiting confirmation
	Returns:
		True
	"""

	token = generate_confirmation_token(email)
	link = "http://127.0.0.1:5000/api/v1/confirm_email/" + token
	text_message = """\
	Hi,
	Welcome! Thanks for signing up.
	Please confirm your email by clicking the button below.
	"""
	html_head =  """\
	<html>
	  <body>
		<p> Welcome! Thanks for signing up.<br> </p>

		<p> 
			Please confirm your email by clicking the
		 	button below.
		</p>  
		<button type="button", 
			style="background-color: #4CAF50; 
			border-radius: 8px; border: none; 
			color: white; padding: 20px; 
			text-align: center; text-decoration: none; 
			display: inline-block; font-size: 16px; 
			margin: 4px 2px; border-radius: 8px; 
			cursor: pointer;" value="token">
			<a href="""
	
	html_tail = """\
			style="color: black; text-decoration:none;">
			Confirm email
			</a>
		</button type="button">
	  </body>
	</html>
	"""

	html_message = html_head + link + html_tail
	port = 465
	sender_email = 'creditscoring.infotrace@gmail.com'
	password = 'Creditscore@2019'
	receiver_email = email

	message = MIMEMultipart("alternative")
	message["Subject"] = "Confirm Your Email"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(text_message, "plain")
	part2 = MIMEText(html_message, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)
	message.attach(part2)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
		)
	return True




def send_passw_reset_email(email):
	"""	
	Sends password reset message
	
	Generates a token using the email, provides a 
	link to process the confirmation, create a html
	head and tail messages creates a message by 
	conctenating the html_head, link and html_tail.
	
	Send the email to the recipient.
	
	Args:
		email(str): The email awaiting confirmation
	Returns:
		True
	"""
	token = generate_confirmation_token(email)

	link = "http://127.0.0.1:5000/api/v1/confirm_email/" + token
	text_message = """\
	Hi,
	Please reset your password by clicking the button below.
	"""
	html_head =  """\
	<html>
	  <body>
		<p> Hi, <br> </p>

		<p> 
			Please reset your password by clicking the 
			button below
		</p>  
		<button type="button", 
			style="background-color: #4CAF50; 
			border-radius: 8px;  border: none; 
			color: white; padding: 20px;
			text-align: center; text-decoration: none;
			display: inline-block; font-size: 16px;
			margin: 4px 2px; border-radius: 8px;
			cursor: pointer;" value="token">
		<a href="""
	
	html_tail = """\
			style="color: black; text-decoration:none;">
			Reset Your Password.
			</a>
		</button type="button">
	  </body>
	</html>
	"""

	html_message = html_head + link + html_tail
	port = 465
	sender_email = 'creditscoring.infotrace@gmail.com'
	password = 'Creditscore@2019'
	receiver_email = email

	message = MIMEMultipart("alternative")
	message["Subject"] = "Confirm Your Email"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(text_message, "plain")
	part2 = MIMEText(html_message, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)
	message.attach(part2)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
		)
	return True

