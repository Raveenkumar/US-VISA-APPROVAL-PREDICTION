# from us_visa.data_access.data_access import DataAccess

# print(DataAccess().read_data_from_db())
# from h11 import Data
from us_visa.components.data_ingestion import DataIngestion

print(DataIngestion().initiate_data_ingestion())