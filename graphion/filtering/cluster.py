"""
Author(s): Yuqin Cui, Steven Broek, Tom Udding
Created: 2019-06-12
Edited: 2019-06-19
"""
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Plot, LinearAxis, CustomJS
from bokeh.models.glyphs import Text
from bokeh.models.widgets.buttons import Button
from bokeh.plotting import figure
from collections import Counter
from colorcet import palette
from holoviews import opts, streams
from holoviews.streams import Selection1D
from numpy import array, linspace
from pandas import DataFrame, concat, Series
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def K_mean_cluster(dataframe):
    node_number = len(dataframe.columns)
    # if node_number >= 1500:
    #     print("The dataset is too large to cluster, use edge weight filter")
    # else:
    pca = PCA(n_components=1)
    newData = pca.fit_transform(dataframe.values)
    X = array(newData)

    n_clusters= node_number//200 + 1

    kmeans = KMeans(n_clusters= (node_number//200+1), random_state=0).fit(X)
    cluster_label = kmeans.labels_
    cluster_label = cluster_label.tolist()
    counter = Counter(cluster_label)

    names = dataframe.columns.tolist()
    cluster_label = Series(cluster_label)
    names_series = Series(names)
    cluster_label_df = concat([names_series, cluster_label], axis=1)
    cluster_label_df = DataFrame({'index': names,'cluster_label': cluster_label})

    check_frequency = counter.most_common(1)
    largest_cluster_label = check_frequency[0][0]
    largest_cluster_node_number = check_frequency[0][1]

    #check whether it's extremely unevenly distributed
    if largest_cluster_node_number >= node_number//3 and largest_cluster_node_number >=500 and node_number<1500:
        #sparate the whole dataset into 2 datasets, one biggest, one combined small others
        cluster_n = 2
        cluster_label_df.loc[cluster_label_df['cluster_label'] != largest_cluster_label, ['cluster_label']] = largest_cluster_label+1
        new_counter = {largest_cluster_label: largest_cluster_node_number, largest_cluster_label + 1 : node_number - largest_cluster_node_number}

        return cluster_n, new_counter, cluster_label_df
    else:
        cluster_n = n_clusters
        return cluster_n, counter, cluster_label_df


def generate_cluster_graph(dataframe):
    node_number = len(dataframe.columns)
    if node_number >= 150000:
        N = 40
        x = linspace(-2, 2, N)
        y = linspace(0,0, N)
        a = "Sorry, the dataset is too large to split"
        text = [a[i] for i in range(N)]
        source = ColumnDataSource(dict(x=x, y=y, text=text))
        plot = Plot(
            title=None, plot_width=600, plot_height=300,
            min_border=0, toolbar_location=None)

        glyph = Text(x="x", y="y", text="text", angle=0.1, text_color="#96deb3")
        plot.add_glyph(source, glyph)
        curdoc().add_root(plot)
        return plot
    else:
        cluster_n, counter, cluster_label_df = K_mean_cluster(dataframe)
        data = ColumnDataSource({"Label": list(counter.keys()), "Size": list(counter.values()),
                                 "circle_size": [item/10 + 10 for item in counter.values()],
                                 "color": [["olive","navy"][i%2] for i in counter.keys()]})

        data.selected.js_on_change('indices', CustomJS(args=dict(data=data), code="""
                let inds = cb_obj.indices;
                let labels = [];
                for (let i = 0; i < inds.length; i++){
                    let label = data.data.Label[inds[i]]
                    labels[i] = label
                }
                console.log(labels);
                $.post("/api/filter/clustering/choose/" + labels[0], function(response){
                    document.getElementById('start-tool-cluster').disabled = false;
                });
            """))

        TOOLTIPS = [
            ("Label", "@Label"),
            ("Number of nodes in this cluster", "@Size"),
        ]

        p = figure(plot_width=400, plot_height=400, title="Choose your cluster", tools=['wheel_zoom','box_zoom', 'hover','tap', 'reset'], tooltips=TOOLTIPS)
        p.circle("Label", "Label", size="circle_size", color="color", alpha=0.5, source=data)
        p.title.text_color = "olive"
        p.title.text_font = "times"
        p.title.text_font_style = "italic"

        p.background_fill_color = None
        p.border_fill_color = None
        p.outline_line_color = None
        #p.xaxis.visible = False
        p.yaxis.visible = False
        p.grid.visible = False
        return p

def get_dataframe_from_dot(dataframe, cluster_umber):
    cluster_n, counter, cluster_label_df = K_mean_cluster(dataframe)
    cluster_selected_index = cluster_label_df.loc[cluster_label_df['cluster_label'] == cluster_umber]
    cluster_selected_name_series = cluster_selected_index['index']
    cluster_selected_df = dataframe.loc[cluster_selected_name_series, cluster_selected_name_series]
    return cluster_selected_df