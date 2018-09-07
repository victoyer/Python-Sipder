HOSTNAME = '127.0.0.1'
DATABASE = 'QQ'
USERNAME = 'root'
DBPORT = 3306
PASSWORD = 'victor'
DB_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, DBPORT, DATABASE)
