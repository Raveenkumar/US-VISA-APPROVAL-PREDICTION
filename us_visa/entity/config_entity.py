from dataclasses import dataclass
import dataclasses
from tkinter import Y

import yaml
from us_visa.constants import  *
import os
from datetime import datetime


TIMESTAMP: str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    timestamp: str = TIMESTAMP
    artifact_dir: str = os.path.join(ARTIFACT_DIR,timestamp)


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()   
    
@dataclass
class DataAccessConfig:
        collection_name = COLLECTION_NAME
        db_name = DB_NAME
            
    
@dataclass
class DataIngestionConfig:
    rawdata_file_path = os.path.join(training_pipeline_config.artifact_dir,INGESTION_DATA_DIR,RAW_DATA_DIR,RAW_DATA_FILE_NAME)
    trainingdata_file_path = os.path.join(training_pipeline_config.artifact_dir,INGESTION_DATA_DIR,TRAINING_DATA_DIR,TRAINING_DATA_FILE_NAME)
    testdata_file_path = os.path.join(training_pipeline_config.artifact_dir,INGESTION_DATA_DIR,TESTING_DATA_DIR,TEST_DATA_FILE_NAME)
    train_test_split_ratio = TRAIN_TEST_SPLIT_RATIO
    collection_name = COLLECTION_NAME
    db_name = DB_NAME
    
@dataclass
class DataValidationConfig:
        schema_file ="./config/schema.yaml"
        data_drift_file_path = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR,DATADRIFT_FILE_NAME)
        

@dataclass
class DataTransformationConfig:
        schema_file ="./config/schema.yaml"
        data_transformatin_data_path = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR,DATA_TRANSFORMATION_DATA_DIR)
        data_transformatin_training_data_path = os.path.join(data_transformatin_data_path,TRAINING_DATA_FILE_NAME.replace("csv","npy"))
        data_transformatin_test_data_path = os.path.join(data_transformatin_data_path,TEST_DATA_FILE_NAME.replace("csv","npy"))
        data_preprocessing_object_file_path = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR,DATA_TRANSFORMATION_OJBECT_DIR,DATA_TRANSFORMATION_PREPROCESSER_FILE_NAME)
        
@dataclass
class ModelTrainerConfig:
        trained_model_file_path = os.path.join(training_pipeline_config.artifact_dir,TRAINED_MODEL_DIR,TRAINED_MODEL_FILE_NAME)
        model_excepted_accuracy = MODEL_EXCEPTED_ACCURACY
        model_config_file_path =  os.path.join("config", "model.yaml")
         
        
    
    
    
    
    