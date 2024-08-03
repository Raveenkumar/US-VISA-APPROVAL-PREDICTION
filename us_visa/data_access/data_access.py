from us_visa.exception import USvisaException
from us_visa.logger import logging
import sys
from us_visa.configuration.mongodb_config import MongoDBConnection
from us_visa.entity.config_entity import DataIngestionConfig
import pandas as pd
import numpy as np
 

class DataAccess:
    def __init__(self) -> None:
        try:
            self.db_name = DataIngestionConfig().db_name
            self.collection_name = DataIngestionConfig().collection_name
            self.mongodb_connection= MongoDBConnection()
            self.mongodb_client = self.mongodb_connection.client
        except Exception as e:
           raise USvisaException(e,sys)
            
    def read_data_from_db(self) -> pd.DataFrame:
        """
        Description: This method used for read the raw data from data_base
        return: Dataframe
        Failure: Raise Exception
        """
        try:
            collection = self.mongodb_client[self.db_name][self.collection_name] #type:ignore
            mongodb_data = collection.find()
            df = pd.DataFrame(list(mongodb_data))
        
            # drop _id column generated by mongodb
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({'na':np.NAN},inplace=True) 
            logging.info("Extract the raw data from mongodb sucessfully.")
            return df   
    
        except Exception as e:
           raise USvisaException(e,sys)