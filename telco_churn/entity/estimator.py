import sys

from pandas import DataFrame 
from sklearn.pipeline import Pipeline 

from telco_churn.exceptions import custom_exception
from telco_churn.logger import logging 

class TargetValueMapping:
    def __init__(self):
        self.No:int = 0
        self.Yes:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    
class TelcoModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        Parameters: preprocessing_object: Input Object of preprocessor
                    trained_model_object: Input Objectc of trained model     
        """    
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Description: Function accepts raw inputs and then transforms raw input 
                     using preprocessing_object to ensure that the inputs are 
                    the same format as the training data. Then performs predictions
                    on the transformed features
        """
        logging.info("Entered the predict method of TelcoModel class")

        try: 
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e: 
            raise custom_exception(e, sys) from e
        
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

    