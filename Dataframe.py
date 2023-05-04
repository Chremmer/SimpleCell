import pandas as pd
from PyQt5.QtWidgets import QTableView
from PandasModel import PandasModel
from pandas import DataFrame as DataframeObject


# Convert excel file to dataframe
def excel_to_dataframe(file, sheetName):

    data = None

    try:
        data = pd.read_excel(file, sheetName)

    except Exception as e:
        print("Excel to dataframe error: " + str(e))

    return data


# Convert dataframe to excel file
def dataframe_to_excel(data, file, index=False):
    try:
        data.to_excel(file, index=index)

    except Exception as e:
        print("Dataframe to excel error: " + str(e))


def empty_df():
    return pd.DataFrame()
