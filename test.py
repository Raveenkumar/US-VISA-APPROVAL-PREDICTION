# from us_visa.data_access.data_access import DataAccess

# print(DataAccess().read_data_from_db())
# from h11 import Data
# from us_visa.components.data_ingestion import DataIngestion

# print(DataIngestion().initiate_data_ingestion())

from us_visa.components.data_validation import DataValidation
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os

train_data_path = r'artifact\08_04_2024_00_27_58\training_data\training_data.csv'
test_data_path = r'artifact\08_04_2024_00_27_58\test_data\test_data.csv'
data_ingestion_artifact = DataIngestionArtifact(train_data_path,test_data_path)


# print(os.path.exists(train_data_path))
# print(os.path.exists(test_data_path))

dv = DataValidation(data_ingestion_artifact)

print(dv.initiate_data_validation())