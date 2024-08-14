from us_visa.exception import USvisaException
from us_visa.logger import logging
import sys
from pandas import DataFrame
from us_visa.entity.config_entity import DataPredictionConfig
from us_visa.entity.artifact_entity import DataTranformationArtifact
from us_visa.entity.s3_estimator import S3Estimator
from us_visa.utils.main_utils import load_obj


class GettingPredictionData:
    def __init__(self,case_id,
                 continent,
                 education_of_employee,
                 has_job_experience,
                requires_job_training,
                no_of_employees,
                yr_of_estab,
                region_of_employment,
                prevailing_wage,
                unit_of_wage,
                full_time_position):
        self.case_id=case_id
        self.continent=continent
        self.education_of_employee=education_of_employee
        self.has_job_experience=has_job_experience
        self.requires_job_training=requires_job_training
        self.no_of_employees=no_of_employees
        self.yr_of_estab=yr_of_estab
        self.region_of_employment=region_of_employment
        self.prevailing_wage=prevailing_wage
        self.unit_of_wage=unit_of_wage
        self.full_time_position=full_time_position
    
    def data_as_dict(self):# -> dict[str, obj]:
        """
        Description: This method used for convert the  data into directory
        :return:Dict
        :failure: Raise Exception
        """    
        try:
            dict_data = {'case_id': self.case_id,
            'continent': self.continent,
            'education_of_employee': self.education_of_employee,
            'has_job_experience': self.has_job_experience,
            'requires_job_training': self.requires_job_training,
            'no_of_employees': self.no_of_employees,
            'yr_of_estab': self.yr_of_estab,
            'region_of_employment': self.region_of_employment,
            'prevailing_wage': self.prevailing_wage,
            'unit_of_wage': self.unit_of_wage,
            'full_time_position': self.full_time_position}
            
            logging.info(f'data convert into dict : {dict_data} ')
            return dict_data
        
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)
    
    def dict_as_dataframe(self,data_dict: dict) -> DataFrame:
        """
        Description: This method used for convert the dict into dataframe
        :param data_dict: data in the form of dict
        :return: dataframe
        :failure: Raise Exception
        """   
        try:
            dataframe = DataFrame([data_dict])
            logging.info(f'dict converted into dataframe successfully.')
            return dataframe
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)
    
    def initiate_get_data_process(self) -> DataFrame:
        """
        Description: This method used for initiate the get data process
        :return: dataframe
        :failure:Raise Exception
        """
        try:
            data_dict = self.data_as_dict()
            dataframe = self.dict_as_dataframe(data_dict)
            logging.info(msg=f' prediction_data : {data_dict}')
            return dataframe
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)
       
       
       
       
class Prediction:
    def __init__(self,data_prediction_config:DataPredictionConfig,
                 prediction_data:DataFrame) -> None:
        self.data_prediction_config = data_prediction_config
        self.s3 = S3Estimator(bucket_name=self.data_prediction_config.s3_bucket_name)
        # self.getting_prediction_data = getting_prediction_data
        self.prediction_data = prediction_data
        
        
    def prediction_data_transformation_process(self):
        """
        Description: This method used for data preprocessing  process
        :return: transformend data
        :failure: raise Exception
        """
        try:
            preprocesser_obj = self.s3.load_model(model_path=self.data_prediction_config.s3_preprocesser_path)
            
            tranformed_data = preprocesser_obj.transform(self.prediction_data) #type:ignore
            
            logging.info('prediction data_transformation process  completed')
            
            return tranformed_data  
        
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)  
   
    def initiate_prediction_process(self):
        """
        Description: This Process used for initiate prediction
        :return: prediction data
        :failure: raise Exception
        """
        try:
            tranformed_data = self.prediction_data_transformation_process()
            target_encoder = self.s3.load_model(model_path=self.data_prediction_config.s3_targetencoder_path)
            model = self.s3.load_model(model_path=self.data_prediction_config.s3_model_path)

            prediction = model.predict(tranformed_data) #type: ignore
            
            final_prediciton = target_encoder.inverse_transform(prediction.reshape(-1,1))  #type: ignore
            
            logging.info(f'prediction : {final_prediciton}')
            
            return final_prediciton[0][0]
            
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys) 
       
               
       
       
       
       