"""
This script will load all the csv files in the data folder with pandas and checks the dimension of the pandas dataframe.
It is expected to have only two columns per csv file and at least 1 row.
"""

import os
import pandas as pd
import pytest

from spartacus import DataFolder, Spartacus, DatasetCSV


@pytest.mark.parametrize("data_folder", DataFolder)
def test_data_format(data_folder):
    if (
        data_folder == DataFolder.GRAICHEN_2000
        or data_folder == DataFolder.DAL_MASO_2014
        or data_folder == DataFolder.CHARBONNIER_2014
    ):
        return

    for subfile in os.listdir(data_folder.value):
        if subfile.endswith(".csv"):
            print("Loading file:", subfile)
            df = pd.read_csv(os.path.join(data_folder.value, subfile), header=None)
            print("Shape:", df.shape)
            print("Columns:", df.columns)
            print(df.head())
            df.columns = ["humerothoracic_angle", "value"]
            print("")

            if df.shape[1] != 2:
                raise ValueError("The csv file should have only two columns.")
            if df.shape[0] < 1:
                raise ValueError("The csv file should have at least one row.")

    print("All csv files have been loaded successfully.")


def test_data_loading():
    # open the file only_dataset_raw.csv
    df = pd.read_csv(DatasetCSV.CLEAN.value)
    print(df.shape)
    sp = Spartacus(dataframe=df)
    sp._load_rows()
    # df = load_confident_data(df, print_warnings=True)
    print(df.shape)
    return sp
