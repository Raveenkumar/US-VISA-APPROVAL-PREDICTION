from us_visa.logger import logging
from us_visa.exception import USvisaException
import sys
import os
from pandas import DataFrame
from us_visa.entity.config_entity import DataIngestionConfig
# from us_visa.constants import RAW_DATA_FILE_NAME,TRAINING_DATA_FILE_NAME,TEST_DATA_FILE_NAME,TRAIN_TEST_SPLIT_RATIO
from sklearn.model_selection import train_test_split
from us_visa.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig, raw_data:DataFrame ):
        self.raw_data = raw_data
        self.raw_data_file_path = data_ingestion_config.rawdata_file_path
        self.training_data_file_path = data_ingestion_config.trainingdata_file_path
        self.test_data_file_path = data_ingestion_config.testdata_file_path
        self.train_test_split_ratio = data_ingestion_config.train_test_split_ratio
    
    def store_raw_data(self):
        """
        This method used for store the raw data into artifact/date-time/raw_data folder
        return: None
        failure : Raise exception
        """
        try:
            # create raw file path if not exist
            dir_path = os.path.dirname(self.raw_data_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            # store data to csv file
            self.raw_data.to_csv(self.raw_data_file_path,index=False,header=True)
            logging.info(f'raw data store successfully file_path: {self.raw_data_file_path}')
        
        except Exception as e:
            raise USvisaException(e,sys)
        
    
    def store_train_test_data(self):
        """
        This method used for seperate the train ,test data and store into artifact/date-time/train_data folder, artifact/date-time/test_data folder
        return : None
        failure :raise Exception
        
        """    
        try:
            # split data
            train_data,test_data = train_test_split(self.raw_data,test_size=self.train_test_split_ratio)
            logging.info('training_data and test_data splitted sucessfully')
            
            # get training_dir_path, test_dir_path
            training_dir_path = os.path.dirname(self.training_data_file_path)
            test_dir_path = os.path.dirname(self.test_data_file_path)
            
             # make train_data, test_data folder
            os.makedirs(training_dir_path, exist_ok=True)
            os.makedirs(test_dir_path,exist_ok=True)
            

            # store trian_data, test_data into its files
            train_data.to_csv(self.training_data_file_path,index=False,header=True)
            test_data.to_csv(self.test_data_file_path,index=False,header=True)
            
            logging.info(f'training_data & test_data stored successfully in train_data_path: {self.training_data_file_path} and test_data_path: {self.test_data_file_path}')
                  
        except Exception as e:
            raise USvisaException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method used for initiate the data_ingestion_process
        return : data_ingestion_articat 
        Failure: raise Exception
        """    
        try:
            # store raw_data into folder
            self.store_raw_data()
            
            # store  train,test_data
            self.store_train_test_data()
                        
            # store in artifact
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.training_data_file_path,test_file_path=self.test_data_file_path)
            
            logging.info('data ingestion process completed sucessfully')
            return data_ingestion_artifact
            
        except Exception as e:
            raise USvisaException(  e,sys)
        