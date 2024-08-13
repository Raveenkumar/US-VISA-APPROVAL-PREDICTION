import sys
import json
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection    
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from us_visa.utils.main_utils import read_yaml_file,write_yaml_file,read_data,get_columns,get_columns_dypes
from pandas import DataFrame

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_yaml = read_yaml_file(data_validation_config.schema_file)
            self.columns = [list(column_data.keys())[0] for column_data in  self.schema_yaml['columns']]
            self.data_drift_filepath = data_validation_config.data_drift_file_path
        except Exception as e:
            raise USvisaException(e,sys)    
            
            
    def validate_no_of_columns(self,validation_columns:list) -> bool:
        """
        Description: This method used of validate no of columns 
        param : validationcolumns list
        return :bool bool (validate successfully return:True else return:False)
        failure: Raise Exception
        """
        try:
            no_of_columns = self.schema_yaml['number_of_columns'][0]['columns_length']
            no_of_validaition_columns = len(validation_columns)
            if no_of_validaition_columns == no_of_columns:
                logging.info('No of columns validation successfully')
                return True
            else:
                logging.info(f'No of columns validation failed no_of_columns: {no_of_columns} != no_of_validaition_columns: {validation_columns} ')
                return False
        
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)    
    
    def validate_column_names(self,validation_columns:list) -> bool:
        """
        Description: This method used of validate  columns names 
        param : validationcolumns list
        return :bool (validate successfully return:True else return:False)
        failure: Raise Exception
        """
        try:
            missing_columns_data = []
            for column in validation_columns:
                if column not in self.columns:
                    missing_columns_data.append(column)
            if len(missing_columns_data) ==0:
                logging.info('column names validation successfully')
                return True
            else:
                logging.info(f'column names validation failed columns: {missing_columns_data} not present in schema file')
                return False        
                
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)             
                    
    def validate_column_type(self,validation_columns_data: dict):
        """
        Description: This method used of validate  columns data types 
        Param: validation columns data in form dict {column:dtype}
        return :bool (validate successfully return:True else return:False)
        failure: Raise Exception
        """
        try:
            mismatch_columns_data = []
            mismatch_data = {'schema_column_data':"", 'validation_column_data':1}
            schema_columns_data = {list(column.keys())[0]:list(column.values())[0] for column in self.schema_yaml['columns']}
            for column  in schema_columns_data:
                if validation_columns_data[column] != schema_columns_data[column]:
                    mismatch_data.update({'schema_column_data':[column,schema_columns_data[column]]})
                    mismatch_data.update({'validation_column_data':[column,validation_columns_data[column]]})
                    
                    mismatch_columns_data.append(mismatch_data)
                    
            if len(mismatch_columns_data)==0:
                logging.info(f'column datatypes are validated successfully.')
                return True 
            else:
                logging.info(f'column datatypes are validated failed  mismatch column data: {mismatch_columns_data}')
                return False       
        except Exception as e:
            raise USvisaException(e,sys) 
        
    def detect_data_drift(self, reference_df: DataFrame, current_df: DataFrame):
        """
        This method used for detect data_draft from training_dataset and test_data if True drift is there 
        :param reference_df: referece dataframe
        :param current_df: current dataframe
        
        return: bool
        failure: raise Exception
        """
        try:
            data_drift_prifile = Profile(sections=[DataDriftProfileSection()])
            data_drift_prifile.calculate(reference_data=reference_df,current_data=current_df)
            
            # store report in json format
            report  = data_drift_prifile.json()
            json_report = json.loads(report)  
            
            # store data report 
            
            write_yaml_file(self.data_drift_filepath,json_report,False)
            
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
                              
        except Exception as e:
            raise USvisaException(e,sys)     
    
    def initiate_data_validation(self):
        """
        This method used for initiate data validation process
        :return: DataValidationArtifact
        :failure : Raise Exception
        """    
        try:
            # define error message if error message have no length then there is no error
            validation_error_message = ""
            # read the training_data, testing_data
            training_data_path = self.data_ingestion_artifact.trained_file_path
            test_data_path = self.data_ingestion_artifact.test_file_path
            
            train_df = read_data(training_data_path)
            test_df = read_data(test_data_path)
            
            #get columns 
            train_df_columns = get_columns(train_df) # type: ignore
            test_df_columns = get_columns(test_df) # type: ignore
            
            # validate the no of columns
            training_status = self.validate_no_of_columns(train_df_columns)
            test_status = self.validate_no_of_columns(test_df_columns)
            
            if not training_status:
                validation_error_message = f"validate number of training columns failed on path:{training_data_path}"
                
            if not test_status:
                validation_error_message = f"validate number of testing columns failed on path:{test_data_path}"    
                
           # validate the no of columns
            training_status = self.validate_column_names(train_df_columns)
            test_status = self.validate_column_names(test_df_columns)
            
            if not training_status:
                validation_error_message = f"validate training columns names failed on path:{training_data_path}"
                
            if not test_status:
                validation_error_message = f"validate testing column names failed on path:{test_data_path}"         
                
                
            # validate the columns and dtypes
            training_columns_info = get_columns_dypes(train_df)     #type: ignore
            test_columns_info = get_columns_dypes(test_df)     # type: ignore    
            
            training_status = self.validate_column_type(training_columns_info)
            test_status = self.validate_column_type(test_columns_info)
            
            if not training_status:
                validation_error_message = f"validate training columns dtypes failed on path:{training_data_path}"
                
            if not test_status:
                validation_error_message = f"validate testing column dtypes failed on path:{test_data_path}"
                
            
            # check data drift 
            drift_status = self.detect_data_drift(train_df,test_df) #type:ignore
            
            
            if len(validation_error_message)==0:
                validation_status=True
                if drift_status:
                    validation_error_message = f'Data Drift Detected Check drift file :{self.data_drift_filepath}'
                else:
                    validation_error_message = 'Data Drift not Detected'    
            else: 
                validation_status=False
            
            data_validation_artifact = DataValidationArtifact(validation_status,validation_error_message,self.data_drift_filepath)    
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact        
                                  
        except Exception as e:
            raise USvisaException(e,sys)
         