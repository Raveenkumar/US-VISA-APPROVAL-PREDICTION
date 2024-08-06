from array import array
import os
import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging
import yaml
from pandas import DataFrame
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import dill
# from numpy import array

def read_yaml_file(file_path):
    try:
        # check file_exit or not
        if os.path.exists(file_path):
            # read yaml file
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            logging.info(f'yaml file {file_path} readed successfully.')    
            return data
        else:
            logging.error(f'{file_path} does not exist')
            raise Exception(f'{file_path} does not exist')
    
    except Exception as e:
        raise USvisaException(e,sys)

def write_yaml_file(file_path:str, content:object, replace: bool):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info('yaml file replaces.')
        else:
            logging.info('yaml file overwrited.')
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(data=content, stream=yaml_file)        
            
    except Exception as e:
        raise USvisaException(e,sys)
        
def read_data(datapath:str):
        """
        This method used for reading csv data (trainindata,testingdata)
        :param datapath :data path file
        :return: dataframe
        :failure: raise Exception
        """
        try:
            dataframe = pd.read_csv(datapath)
            logging.info(f'dataframe file : {datapath} readed successfully.')
            return dataframe
        except Exception as e:
            raise USvisaException(e,sys)
        
def get_columns(dataframe:DataFrame):
    """
    This method used for get the columns from the dataframe
    :param dataframe: dataframe
    :return: columns
    :failure: raise Exception
    """       
    try:
        columns = dataframe.columns.to_list() # type: ignore
        return columns
    except Exception as e:
        raise USvisaException(e,sys)

def get_columns_dypes(dataframe: DataFrame):
    """
    This method used for get the columns and dtype the dataframe
    :param dataframe: dataframe
    :return: dict {column:dtype}
    :failure: raise Exception
    """        
    try:
        column_info = {col: str(dtype) for col, dtype in dataframe.dtypes.items()}
        return column_info
    except Exception as e:
        raise USvisaException(e,sys)        
    
def save_numpy_array(file_path:str, content:array):
    """
    This method used for save the preprocessing data (numpy array)
    :param file_path: file_path of numpy array where want to save
    :param content: numpy array contains data
    :return : None
    :failure: Raise Exception
    """    
    try:
        dir_path =  os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,content)
        logging.info(f'save the numpy array successfully path:{file_path}')      
    except Exception as e:
        raise USvisaException(error_message=e,error_detail=sys)
    
def load_numpy_array(file_path:str):
    """
    This method used for load the numpy array of the file path
    :param file_path: This is file path of saved numpy array
    :return: numpy array
    :failure: Raise Exception
    """
    try:
        if os.path.exists(file_path):
            with open(file_path,'rb') as file_obj:
                result =  np.load(file=file_obj)
            logging.info(msg=f'numpy array loaded successfully: {file_path}')    
            return result
        else:
            e = Exception('faile to load numpy array  file path not exist')
            logging.info(msg=e)
            raise e
    except Exception as e:
        raise USvisaException(error_message=e,error_detail=sys)

def save_obj(file_path:str,obj: object):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file=file_obj)
        logging.info(msg=f'object saved successfully path: {file_path}')    
    except Exception as e:
        raise USvisaException(error_message=e,error_detail=sys)
    
def load_obj(file_path:str)-> object:
    """
    This method used for load the object 
    :param file_path: This is file of the object
    :return : object 
    :failure: Raise Exception
    """
    try:
        
        if os.path.exists(path=file_path):
            with open(file_path,mode='rb') as file_obj:
                result = dill.load(file=file_path)
            return result     
        else:
            e = Exception(f'object file path not exist path: {file_path}')    
            logging.info(msg=e)
            raise e
    
    except Exception as e:
        raise USvisaException(error_message=e,error_detail=sys)
    
class DataFrameTransformer(BaseEstimator, TransformerMixin):
    """
    This class used for avoid dataframe convertion error in custom preprocessing pipeline
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, np.ndarray):
            return pd.DataFrame(X, columns=self.columns_)
        return X

    def fit_transform(self, X, y=None, **fit_params):
        result = self.fit(X, y).transform(X)
        self.columns_ = result.columns if isinstance(result, pd.DataFrame) else []
        return result    