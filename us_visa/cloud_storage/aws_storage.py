import os,sys
from io import StringIO
import dill
from typing import Union,List
from matplotlib.tri import TriAnalyzer
from us_visa.logger import logging
from us_visa.exception import USvisaException
from mypy_boto3_s3.service_resource import Bucket
from us_visa.exception import USvisaException
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
from us_visa.configuration.aws_connection import S3Client

class SimpleStorageService:
    def __init__(self):
        s3_client = S3Client()
        self.s3_resource  = s3_client.s3_resource
        self.s3_client   = s3_client.s3_client
        
    
    def get_bucket(self,bucket_name:str):
        """
        Description : This method used for gets the bucket object based on the bucket name.
        :param bucket_name: The name of the bucket
        :return: The bucket object
        :failure: Raise exception
        """
        try:
           bucket = self.s3_resource.Bucket(bucket_name) # type: ignore
           logging.info(f"getting bucket name {bucket_name} successfully.")
           return bucket
       
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)
        
    
    def s3_key_path_available(self, bucket_name:str, s3_key:str):
        """
        Description : This method used for check s3_key_path_available or not
        :param bucket_name: The name of the bucket
        :param s3_key: The name of the key(file or directory)
        :return: bool
        :failure: Raise an exception
        
        """ 
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            if len(file_objects) > 0:
                logging.info(f"file path existed : {bucket_name}/{s3_key}")
                return True
            else:
                logging.info(f"file path  not existed : {bucket_name}/{s3_key}")
                return False
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)   
        
        
    def create_folder(self, bucket_name, folder_name):
        """
        Description : This method used for create a folder in the bucket
        :param bucket_name: Bucket name
        :param folder_name: Name of the folder
        :return: None
        :failure: Raise exception
        """
        
        try:
            if  not self.check_folder_exists(bucket_name, folder_name):
                self.s3_resource.Object(bucket_name, folder_name).put() # type: ignore
                logging.info(f'folder created successfully : {bucket_name}/{folder_name}')
                
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)  
        
    
    def check_folder_exists(self, bucket_name,folder_name):
        """
        Description : This method used for check folder in the bucket exists or not
        :param bucket_name: Bucket name
        :param folder_name: Name of the folder
        :return: True if folder exists else False
        :failure: Raise Exception
        """    
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()  # type: ignore
            logging.info(f"folder already exists :{bucket_name}/{folder_name}")
            return True
        
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logging.info(f"folder not exists :{bucket_name}/{folder_name}")
                return False
            
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys) 
        
    
    def upload_file(self,bucket_name:str,file_path:str,object_name:str ):
        """
        This method used for upload the file  into bucket
        :param bucket_name: Name of the bucket
        :param file_path: Path to the file
        :param object_name: Name of the object
        
        """ 
        
        try:
            # Upload files to S3 bucket 
            self.s3_resource.Bucket(bucket_name).upload_file(Filename=file_path, Key=object_name) # type: ignore
            logging.info(f'uploaded file successfully bucket_name :{bucket_name},local_file: {file_path}, uploaded_file :{object_name}')
            
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)    
            
    
    def  get_file_object(self,filename:str, bucket_name:str):
        """
        Description: This method used for getting the file object from s3 bucket
        :param filename: Name of the file
        :param bucket_name: Bucket Name
        :return: file_objs
        :failure: Raise Exception
        """
        try:
            bucket = self.get_bucket(bucket_name)
            
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            
            func = lambda x: x[0] if len(x)==1 else x
            
            file_objects = func(file_objects)
            
            return file_objects
        
        except Exception as e:
            raise USvisaException(e, sys)     
            
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Description :   This method reads the object_name object with kwargs
        Output      :   The column name is renamed
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            func = (
                lambda: object_name.get()["Body"].read().decode() # type: ignore
                if decode is True
                else object_name.get()["Body"].read()  # type: ignore
            )
            conv_func = lambda: StringIO(func()) if make_readable is True else func()
            logging.info(f"read the file object object_name :{object_name}")
            return conv_func()

        except Exception as e:
            raise USvisaException(e, sys) 
    
  
    def load_model(self,bucket_name: str, model_name: str ,model_dir: str = None) -> object: # type: ignore
        """
        Description :   This method loads the model_name model from bucket_name bucket with kwargs
        Output      :   list of objects or object is returned based on filename
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )
            model_file = func()
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = dill.loads(model_obj)
            logging.info(f"load model succesfully, bucketname: {bucket_name} model_name :{model_name} ")
            return model
        
        except Exception as e:
            raise USvisaException(e, sys)      