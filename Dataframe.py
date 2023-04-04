import pandas as pd


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


def empty_df():
    return pd.DataFrame()
