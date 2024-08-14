import sys
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import ModelEvalutionArtifact
from us_visa.entity.s3_estimator import S3Estimator

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evalution_artifact:ModelEvalutionArtifact) -> None:
        self.model_pusher_config =model_pusher_config
        self.model_evalution_artifact = model_evalution_artifact
        self.s3 = S3Estimator(bucket_name=self.model_pusher_config.s3_bucket_name)
    
    def modelpusher_process(self) -> None:
        """
        Description: This method used for push the model into cloud
        :return: None
        :failure: Raise Exception
        """    
        try:
            if self.model_evalution_artifact.change_in_score>self.model_pusher_config.expected_accuracy_change:
                training_model_path = self.model_evalution_artifact.trained_model_path
                preprocesser_obj_path = self.model_evalution_artifact.preprocesser_obj_path
                target_encoder_obj_path = self.model_evalution_artifact.target_encoder_obj_path
                
                self.s3.upload_model(file_path=training_model_path,model_path=self.model_pusher_config.s3_model_path)
                self.s3.upload_model(file_path=preprocesser_obj_path,model_path=self.model_pusher_config.s3_preprocesser_path)
                self.s3.upload_model(file_path=target_encoder_obj_path,model_path=self.model_pusher_config.s3_targetencoder_path)
                logging.info(msg=f"change score:{self.model_evalution_artifact.change_in_score}>excepted_accuracy_change: {self.model_pusher_config.expected_accuracy_change}")
                logging.info(msg=f"training model({training_model_path}) upload in s3 bucket:({self.model_pusher_config.s3_bucket_name})")
                logging.info(msg=f"Preprocesser Obj ({preprocesser_obj_path}) upload in s3 bucket:({self.model_pusher_config.s3_bucket_name})")
                logging.info(msg=f"target encoder obj ({target_encoder_obj_path}) upload in s3 bucket:({self.model_pusher_config.s3_bucket_name})")
            
            else:
                 logging.info(msg=f"change score:{self.model_evalution_artifact.change_in_score}<excepted_accuracy_change: {self.model_pusher_config.expected_accuracy_change}")   
                 logging.info(msg=f"Existing model ins better one, availible in s3 bucket:({self.model_pusher_config.s3_bucket_name})")
                
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)
        
        
    def initiate_modelpusher_process(self):
        """
        Description: This method used for initiate the model pusher process
        :return: None
        :failure: Raise Exception
        """    
        try:
            self.modelpusher_process()
            logging.info("initiate  modelpusher process completed.")
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)