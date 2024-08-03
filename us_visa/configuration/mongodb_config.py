import sys

from pymongo.mongo_client import MongoClient
from us_visa.logger import logging
from us_visa.exception import USvisaException

import os
import certifi
from us_visa.constants import MONGO_DB_URL,DB_NAME,COLLECTION_NAME


class MongoDBConnection:
    """
    class_name: MongoDBConnection
    Description :This class used for make secure connection to MongoDB Database
    Output: Provide connection
    Failure: Raise an Exeception
    
    """
    client = None
    def __init__(self) -> None:
        try:
            if MongoDBConnection.client==None:
                mongodb_uri  = os.getenv(MONGO_DB_URL)
                # print(mongodb_uri)
                if mongodb_uri is None:
                    raise Exception(f'Environment key :{mongodb_uri} is not set')
                # mongodb_uri = MONGO_DB_URL
                MongoDBConnection.client = MongoClient(mongodb_uri,tlsCAFile=certifi.where())
                self.client = MongoDBConnection.client
                # client.admin.command('ping')
                logging.info("You successfully connected to MongoDB!")
                
        except Exception as e:
            raise USvisaException(e,sys)    
        
        
        




