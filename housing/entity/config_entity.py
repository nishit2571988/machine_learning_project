from collection import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["dataset_download_url",
                                                        "tgz_download_dir",
                                                        "raw_data_dir",
                                                        "ingested_train_dir",
                                                        "ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig",["schema_file_path"])

DataTransformationConfig = namedtuple("DataTransformationConfig",["add_bedroom_per_room",
                                                                "transformed_train_dir",
                                                                "transformed_test_dir",
                                                                "preprocessed_object_file_path"])

DataTrainerConfig = namedtuple("DataTrainerConfig",["trained_model_file_path","base_accuracy"])

DataEvaluationConfig = namedtuple("DataEvaluationConfig",["model_evaluation_file_paht","time_stamp"])

DataPusherConfig = namedtuple("DataPusherConfig",["export_dir_path"])