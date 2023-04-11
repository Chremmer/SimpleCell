import Dataframe
import os


def main():
    num_files = len(os.listdir(os.getcwd() + "\\excel_sample\\"))

    print(num_files)


main()
