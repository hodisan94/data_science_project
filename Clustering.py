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
import plotly.plotly as py
from urllib.request import urlopen
import json

# creating a Kmeans cluster
def Kmeans_clus(df, n_clusters, n_init):
    res = KMeans(n_clusters=n_clusters, init='random', n_init=n_init).fit_predict(df.iloc[:, 1:])
    df["Cluster"] = res
    return df

def scatter_plot(df):
    fig = Figure(figsize=(4, 4))
    # plt1 = fig.add_subplot(111) ?!!?!?!?!??!?!?!?!?!?!?!
    plot = plt.scatter(df["Social support"].to_numpy(), df["Generosity"].to_numpy(), s=9, c=df["Cluster"], alpha=0.5)

    cluster_list = df['Cluster'].unique().tolist()
    cluster_list = cluster_list.sort()
    cluster_list.append(len(cluster_list))
    plt.title("Social support as a dependency In attribute values of Generosity")
    plt.xlabel("Social support")
    plt.ylabel("Generosity")
    fig.colorbar(plot, boundaries=cluster_list)

    return fig


def horopleth_map(df):
    # we want the length of the column to set to color range
    length=len(df['Cluster'].unique().tolist()) - 1
    try:
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)

            fig = px.choropleth(df, geojson=counties, locations=df['country'], color=df['Cluster'],
                            range_color=(0, length),
                            locationmode="country names",
                            scope="world",
                            labels={'unemp': 'Cluster'}
                            )
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, title_text="choropleth map of Kmeans clustering by countries")
            fig.show()

            py.sing_in("hodisan94", "P023ybcdxGVcC131IZ7V")
            py.image.save_as(fig, filename='choropleth.png')
        return True
    except:
        return False




