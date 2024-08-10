from matplotlib.tri import TriAnalyzer
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.entity.artifact_entity import DataTranformationArtifact,ModelTrainerArtifact,ClassificationMatrixArtifacts
from us_visa.entity.config_entity import ModelTrainerConfig
import sys
from neuro_mf import ModelFactory
import numpy as np
from sklearn.metrics import f1_score,recall_score,precision_score
from us_visa.utils.main_utils import load_numpy_array,save_obj




class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTranformationArtifact) -> None:
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = ModelTrainerConfig()
    
    def get_model_trainier_object(self,train:np.ndarray,test:np.ndarray):
        """
        This method used for getting the trainier object
        :param X_train: the training dataset
        :param y_train: the training dataset contains labels
        :return: ModelTrainerArtifact
        :failure: raise Exception
        """        
        try:
            logging.info("Using neuro_mf to get best model object and report")
            #initialize the model factor
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            
            # split the dataset 
            X_train, y_train, X_test, y_test = train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            
            # find best model detials
            best_model_detials = model_factory.get_best_model(X=X_train,y=y_train,base_accuracy=self.model_trainer_config.model_excepted_accuracy)
            
            #get best model obj
            best_model_obj = best_model_detials.best_model
            
            if best_model_detials.best_score > self.model_trainer_config.model_excepted_accuracy:
                # get y_pred
                y_pred = best_model_obj.predict(X_test)
                
                # get scores
                f1 = f1_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                
                # store the score
                metric_artifact = ClassificationMatrixArtifacts(f1_score=f1, recall_score=recall, precision_score=precision) # type:ignore
                
                
                logging.info(msg=f"model trainied successfully metrics : {metric_artifact}") 
                
                return best_model_obj, metric_artifact
            
            else:
                raise Exception(f"Not find any best model : model accuracy: {best_model_detials.best_score} lower than excepted accuracy: {self.model_trainer_config.model_excepted_accuracy}")
            
            
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)
        
    
    def initiate_model_training(self):
        """
        This method used for initializing the training process
        :return: None
        :failure: Raise Exception
        """    
        try:
            # getting the  paths training data ,test data
            train_data_path = self.data_transformation_artifact.training_data_path
            test_data_path = self.data_transformation_artifact.testing_data_path
            
            # read the numpy arrays(training,testing)
            train_data = load_numpy_array(train_data_path)
            test_data = load_numpy_array(test_data_path)

            # provide this data to model_training_object
            best_model_obj, metric_artifact= self.get_model_trainier_object(train=train_data,test=test_data)
            
            # # store model,metric in model trainier artifacts
            model_trainier_artifact = ModelTrainerArtifact(model_path=best_model_obj, metrics_path=metric_artifact)
            
            logging.info(msg=f"initializing model training process completed successfully  model_detials {model_trainier_artifact}")
            
            save_obj(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model_obj)
            
            return model_trainier_artifact
        
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)