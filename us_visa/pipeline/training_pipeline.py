from us_visa.data_access import data_access
from us_visa.exception import USvisaException
from us_visa.logger import logging
import sys
from us_visa.entity.config_entity import DataAccessConfig
from us_visa.data_access.data_access import DataAccess


class TrainingPipeline:
    def __init__(self):
        self.data_access_config = DataAccessConfig()
    
    
    def initiate_training(self):
        """
        Description:This method  used for  initiate_training_process
        :return: None
        :failure: Raise Exception
        """    
        try:
            logging.info("Training Pipeline started is started")
            
            # data access process
            logging.info("start the data access process")
            data_access = DataAccess(self.data_access_config)
            raw_data = data_access.read_data_from_db()
            logging.info('data access process completed!.')
            
            
            # data ingestion process
            logging.info('start the data ingestion process')
                
        
            
            
            
        
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)