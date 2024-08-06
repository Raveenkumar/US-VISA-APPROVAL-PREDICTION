# from us_visa.data_access.data_access import DataAccess

# print(DataAccess().read_data_from_db())
# from h11 import Data
from us_visa.components.data_ingestion import DataIngestion



from us_visa.components.data_validation import DataValidation
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

import os
from us_visa.utils.main_utils import read_data
from us_visa.components.data_transformation import DataTranformation

# train_data_path = r'artifact\08_04_2024_00_27_58\training_data\training_data.csv'
# test_data_path = r'artifact\08_04_2024_00_27_58\test_data\test_data.csv'
# data_ingestion_artifact = DataIngestionArtifact(trained_file_path=train_data_path,test_file_path=test_data_path)
data_ingestion_artifact= DataIngestion().initiate_data_ingestion()
data_validation_artifact = DataValidation(data_ingestion_artifact).initiate_data_validation()


# # print(os.path.exists(train_data_path))
# # print(os.path.exists(test_data_path))

# dv = DataValidation(data_ingestion_artifact)

# print(dv.initiate_data_validation())



# df = read_data(train_data_path)
dt = DataTranformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
print(dt.initiate_data_transformation())