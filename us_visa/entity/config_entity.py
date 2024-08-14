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
        collection_name:str = COLLECTION_NAME
        db_name:str = DB_NAME
            
    
@dataclass
class DataIngestionConfig:
    rawdata_file_path: str= os.path.join(training_pipeline_config.artifact_dir,INGESTION_DATA_DIR,RAW_DATA_DIR,RAW_DATA_FILE_NAME)
    trainingdata_file_path: str = os.path.join(training_pipeline_config.artifact_dir,INGESTION_DATA_DIR,TRAINING_DATA_DIR,TRAINING_DATA_FILE_NAME)
    testdata_file_path: str = os.path.join(training_pipeline_config.artifact_dir,INGESTION_DATA_DIR,TESTING_DATA_DIR,TEST_DATA_FILE_NAME)
    train_test_split_ratio: float = TRAIN_TEST_SPLIT_RATIO
    collection_name: str = COLLECTION_NAME
    db_name: str = DB_NAME
    
@dataclass
class DataValidationConfig:
        schema_file: str ="./config/schema.yaml"
        data_drift_file_path: str = os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR,DATADRIFT_FILE_NAME)
        

@dataclass
class DataTransformationConfig:
        schema_file: str ="./config/schema.yaml"
        data_transformatin_data_path: str = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR,DATA_TRANSFORMATION_DATA_DIR)
        data_transformatin_training_data_path: str = os.path.join(data_transformatin_data_path,TRAINING_DATA_FILE_NAME.replace("csv","npy"))
        data_transformatin_test_data_path: str = os.path.join(data_transformatin_data_path,TEST_DATA_FILE_NAME.replace("csv","npy"))
        data_preprocessing_object_file_path: str = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR,DATA_TRANSFORMATION_OJBECT_DIR,DATA_TRANSFORMATION_PREPROCESSER_FILE_NAME)
        target_encoder_object_file_path: str = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR,DATA_TRANSFORMATION_OJBECT_DIR,TARGET_ENCODER_FILE_NAME)
        
@dataclass
class ModelTrainerConfig:
        trained_model_file_path: str = os.path.join(training_pipeline_config.artifact_dir,TRAINED_MODEL_DIR,TRAINED_MODEL_FILE_NAME)
        model_excepted_accuracy: float = MODEL_EXCEPTED_ACCURACY
        model_config_file_path: str =  os.path.join("config", "model.yaml")
         

@dataclass
class ModelEvalutionConfig:
        s3_bucket_name: str = S3_BUCKET_NAME
        s3_model_path: str = S3_MODEL_OBJECT_NAME
        schema_file: str ="./config/schema.yaml"
        
        
@dataclass
class ModelPusherConfig:
        expected_accuracy_change:float = EXCEPTED_ACCURACY_CHANGE
        s3_bucket_name: str = S3_BUCKET_NAME
        s3_model_path: str = S3_MODEL_OBJECT_NAME
        s3_preprocesser_path: str = S3_PREPROCESSER_OBJECT_NAME
        s3_targetencoder_path: str = S3_TARGETENCODER_OBJECT_NAME    

    
@dataclass
class DataPredictionConfig:
        s3_bucket_name: str = S3_BUCKET_NAME
        s3_model_path: str = S3_MODEL_OBJECT_NAME   
        s3_preprocesser_path: str = S3_PREPROCESSER_OBJECT_NAME
        s3_targetencoder_path: str= S3_TARGETENCODER_OBJECT_NAME    
     
    
    
    
    