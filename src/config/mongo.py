import pymongo
from environs import Env

env = Env()
env.read_env()
mongo_conf = {
    # 'username': env("MONGO_AUTH_USERNAME"),
    # 'password': env("MONGO_AUTH_PASSWORD"),
    'db': env("MONGO_APP_DATABASE"),
    # 'authSource': env("MONGO_AUTH_DATABASE"),     
    'endPoint' : env("MONGO_ENDPOINT")
}















