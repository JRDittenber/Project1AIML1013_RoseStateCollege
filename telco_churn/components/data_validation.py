"""
Data Validation Module for Telco Churn Project 

This module defines the `DataValidation` class, which performs schema-based checks 
and data drift detection for the Telco Churn pipeline. 

Responsibilities include: 

- Loading a YAML schema that specifies the columns and their types/groups.
- Verifying that the incoming datates match the expected number of columns. 
- Verifying that all expected numerical and categorical columns exist. 
- Detecting data drift between a refernce (training) dataframe and current (testing) 
    dataframe using Evidently's profile + DataDriftProfileSection.
- Emitting a `DataValidationArtifact` that summarizes validation/drift outcomes and paths

"""

import json
import sys 

import pandas as pd 
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from pandas import DataFrame 

from telco_churn.exceptions import custom_exception
from telco_churn.logger import logging 
from telco_churn.utils import read_yaml_file, write_yaml_file
from telco_churn.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from telco_churn.entity.config_entity import DataValidationConfig
from telco_churn.constants import SCHEMA_FILE_PATH


class DataValidation:
    """
    Orchestrates dataset validation for the Telco Churn Pipeline.

    This class: 
    - Load schema configuration from the `SCHEMA_FILE_PATH`
    - Validates the number of columns and presence of numerical/categorical columns 
    - Detects data drift between training and testing dataframes using Evidently
    - Produce a `DataValidationArtifact` summarizing the validation 


    Parameters: 
    -----------------
    data_ingestion_artifact: DataIngestionArtifact 
        Output reference of the data ingestion stage. Expected to provide file paths such as 
        `trained_file_path` and `test_file_path`. 
    data_validation_config: DataValidationConfig
        Configuration object for data validation (e.g., paths to write drift reports)    
    
    --------------
    Attributes:
    --------------
    data_ingestion_artifact: DataIngestionArtifact
        Stored ingestion artifact used to located the training/testing datasets.
    data_validation_config: DataValidationConfig
        Stored configuration used to control validation output (e.g., drift report path)
    _schema_config: dict
        Parsed YAML schema loaded from `SCHEMA_FILE_PATH`. Expected to include keys such as 
        "columns", "numerical_columns", and "categorical_columns".

    ------
    Raises
    ------
    custom_exception
        Wraps and re-raises any underlying exceptions withi project specific context.  
    """

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        

