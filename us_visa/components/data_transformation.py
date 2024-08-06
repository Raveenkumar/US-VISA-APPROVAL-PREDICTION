import sys
from us_visa.exception import USvisaException
from us_visa.logger import logging
from datetime import datetime
from us_visa.utils.main_utils import read_yaml_file,read_data,DataFrameTransformer,save_numpy_array,save_obj
from us_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTranformationArtifact
from us_visa.entity.config_entity import DataTransformationConfig
from pandas import DataFrame
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder,FunctionTransformer,PowerTransformer,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN
import numpy as np





class DataTranformation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact):
        # This block of code is part of the constructor (`__init__` method) of the `DataTranformation`
        # class. Here's what it does:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.schema_yaml = read_yaml_file((DataTransformationConfig().schema_file))
            
            
            
        except Exception as e:
            raise USvisaException(e,sys)     
            
    def derivate_column(self,X: DataFrame) -> DataFrame:
        """
        This method used for derive a new feature which is usefull  [company age]
        :param X: X is dataframe that contains values
        :return: Dataframe
        :failure: Raise Exception
        """
        try:
            present_year = datetime.today().year
            derive_column = self.schema_yaml['derivated_columns'][0]
            X[derive_column] = present_year-X['yr_of_estab']
            logging.info(f'derive the feature: {derive_column} successfully')
            return X
        
        except Exception as e:
            raise USvisaException(e,sys) 
    
    def drop_unwanted_columns(self,X:DataFrame) -> DataFrame:
        """
        This method used for drop_unwanted_columns in X
        :param X: X is dataframe that contains values
        :return: Dataframe
        :failure: Raise Exception
        """
        try:
            drop_columns = self.schema_yaml['drop_columns']
            X.drop(columns=drop_columns,inplace=True)
            logging.info(f'drop the feature: {drop_columns} successfully')
            return X
        
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys) 

    def target_encoding(self,y:DataFrame):# -> ndarray[Any, Any]:
        try:
            target_encoder = OrdinalEncoder(categories=[['Certified', 'Denied']])
            encoded_y = target_encoder.fit_transform(y)
            logging.info(f'target feature :{self.schema_yaml['target_column'][0]} encoded  successfully')
            return encoded_y
            
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)    
    
    def initiate_data_preprocessing(self) -> Pipeline:
        """
        This method used for intiate data_preprocessing
        :return : pipeline obj 
        :failure: Raise Exception
        """
        try:
            # convet methods to sklearn Tranformers
            drop_columns_transformer = FunctionTransformer(func=self.drop_unwanted_columns)
            derive_column_transformer = FunctionTransformer(func=self.derivate_column, validate=False)

            # object of encoders
            one_hot_encoder = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()
            power_transformer = PowerTransformer()
            standard_scaler = StandardScaler()
            
            custom_preprocessor = Pipeline(steps=[
            ('derive_col', derive_column_transformer),
            ('drop_cols', drop_columns_transformer),
            ('to_df', DataFrameTransformer())
            ])
            
            num_features = self.schema_yaml['num_features']
            or_columns = self.schema_yaml['or_columns']
            oh_columns = self.schema_yaml['oh_columns']
            tranform_columns = self.schema_yaml['transform_columns']
            
            
            preprocesser = Pipeline(steps=[
                                    ('preprocessing', custom_preprocessor),
                                    ('column_trans', ColumnTransformer(
                                        transformers=[
                                            ('one_hot', one_hot_encoder, or_columns),
                                            ('ordinal', ordinal_encoder, oh_columns),
                                            ('power_trans', power_transformer, tranform_columns),
                                            ('scaling', standard_scaler, num_features)
                                        ],
                                        remainder='passthrough'))
                                    ])
            
            logging.info('preprocesser object created successfully')
            return preprocesser
                    
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)
        
    def data_transformation(self,df:DataFrame,preprocesser_obj: object=None):
        """
        This method used for intiate data_transformation  if validation status is true
        :return :  final_array , preprocesser_object
        :failure: Raise Exception
        """
        try:
            # if data validation is true then do data transformation
            if self.data_validation_artifact.validation_status:
                
                # get preprocesser object
                preprocesser = self.initiate_data_preprocessing()
                
                # get data and split it
                X = df.drop(columns=self.schema_yaml['target_column'])
                y = df[self.schema_yaml['target_column']]
                if preprocesser_obj:
                   preproced_x =preprocesser_obj.transform(X=X) # type:ignore
                   logging.info('test data preprocessing completed successfully.')
                else:    
                    preproced_x = preprocesser.fit_transform(X=X)
                    logging.info('training data preprocessing completed successfully.')
                encoded_y = self.target_encoding(y=y)
                
                # logging.info('preprocessing completed successfully.')
                
                ### handle imbalance of dataset
                sme = SMOTEENN(sampling_strategy="minority",random_state=42)
                X_res, y_res = sme.fit_resample(X=preproced_x, y=encoded_y) # type:ignore
                
                logging.info(msg=f"Im balance data handles completed successfully before records:{X.shape[0]}, after records:{X_res.shape[0]}")
                
                final_array = np.c_[X_res, y_res]
                return final_array , preprocesser
                
            else:
                e = self.data_validation_artifact.validation_message
                raise USvisaException(error_message=e,error_detail=sys)
        
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)    

    def initiate_data_transformation(self):
        """
        This method used for initiate the data tranformation process
        :return: DataTranformationArtifacdt
        :Failure: Raise Exception
        """
        try:
            # read the training, test data
            train_df = read_data(datapath=self.data_ingestion_artifact.trained_file_path)
            test_df = read_data(datapath=self.data_ingestion_artifact.test_file_path)
            
            # do data transforamtion for training_data
            final_train_data, preprocesser_object = self.data_transformation(df=train_df)
            final_test_data ,_ = self.data_transformation(df=test_df)
            
            # store the numpy training data,  numpy testing data
            save_numpy_array(file_path=DataTransformationConfig().data_transformatin_training_data_path,content=final_train_data)
            save_numpy_array(file_path=DataTransformationConfig().data_transformatin_test_data_path,content=final_test_data)
    
            # store the preprocesser object 
            save_obj(file_path=DataTransformationConfig().data_preprocessing_object_file_path,obj=preprocesser_object)
            
            data_tranformation_artifact = DataTranformationArtifact( preprocessor_object_path=DataTransformationConfig().data_preprocessing_object_file_path,
                                                                    training_data_path=DataTransformationConfig().data_transformatin_training_data_path,
                                                                    testing_data_path=DataTransformationConfig().data_transformatin_test_data_path)
            
            logging.info(f'data tranformation completed suceessfully , data_transformation artifact object : {data_tranformation_artifact}')
            return data_tranformation_artifact
        
        except Exception as e:
            raise USvisaException(error_message=e,error_detail=sys)    