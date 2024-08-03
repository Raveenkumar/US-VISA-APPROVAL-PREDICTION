from dataclasses import dataclass
from us_visa.constants import  *
import os
from datetime import datetime

from us_visa.pipeline import training_pipeline

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

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
    
    
    
    