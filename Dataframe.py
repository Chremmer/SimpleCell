import pandas as pd
from PyQt5.QtWidgets import QTableView
from PandasModel import PandasModel
from pandas import DataFrame as DataframeObject


def excel_to_dataframe(file):

    data = None

    try:
        data = pd.read_excel(file)

    except Exception as e:
        print("Excel to dataframe error: " + str(e))

    return data


def dataframe_to_excel(data, file, index=False):
    try:
        data.to_excel(file, index=index)

    except Exception as e:
        print("Dataframe to excel error: " + str(e))





def test():
    print("thing")



def empty_df():
    return pd.DataFrame()
