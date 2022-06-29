from matplotlib.figure import Figure
from sklearn.cluster import KMeans
import plotly.express as px
import chart_studio.plotly as py
from urllib.request import urlopen
import json

# creating a Kmeans cluster
def Kmeans_clus(df, n_clusters, n_init):
    # creating a Kmeans model
    res = KMeans(n_clusters=n_clusters, init='random', n_init=n_init).fit_predict(df.iloc[:, 1:])
    df["Cluster"] = res
    return df

def scatter_plot(df):
    # creating a plot based on Social support and Generosity

    cluster_list = []
    fig = Figure(figsize=(5, 5))
    our_plot_fig = fig.add_subplot(111)

    cluster_list = df['Cluster'].unique().tolist()
    cluster_list.sort()
    x = df["Social support"].to_numpy()
    y = df["Generosity"].to_numpy()
    color = df["Cluster"]
    plot = our_plot_fig.scatter(x, y, s=9, c=color, alpha=0.5)
    cluster_list.append(len(cluster_list))
    fig.colorbar(plot, boundaries=cluster_list)
    our_plot_fig.title.set_text("Attribute values of Generosity depend on attribute values of Social support")
    our_plot_fig.set_xlabel("Social support")
    our_plot_fig.set_ylabel("Generosity")
    return fig


def horopleth_map(df):
    # we want the length of the column to set to color range
    length=len(df['Cluster'].unique().tolist()) - 1
    try:

        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)

            fig = px.choropleth(geojson=counties, locations=df['country'], color=df['Cluster'],
                                range_color=(0, length),
                                locationmode="country names",
                                scope="world",
                                labels={'unemp': 'Clusters'}
                                )
            fig.update_layout(margin={"r": 1, "t": 1, "l": 1, "b": 1},
                              title_text='K Means Clustering Visualization Per Country',
                              width=700,
                              height=700)

            py.sign_in("dhodisan", "3DyTzFJLcEaiLra9IEIT")
            py.image.save_as(fig, filename='choropleth.png')
        return True
    except:
        return False




