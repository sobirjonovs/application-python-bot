from environs import Env

env = Env()
env.read_env()

db_driver = env.str('DB_DRIVER')
db_host = env.str('DB_HOST')
db_user = env.str('DB_USER')
db_pass = env.str('DB_PASSWORD')
db_database = env.str('DB_DATABASE')

admins = env.list('APP_ADMINS')
token = env.str('APP_TOKEN')
