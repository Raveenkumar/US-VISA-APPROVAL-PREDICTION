from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str 

@dataclass
class DataValidationArtifact:
    validation_status: bool
    validation_message: str
    data_drift_file_path: str

@dataclass
class DataTranformationArtifact:
      preprocessor_object_path: str
      training_data_path: str
      testing_data_path: str
          