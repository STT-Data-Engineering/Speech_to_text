import re
import pandas as pd
import seaborn as sns  
import matplotlib.pyplot as plt 
sns.set_style("darkgrid")

from logger import get_logger

_logger = get_logger("FileHandler")
_logger.debug("Loaded successfully!")

class FileHandler():

    def __init__(self):
        pass
    
    def save_csv(self, df, csv_path, index=False):
        try:
            df.to_csv(csv_path, index=index)
            _logger.info("File saved as csv")

        except Exception:
            _logger.exception("File saving failed")

    def read_csv(self, csv_path):
        try:
            df = pd.read_csv(csv_path)
            _logger.debug("File is read as csv")
            return df

        except FileNotFoundError:
            _logger.exception("File is not found")