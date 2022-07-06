import pandas as pd
import seaborn as sns  
import matplotlib.pyplot as plt 
sns.set_style("darkgrid")

from logger import get_logger

_logger = get_logger("Plotter")
_logger.debug("Loaded successfully!")

class Plotter():

    def __init__(self):
        pass


    def plot_bar(self, column, title, xlabel, ylabel):
        """ Plot a bar diagram for the recieved data column     
        """
        plt.figure(figsize=(10,7))
        sns.barplot(y=column.index, x=column.values) 
        plt.title(title, size=14, fontweight="bold")
        plt.xlabel(xlabel, size=13, fontweight="bold", ) 
        plt.ylabel(ylabel, size=13, fontweight="bold")
        plt.show() 