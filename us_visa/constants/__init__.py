from datetime import datetime

# Database_constants
DB_NAME: str = "us_visa"
COLLECTION_NAME: str = "US_VISA"
MONGO_DB_URL: str = "MONGODB_URL"


# Data Ingestion costants
RAW_DATA_DIR: str = "raw_data"
TRAINING_DATA_DIR: str ="training_data"
TESTING_DATA_DIR: str = "test_data"
PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"
INGESTION_DATA_DIR: str = 'ingestion_data'
RAW_DATA_FILE_NAME: str = "raw_data.csv"
TRAINING_DATA_FILE_NAME: str = "training_data.csv"
TEST_DATA_FILE_NAME: str = "test_data.csv"
TRAIN_TEST_SPLIT_RATIO : float = 0.25

# Data validation_constants
DATADRIFT_FILE_NAME: str = "report.yaml"
DATA_VALIDATION_DIR: str = "data_validation"

# Data Tranformation constants
DATA_TRANSFORMATION_DIR:str = 'data_transformation'
DATA_TRANSFORMATION_DATA_DIR: str = 'transformed_data'
DATA_TRANSFORMATION_OJBECT_DIR: str ='transformed_object'
DATA_TRANSFORMATION_PREPROCESSER_FILE_NAME:str = 'preprocesser.dill'
TARGET_ENCODER_FILE_NAME:str = 'target_encoder.dill'

# model training constants
TRAINED_MODEL_FILE_NAME:str ='model.dill'
TRAINED_MODEL_DIR:str ='trained_models'
MODEL_EXCEPTED_ACCURACY:float= 0.6


# AWS credentials
AWS_ACCESS_KEY_ID_ENV_KEY:str = 'AWS_ACCESS_KEY_ID_ENV_KEY'
AWS_SECRET_ACCESS_KEY_ENV_KEY:str = 'AWS_SECRET_ACCESS_KEY_ENV_KEY'
REGION_NAME:str = 'us-east-2'

# Model Evalution constants
S3_BUCKET_NAME:str = 'usvisamodels'
S3_MODEL_OBJECT_NAME:str = 'model.dill'
S3_PREPROCESSER_OBJECT_NAME:str = 'preprocesser.dill'
S3_TARGETENCODER_OBJECT_NAME:str = 'target_encoder.dill'

# Model pusher constants
EXCEPTED_ACCURACY_CHANGE:float = 0.15


#api_constants
APP_HOST = "0.0.0.0"
APP_PORT = 8080
