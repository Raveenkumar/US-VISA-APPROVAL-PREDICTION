from us_visa.data_access import data_access
from us_visa.exception import USvisaException
from us_visa.logger import logging
import sys
from us_visa.entity.config_entity import (DataAccessConfig,
                                          DataIngestionConfig,
                                          DataValidationConfig,
                                          DataTransformationConfig)
from us_visa.data_access.data_access import DataAccess
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTranformation



class TrainingPipeline:
    def __init__(self):
        self.data_access_config = DataAccessConfig()
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config  = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
    
    
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
            data_ingestion = DataIngestion(self.data_ingestion_config,raw_data=raw_data)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info('start the data ingestion completed!.')
            
            # data validation process
            logging.info('started Data validation process')
            data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                             data_ingestion_artifact=data_ingestion_artifact)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('started Data validation completed')
            
            
            
            # data transformation process
            # logging.info("start the data transformation process")
            # data_transformation  = DataTranformation(self.data_transformation_config,)
            
            
            
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)