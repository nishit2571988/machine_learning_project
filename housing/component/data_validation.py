from email import message
from tempfile import TemporaryFile
from evidently import dashboard
from housing.constant import DATA_DRIFT_DATA_DRIFT_KEY, DATA_DRIFT_DATA_KEY, DATA_DRIFT_DATASET_DRIFT_KEY, DATA_DRIFT_METRICS_KEY, SCHEMA_COLUMNS_KEY, SCHEMA_DOMAIN_VALUE_KEY
from sklearn.feature_selection import SelectFdr
from housing.util.util import read_yaml_file,save_json_file
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.artifact_entity import DataValidationArtifact
import os,sys
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
import pandas as pd
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:
    
    def __init__(self,data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*30}Data Valdaition log started.{'<<'*30} \n")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_train_test_file_exists(self)->bool:
        try:
            logging.info(f"Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)

            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> [{is_available}]")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file: [{training_file}] or Testing file: [{testing_file}] is not present"
                raise Exception(message)

            return is_available

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def validate_num_columns(self)->bool:
        try:
            validate_num_columns = False
            no_col_schema = len(self.schema[SCHEMA_COLUMNS_KEY])
            no_col_train_df = len(self.train_df.columns)
            no_col_test_df = len(self.test_df.columns)
            if (no_col_schema==no_col_train_df) and (no_col_schema==no_col_test_df):
                validate_num_cols = True
            
            logging.info(f"Number of Columns Check: Passed")
            return validate_num_columns                
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def validate_column_names(self)->bool:
        try:
            validate_column_names = False
            for column in self.train_df.columns:
                if not column in self.schema[SCHEMA_COLUMNS_KEY]:
                    message = f"{column} not in schema file"
                    raise Exception(message)
            validate_column_names = True
            
            logging.info(f"Column Names Check: Passed")
            return validate_column_names
            
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def validate_domain_values (self)->bool:
        try:
            validate_domain_values = False
            for column,category_list in self.schema[SCHEMA_DOMAIN_VALUE_KEY]. \
                items():
                for category in self.train_df[column].unique():
                    if category not in category_list:
                        message = f"[{column}] column does not accept <{category}>"
                        "in schema"
                        raise Exception(message)
            validate_domain_values = True
            
            logging.info(f"Domain Values Check: Passed")    
            return validate_domain_values
        
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def validate_column_dtypes (self):
        try:
            validate_column_dtypes = False
            for column in self.train_df.columns:
                try:
                    schema_dtype = self.schema[SCHEMA_COLUMNS_KEY][column]
                    column_dtype = str(self.train_df[column].dtype)
                    if not column_dtype == schema_dtype:
                        self.train_df[column].astype(schema_dtype)
                except Exception as e:
                    message = f"[{column}] : dtype [{column_dtype}] " + \
                    "\n {column_dtype} cannot be typecasted to <{schema_dtype}>"
                    raise Exception(message)
            
            validate_column_dtypes = True
            
            logging.info(f"Column Dtypes Check: Passed")
            return validate_column_dtypes      
              
        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            is_validated = False
            schema_file_path = self.data_validation_config.schema_file_path
            # read the schema
            self.schema = read_yaml_file(file_path=schema_file_path)
            # get the train & test data
            self.train_df,self.test_df =self.get_train_and_test_dataset()            
            
            #1. Number of Column
            validated_num_columns = self.validate_num_columns()
            #2. Check column names
            validated_column_names = self.validate_column_names()
            #3. Check the value of ocean proximity 
            validated_domain_values = self.validate_domain_values()
            #4. check dtypes of columns
            validated_column_dtypes = self.validate_column_dtypes()
            
            is_validated =  (validated_num_columns & validated_column_names 
                            & validated_domain_values & validated_column_dtypes)
            
            logging.info(f"Validation of Schema is Completed")
            return is_validated

            #commentedd
            validation_staus = False

            #Assignment validate training and testing dataset using schema file
            #1. Number of column
            #2. check the value of ocean proximity
            # acceptable values
            # <1H OCEAN
            # INLAND
            # ISLAND
            # NEAR BAY
            # NEAR OCEAN
            #3. check column name

            validation_staus = True
            return validation_staus
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_save_data_drift_report(self):
        try:
            logging.info("start save report") 

            profile = Profile(sections=[DataDriftProfileSection()])
            
            train_df,test_df=self.get_train_and_test_df()
            
            profile.calculate(train_df,test_df)
            
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)
            return report

            logging.info("Completed save report")
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            logging.info("start save report page")
            dashboard = Dashboard(tabs=[DataDriftTab()])

            train_df,test_df=self.get_train_and_test_df()

            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(self.data_validation_config.report_page_file_path)
            logging.info("completed save report page")
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self):
        try:
            validated_data_drift = False
            report = self.get_save_data_drift_report() 
            
            if report[DATA_DRIFT_DATA_DRIFT_KEY][DATA_DRIFT_DATA_KEY][
                DATA_DRIFT_METRICS_KEY][DATA_DRIFT_DATASET_DRIFT_KEY]:
                message = f"Data Drift is found in Dataset"
                raise Exception(message)
            self.save_data_drift_report_page()       

            validated_data_drift=True

            logging.info(f"Data Drift Check: Passed")
            return validated_data_drift
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_file_exists() 
            self.validate_dataset_schema()
            self.is_data_drift_found()
            data_validation_artifact=DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successfully"
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    
    
    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")
