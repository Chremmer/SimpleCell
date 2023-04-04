import Dataframe
import os


def main():
    sample_file = os.getcwd() + "\\excel_sample\\sample_1.xlsx"

    data = Dataframe.excel_to_dataframe(sample_file)

    if data is None:
        data = Dataframe.empty_df()

    print(data)


main()
