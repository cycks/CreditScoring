"borrower_id": [246126,234567,345678, 456789,567890,678901,789012,890123,901234,876590]
CREATE USER 'bayokwendo'@'localhost' IDENTIFIED BY 'Credit@bayo2020';

Deploying to AWS
=================================================================================
"""
	1. ssh into the server


"""
"mysql+mysqlconnector://bayokwendo:Credit@bayo2020@localhost/development"
DELETE FROM mysql.user WHERE user='' AND host='localhost';
FLUSH PRIVILEGES;


CREATE USER 'bayokwendo'@'localhost' IDENTIFIED WITH authentication_plugin BY 'Credit@bayo2020';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Credit@bayo2020';


scp backend.zip ubuntu@3.251.87.1:home/opt/creditscore


To copy an entire directory, add the -r recursive option:
scp -i . -r .backend.zip ubuntu@3.251.87.1:path/to/directory.

SELECT user,authentication_string,plugin,host FROM mysql.user;
 "cycks            | *E321624137DF7D26B1BAEB166CE8E70C76E6F8F7"  "mysql_native_password"


