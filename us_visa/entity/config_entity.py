from dataclasses import dataclass
from tkinter import Y

import yaml
from us_visa.constants import  *
import os
from datetime import datetime


from us_visa.pipeline import training_pipeline

TIMESTAMP: str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    timestamp: str = TIMESTAMP
    artifact_dir: str = os.path.join(ARTIFACT_DIR,timestamp)


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()   
    
@dataclass
class DataIngestionConfig:
    rawdata_file_path = os.path.join(training_pipeline_config.artifact_dir,RAW_DATA_DIR,RAW_DATA_FILE_NAME)
    trainingdata_file_path = os.path.join(training_pipeline_config.artifact_dir,TRAINING_DATA_DIR,TRAINING_DATA_FILE_NAME)
    testdata_file_path = os.path.join(training_pipeline_config.artifact_dir,TESTING_DATA_DIR,TEST_DATA_FILE_NAME)
    train_test_split_ratio = TRAIN_TEST_SPLIT_RATIO
    collection_name = COLLECTION_NAME
    db_name = DB_NAME
    
@dataclass
class DataValidationConfig:
        schema_file ="./config/schema.yaml"
        data_drift_file_path = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR,DATADRIFT_FILE_NAME)
        
    
    
    
    
    
    
    