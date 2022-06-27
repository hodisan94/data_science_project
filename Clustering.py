from platform import platform
from matplotlib.figure import Figure
import pandas as pd
import os
from sklearn import cluster
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import preProcess as pp

import numpy as np
import plotly.express as px
# import chart_studio.plotly as py
from urllib.request import urlopen
import json

# creating a Kmeans cluster
def Kmeans_clus(df, n_clusters, n_init):
    res = KMeans(n_clusters=n_clusters, init='random', n_init=n_init).fit_predict(df.iloc[:, 1:])
    df["Cluster"] = res
    return df


