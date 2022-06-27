from platform import platform
from matplotlib.figure import Figure
import pandas as pd
import os
from sklearn import cluster
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import numpy as np
import plotly.express as px
# import chart_studio.plotly as py
from urllib.request import urlopen
import json

# checks that the file is with xlsx ending and read the the file.
def read_xlsx(path):
    split_path = os.path.splitext(path)
    file_extension = split_path[1]
    if file_extension != ".xlsx":
        return None
    else:
        df = pd.read_excel(path)
        return df


# fill NA values with mean value of the coulmn
def complete_vals(df):
    df = df.fillna(df.mean())
    return df

# normalization by standardization
def normalization_vals(df):
    columns = df.columns.to_list()
    for i in columns:
        # we don't want to standardized the country and year column
        if (i == "country" or i =="year"):
            continue
        else:
            # Standardization
            df[i] = (df[i] - df[i].mean()) / df[i].std()

    return df

def group_data(df):
    g1 = df.groupby(['country'], as_index=False).mean()
    g1.drop('year', inplace=True, axis=1)
    return g1

def export_to_excel(df):
    df.to_excel("PPData.xlsx")
    return

