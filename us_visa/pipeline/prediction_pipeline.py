from us_visa.exception import USvisaException
from us_visa.logger import logging
import sys
from us_visa.entity.config_entity import DataPredictionConfig
from us_visa.components.data_prediction import GettingPredictionData, Prediction


class PredictionPipeline:
    def __init__(self) -> None:
        self.data_prediction_config = DataPredictionConfig()

    def initiate_prediction(self,case_id,
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
        try:
            logging.info("prediction pipeline process started")
            
            prediction_data = GettingPredictionData(case_id=case_id,
                continent=continent,
                education_of_employee=education_of_employee,
                has_job_experience=has_job_experience,
                requires_job_training=requires_job_training,
                no_of_employees=no_of_employees,
                yr_of_estab=yr_of_estab,
                region_of_employment=region_of_employment,
                prevailing_wage=prevailing_wage,
                unit_of_wage=unit_of_wage,
                full_time_position=full_time_position).initiate_get_data_process()
            logging.info(msg='getting prediction data successfully!.')
            
            prediction_process = Prediction(data_prediction_config=self.data_prediction_config,
                                           prediction_data=prediction_data)
           
            final_prediction = prediction_process.initiate_prediction_process()
            logging.info('prediction process completed successfully.')
            
            logging.info("prediction pipeline process started")
            return final_prediction
        
        except Exception as e:
           raise USvisaException(error_message=e,error_detail=sys)