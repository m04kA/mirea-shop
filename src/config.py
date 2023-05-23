import os

# DB_HOST = 'db_postgres'
# DB_PORT = '5432'
# DB_NAME = 'postgres'
# DB_USER = 'postgres'
# DB_PASS = 'postgres'
SECRET_KEY_TOKEN = 'SECRET'
SECRET_KEY_MANAGER = 'SECRET'


DB_HOST = os.getenv("DB_HOST", "db_postgres")
DB_PORT = os.getenv("DB_PORT", '5432')
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
# SECRET = os.environ.get("SECRET_KEY_TOKEN")
# SECRET = os.environ.get("SECRET_KEY_MANAGER")
