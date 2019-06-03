"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-05-31
"""
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import numpy as np
from bokeh.plotting import figure
from bokeh.models import BoxSelectTool, CustomJS, ColumnDataSource
from bokeh.models.widgets import Paragraph
import pandas
from pandas import read_hdf
import time

def generate_selection(file, kind="degree", dir="in", dataframe=False):
    if file is None or file.size == 0:
        p = Paragraph(text="""No nodes left""")
        return p

    # big_bang = time.time()

    if (kind == "degree"):
        edges=False
    else:
        edges=True

    limit = 1000

    begin = time.time()
    if not dataframe:
        df = read_hdf(file)
    else:
        df = file

    names = df.columns.tolist()

    # print("Reading data {}-{}: ".format(dir, kind) + str(time.time()-begin))

    # begin = time.time()
    ### BASIC DEGREE COUNTING
    if (not edges):
        if (dir == "in"):
            deg_all = (df.ne(0).sum(axis=1)).to_numpy(copy=True)
        if (dir == "out"):
            deg_all = (df[df.columns].ne(0).sum(axis=1)).to_numpy(copy=True)
    else:
        adj_matrix = df.to_numpy(copy=True)  # convert dataframe to numpy array for efficiency
        deg_all = adj_matrix.flatten()

    # print("Degree counting/edge weights {}-{}: ".format(dir, kind) + str(time.time() - begin))
    # begin = time.time()
    if (len(deg_all) > limit):
        deg = np.random.choice(deg_all, limit, replace=False)
        #deg = deg_all[:limit]
        # print("Random sampling: {}-{}: ".format(dir, kind) + str(time.time() - begin))
        # begin = time.time()
        np.append(deg, np.array([max(deg_all)]))
        np.append(deg, np.array([min(deg_all)]))
        # print("Appending: {}-{}: ".format(dir, kind) + str(time.time() - begin))
    else:
        deg = deg_all

    # begin = time.time()
    deg_all = np.reshape(deg_all, (-1, 1))
    deg = np.reshape(deg, (-1, 1))
    # print("Reshaping: {}-{}: ".format(dir, kind) + str(time.time() - begin))
    deg_plot = np.linspace(-max(deg)[0] / 15, max(deg_all)[0] + max(deg_all)[0] / 15, 1000)
    # Calculate 'pretty good' (since best takes a long time) bandwidth
    # begin = time.time()
    #
    # grid = GridSearchCV(KernelDensity(),
    #                     {'bandwidth': np.linspace(0.1, 10.0, 20)},
    #                     cv=min(len(deg), 5),
    #                     iid=False)  # 5-fold cross-validation
    # grid.fit(deg)
    # print("Bandwidth: {}-{}: ".format(dir, kind) + str(time.time()-begin))
    # begin = time.time()
    # kde = grid.best_estimator_
    bandwidth = max(1.06 * np.std(deg) * len(deg)**(-1/5), 0.05)
    kde = KernelDensity(kernel="gaussian", bandwidth=bandwidth).fit(deg)
    # if (not edges):
    #     kde = KernelDensity(kernel="gaussian", bandwidth=5.3).fit(deg)
    # if (edges):
    #     kde = KernelDensity(kernel="gaussian", bandwidth=0.2).fit(deg)
    try:
        print(deg_plot[0][0])
    except IndexError:
        deg_plot = np.array([[item] for item in deg_plot])
    log_dens = kde.score_samples(deg_plot)
    X = np.append(deg_plot[:, 0], deg_plot[:, 0][-1])
    X = np.insert(X, 0, X[0])
    Y = np.append(np.exp(log_dens), 0)
    Y = np.insert(Y, 0, 0)
    complete = ColumnDataSource(data=dict(x=X, y=Y))
    before = ColumnDataSource(data=dict(x=[], y=[]))
    middle = ColumnDataSource(data=dict(x=X, y=Y))
    after = ColumnDataSource(data=dict(x=[], y=[]))

    if (not edges):

        type_dependent1 = "let p = document.getElementById('between-{}-degree')".format(dir) + """
                if(!p){
                p = document.createElement("p")
                """ + 'p.id = "between-{}-degree"'.format(dir) + """
                document.getElementsByClassName("bk-root")[0].appendChild(p)
            }
            """
        type_dependent2 = """
        amount = result['nodes'];
        
             colored_amount = "<span style='color:red; font-weight:bold'>" + amount + "</span>"
                    if (amount < 600){
                        colored_amount = "<span style='color:orange; font-weight:bold'>" + amount + "</span>"
                    }
                    if (amount < 150){
                        colored_amount = "<span style='color:green; font-weight:bold'>" + amount + "</span>"
                    }

            """ + 'p.innerHTML = "Selected " + colored_amount + " nodes with {}-degree between " + Math.ceil(geometry.x0) + " and " + Math.floor(geometry.x1) + "."'.format(dir)

    else:
        type_dependent1 = """
            let p = document.getElementById('between-weight')

            if(!p){
                p = document.createElement("p")
                p.id = "between-weight"
                document.getElementsByClassName("bk-root")[0].appendChild(p)
            }
            """

        type_dependent2 = """
        amount = result['nodes'];
        amount_edges = result['edges'];
        
        colored_amount_edges = "<span style='color:red; font-weight:bold'>" + amount_edges + "</span>"
        if (amount_edges < 4000){
        colored_amount_edges = "<span style='color:orange; font-weight:bold'>" + amount_edges + "</span>"
        }
        if (amount_edges < 1500){
        colored_amount_edges = "<span style='color:green; font-weight:bold'>" + amount_edges + "</span>"
        }
        
            colored_amount = "<span style='color:red; font-weight:bold'>" + amount + "</span>"
        if (amount < 600){
        colored_amount = "<span style='color:orange; font-weight:bold'>" + amount + "</span>"
        }
        if (amount < 150){
        colored_amount = "<span style='color:green; font-weight:bold'>" + amount + "</span>"
        }

            p.innerHTML = colored_amount + " nodes remaining having a total of " + colored_amount_edges + " edges with weight between " + Math.ceil(geometry.x0*100)/100 + " and " + Math.floor(geometry.x1*100)/100 + "."
        """

    geometry_callback = CustomJS(args=dict(complete=complete, before=before, middle=middle, after=after), code="""
    let geometry = cb_data["geometry"]
    let Xs = complete.data.x
    let Ys = complete.data.y

    let bXs = before.data.x
    let bYs = before.data.y
    bXs = []
    bYs = []
    let mXs = middle.data.x
    let mYs = middle.data.y
    mXs = []
    mYs = []
    let aXs = after.data.x
    let aYs = after.data.y
    aXs = []
    aYs = []

    for (let i = 0; i < Xs.length; i++){
    // should use binary search
    let x = Xs[i]
    let y = Ys[i]
    if(x < geometry.x0){
    bXs.push(x)
    bYs.push(y)
    }
    else if (x > geometry.x1){
    aXs.push(x)
    aYs.push(y)
    }
    else {
    mXs.push(x)
    mYs.push(y)
    }
    }

    bXs.unshift(bXs[0])
    bYs.unshift(0)
    bXs.push(bXs[bXs.length-1])
    bYs[bYs.length] = 0
    mXs.unshift(mXs[0])
    mYs.unshift(0)
    mXs.push(mXs[mXs.length-1])
    mYs[mYs.length] = 0
    aXs.unshift(aXs[0])
    aYs.unshift(0)
    aXs.push(aXs[aXs.length-1])
    aYs[aYs.length] = 0

    before.data.x = bXs
    before.data.y = bYs
    middle.data.x = mXs
    middle.data.y = mYs
    after.data.x = aXs
    after.data.y = aYs

    before.change.emit()
    middle.change.emit()
    after.change.emit()
    var amount = 0
    let data = {
        left: geometry.x0,
        right: geometry.x1,
        file: window.location.pathname.substring(8),
        """ + "type: '{}', dir: '{}'".format(kind, dir) + """
    }
    $.post("/postmethod", data, function(result){ """ + type_dependent2 + "});" + type_dependent1)

    #p = figure(plot_width=300, plot_height=300, sizing_mode='scale_width')
    p = figure(plot_width=300, plot_height=300)
    select_tool = BoxSelectTool(dimensions="width", callback=geometry_callback)
    p.add_tools(select_tool)

    p.patch("x", "y", source=before, alpha=0.3, line_width=0)
    p.patch("x", "y", source=middle, alpha=1, line_width=0, color="#4C72B0")
    # p.patch("x", "y", source=middle, alpha=1, line_width=0, color="orange")
    p.patch("x", "y", source=after, alpha=0.3, line_width=0)

    if (not edges):
        p.xaxis.axis_label = "{}-degree".format(dir)
    else:
        p.xaxis.axis_label = "Edge weight"

    p.yaxis.visible = False
    p.grid.visible = False

    p.toolbar.active_drag = select_tool
    p.toolbar.autohide = True

    p.background_fill_color = None
    p.border_fill_color = None

    # print("KDE + plotting: {}-{}: ".format(dir, kind) + str(time.time()-begin))
    # print("Total {}-{}: ".format(dir, kind) + str(time.time()-big_bang))
    return p