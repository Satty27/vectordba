import logging
from pymongo import MongoClient, errors
import certifi


class Connection:
    @classmethod
    def initialize_database(cls,url, database_name):
        try:
            database_client = MongoClient(url, connect=False, tlsCAFile=certifi.where(),)
            database_client.admin.command('ping')
            print("Connected successfully!")

            db = database_client[database_name]
            print("initialized database " + database_name)
            return db

        except errors.PyMongoError as e:
            print("--Printing db error---")
            logging.error(e)
            return {"result": False, "error": str(e)}

