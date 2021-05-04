from pymongo import MongoClient
from django.conf import settings
import urllib.parse

MANGO_JWT_SETTINGS = settings.MANGO_JWT_SETTINGS

password = urllib.parse.quote(MANGO_JWT_SETTINGS['db_pass'])
username = urllib.parse.quote(MANGO_JWT_SETTINGS['db_user'])
db_name = MANGO_JWT_SETTINGS['db_name']
db_host_mongo = MANGO_JWT_SETTINGS['db_host']
# db_port_mongo = MANGO_JWT_SETTINGS['db_port']
# 'username': DB_USERID_MONGO,
# 'password': DB_PASSWORD_MONGO,
host= db_host_mongo ,
database = MANGO_JWT_SETTINGS['db_name']
# port = MANGO_JWT_SETTINGS['db_port']


if 'db_port' in MANGO_JWT_SETTINGS:
    db_port_mongo = MANGO_JWT_SETTINGS['db_port']
    # mongo_uri = ("mongodb://""{host}/?authSource={database}".format(host=host, database=database))

    mongo_uri = "mongodb://{username}:{password}@{db_host}:{db_port_mongo}/{db_name}".format(
        username=username, password=password, db_host=db_host_mongo,
        db_port_mongo=db_port_mongo, db_name=db_name)
else:
    print("hello")
    mongo_uri = "mongodb+srv://{username}:{password}@{host}/{db_name}".format(
        username=username, password=password, host=db_host_mongo, db_name=db_name)


client = MongoClient(mongo_uri)
database = client[db_name]