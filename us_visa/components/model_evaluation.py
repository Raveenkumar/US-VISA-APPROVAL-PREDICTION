from numpy import ndarray
from us_visa.logger import logging
from us_visa.exception import USvisaException
import sys
from typing import Any, Union
from pandas import DataFrame
from us_visa.entity.config_entity import ModelEvalutionConfig
from us_visa.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact,DataTranformationArtifact,ModelEvalutionArtifact
from us_visa.entity.s3_estimator import S3Estimator
from us_visa.utils.main_utils import read_data,read_yaml_file,load_obj
from sklearn.metrics import f1_score
from dataclasses import dataclass

@dataclass
class EvalutionResponse:
    change_in_score: ndarray
    trained_model_path:str
    existing_best_model_path: str


class ModelEvalution:
    def __init__(self,model_evalution_config:ModelEvalutionConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_tranformation_artifact:DataTranformationArtifact,
                 model_training_artifact:ModelTrainerArtifact) -> None:
        self.model_evalution_config = model_evalution_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_tranformation_artifact = data_tranformation_artifact
        self.model_training_artifact = model_training_artifact
        self.s3 = S3Estimator(bucket_name=self.model_evalution_config.s3_bucket_name,
                              model_path=self.model_evalution_config.s3_model_path)
    
    def get_best_model(self) -> object | None:
        """
        Description: This method used for getting the best model from s3 bucket
        :return: model object
        :failure: Raise Exception
        """
        try:
            best_model = self.s3.load_model()
            if best_model:logging.info(f'getting the best model from s3 :{best_model} getted successfully.')    
            else:logging.warning(msg=f'No model present in s3 bucket')   
            return best_model
        
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)
    
    def best_model_f1_score(self,X:DataFrame,y:DataFrame):# -> Float | ndarray[Any, Any] | Literal[0]:
        """
        Description: this method used for getting f1 score from the existing best_model
        :return: f1_score
        :failure: Raise Exception
        """
        try:
            # load preprocessing objects
            preprocesser_object = load_obj(self.data_tranformation_artifact.preprocessor_object_path)
            target_encoder_object = load_obj(self.data_tranformation_artifact.target_encoded_object_path)
            
            preprocessed_data = preprocesser_object.transform(X) # type: ignore
            encoded_target_variable = target_encoder_object.transform(y) # type: ignore

            # load best model
            best_model = self.s3.load_model()
            best_model_f1_score = 0
            if best_model:
                y_pred= best_model.predict(preprocessed_data) # type: ignore
                best_model_f1_score = f1_score(y_true=encoded_target_variable,y_pred=y_pred)
                logging.info(f'Getting best model f1_score: {best_model_f1_score}')
                return best_model_f1_score
            else:
                logging.info(f'No model exist in S3 bucket {self.model_evalution_config.s3_bucket_name} f1_score: {best_model_f1_score}')      
                return best_model_f1_score
                
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)
            
    def model_evalution_process(self) -> EvalutionResponse:
        """
        Description: This Method used for start the model evalution process
        :return: EvalutionResponse
        :failure: raise Exception
        """
        try:
            # getting test data
            test_data_path = self.data_ingestion_artifact.test_file_path
            test_data = read_data(datapath=test_data_path)
            
            # split data
            schema_data  = read_yaml_file(file_path=self.model_evalution_config.schema_file)
            target_variable = schema_data['target_column'][0]
            
            X = test_data.drop(columns=[target_variable])
            y = test_data[[target_variable]]
            
            # getting trained model f1-score
            present_trained_model_f1_score = self.model_training_artifact.metrics_path.f1_score
            
            # getting existing best model f1_score
            existing_best_model_f1_score = self.best_model_f1_score(X,y)
            
            # model resutls
            change_in_score = present_trained_model_f1_score-existing_best_model_f1_score
            
            result = EvalutionResponse(change_in_score=change_in_score, # type: ignore
                                       trained_model_path=self.model_training_artifact.model_path,
                                       existing_best_model_path=self.model_evalution_config.s3_model_path)
            
            logging.info(msg=f'Model evalution responce {result}')
            return result       
            
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)
        
    def initiate_model_evalution_process(self) -> ModelEvalutionArtifact:
        """
        Description: This method used for initiate the model evalution processs
        :return: ModelEvalutionArtifact
        :failure: Raise Exception
        """       
        try:
            evalution_responce = self.model_evalution_process()
            model_evalution_artifact = ModelEvalutionArtifact(change_in_score=evalution_responce.change_in_score, 
                                                              trained_model_path=evalution_responce.trained_model_path,
                                                              existing_best_model_path=evalution_responce.existing_best_model_path)

            logging.info(f"Model Evalution Artifact : {model_evalution_artifact}")
            return model_evalution_artifact
        except Exception as e:
            raise USvisaException(error_message=e, error_detail=sys)    
    