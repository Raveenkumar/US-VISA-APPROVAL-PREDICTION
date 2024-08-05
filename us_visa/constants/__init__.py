# Database_constants
DB_NAME: str = "us_visa"
COLLECTION_NAME: str = "US_VISA"
MONGO_DB_URL: str = "MONGODB_URL"
# MONGO_DB_URL: str = "mongodb+srv://jraveen1997:raveenkumar@cluster0.q7ktbxf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Data Ingestion costants
RAW_DATA_DIR: str = "raw_data"
TRAINING_DATA_DIR: str ="training_data"
TESTING_DATA_DIR: str = "test_data"
PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"
RAW_DATA_FILE_NAME: str = "raw_data.csv"
TRAINING_DATA_FILE_NAME: str = "training_data.csv"
TEST_DATA_FILE_NAME: str = "test_data.csv"
TRAIN_TEST_SPLIT_RATIO : float = 0.25

# Data validation_constants
DATADRIFT_FILE_NAME: str = "report.yaml"
DATA_VALIDATION_DIR: str = "data_validation"


