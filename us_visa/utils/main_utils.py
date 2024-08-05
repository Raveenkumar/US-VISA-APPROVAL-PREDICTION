import os
import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging
import yaml
from pandas import DataFrame
import pandas as pd

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