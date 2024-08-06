from datetime import datetime

# Database_constants
DB_NAME: str = "us_visa"
COLLECTION_NAME: str = "US_VISA"
MONGO_DB_URL: str = "MONGODB_URL"
# MONGO_DB_URL: str = "mongodb+srv://jraveen1997:raveenkumar@cluster0.q7ktbxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MONGODB_URL="mongodb+srv://jraveen1997:raveenkumar@cluster0.q7ktbxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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





