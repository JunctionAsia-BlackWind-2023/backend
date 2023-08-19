from dotenv import load_dotenv   # dotenv 
import os                        # os 환경변수


load_dotenv()
mysql_connection_string = os.environ.get('MYSQL_CONNECTION_STRING')

'''
rds_connection_host     = os.environ.get('HOST')
rds_connection_port     = os.environ.get('PORT')
rds_connection_username = os.environ.get('USERNAME')
rds_connection_database = os.environ.get('DATABASE')
rds_connection_password = os.environ.get('PASSWARD')
'''

crypto_key = os.environ.get('CRYPTO_KEY')
# crypto_key = int(os.environ.get('CRYPTO_KEY')).to_bytes(16, byteorder='big')
print(crypto_key)
jwt_key = int(os.environ.get('JWT_KEY')).to_bytes(32, byteorder='big')
jwt_alorithm = os.environ.get('JWT_ALGORITHM')
access_token_expire_minutes = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))