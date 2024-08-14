from us_visa.logger import logging
from us_visa.exception import USvisaException
import sys

from us_visa.cloud_storage.aws_storage import SimpleStorageService


class S3Estimator:
    def __init__(self,bucket_name: str, model_path:str):
        self.s3 = SimpleStorageService()
        self.bucket_name = bucket_name
        self.model_path = model_path
    
    def load_model(self) -> object | None:
        """
        Description: This Method used for load the model from the s3 bucket
        :return: model object
        :failure: Raise exception
        """
        try:
            model_object = ""
            if self.s3.s3_key_path_available(bucket_name=self.bucket_name,s3_key=self.model_path):
                model_object = self.s3.load_model(bucket_name=self.bucket_name,model_name=self.model_path)
            
            else:
                model_object = None
            
            return model_object    
        
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)                  
    
    def upload_model(self,file_path):
        """
        Description: This method used for upload the model into s3 bucket
        :return: None
        :failure: Raise Exception
        """
        try:
            self.s3.upload_file(bucket_name=self.bucket_name,
                                file_path=file_path,
                                object_name=self.model_path)    
        
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)                  
    