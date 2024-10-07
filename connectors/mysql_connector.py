from sqlalchemy import create_engine
import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
port = os.getenv("DB_PORT")

# Connect to Database
print("Connecting to MySQL Database")
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')

connection = engine.connect()
print("Success connecting to MySQL Database")