# from us_visa.data_access.data_access import DataAccess

# print(DataAccess().read_data_from_db())
# # from h11 import Data
# from us_visa.components.data_ingestion import DataIngestion



# from us_visa.components.data_validation import DataValidation
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataTranformationArtifact, ModelTrainerArtifact,ClassificationMatrixArtifacts

# import os
# from us_visa.utils.main_utils import read_data
# from us_visa.components.data_transformation import DataTranformation


from us_visa.cloud_storage.aws_storage import SimpleStorageService

train_data_path = r'artifact\13_08_2024_21_36_06\ingestion_data\training_data\training_data.csv'
test_data_path = r'artifact\13_08_2024_21_36_06\ingestion_data\test_data\test_data.csv'
data_ingestion_artifact = DataIngestionArtifact(trained_file_path=train_data_path,test_file_path=test_data_path)
# data_ingestion_artifact= DataIngestion().initiate_data_ingestion()
# data_validation_artifact = DataValidation(data_ingestion_artifact).initiate_data_validation()


# # # print(os.path.exists(train_data_path))
# # # print(os.path.exists(test_data_path))

# # dv = DataValidation(data_ingestion_artifact)

# # print(dv.initiate_data_validation())



# # df = read_data(train_data_path)
# dt = DataTranformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
# print(dt.initiate_data_transformation())

# import os
# print(os.path.exists(r'artifact\06_08_2024_16_21_48\data_validation\report.yaml'))

# s3 = SimpleStorageService()
# # print(s3.get_bucket('rjes5854'))
# file = r"artifact\06_08_2024_16_21_48\data_transformation\transformed_object\preprocesser.dill"
# # s3.upload_file('rjes5854',file_path=file,object_name='disl.dill')
# preprocesser = s3.load_model(bucket_name='rjes5854',model_name='disl.dill')
# print(preprocesser)

preprocesser_obj = r"artifact\14_08_2024_14_27_57\data_transformation\transformed_object\preprocesser.dill"
target_encoder_obj = r"artifact\14_08_2024_14_27_57\data_transformation\transformed_object\target_encoder.dill"
training_numpy = r"artifact\14_08_2024_21_36_06\data_transformation\transformed_data\training_data.npy"
test_numpy = r"artifact\14_08_2024_21_36_06\data_transformation\transformed_data\test_data.npy"
data_transformation_artifact = DataTranformationArtifact(preprocessor_object_path=preprocesser_obj,
                                                         target_encoded_object_path=target_encoder_obj,
                                                         training_data_path=training_numpy,
                                                         testing_data_path=test_numpy)


model_trainer_artifact = ModelTrainerArtifact(model_path='artifact\\13_08_2024_21_36_06\\trained_models\\model.dill', metrics_path=ClassificationMatrixArtifacts(f1_score=0.8347597103357473, recall_score=0.8121263877028181, precision_score=0.8586907449209932))

from  us_visa.components.model_evaluation import ModelEvalution
from us_visa.entity.config_entity import ModelEvalutionConfig
mde = ModelEvalution(model_evalution_config=ModelEvalutionConfig(),
                     data_ingestion_artifact=data_ingestion_artifact,
                     data_tranformation_artifact=data_transformation_artifact,
                     model_training_artifact=model_trainer_artifact)

mde.initiate_model_evalution_process()