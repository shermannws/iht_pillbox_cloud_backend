import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")

def create_connection():
    try:
        connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_database
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def fetch_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT medicationtype, administeredtime, consumedtime FROM pillstatuses")
        records = cursor.fetchall()
        return records
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)