"""
Author(s): Steven van den Broek
Created: 2019-05-18
Edited: 2019-05-20
"""
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import BoxSelectTool, Circle, CustomJS, ColumnDataSource
import pandas
from pandas import read_hdf
import random

def generate_selection(file, kind="degree", dir="in"):
    if (kind == "degree"):
        edges=False
    else:
        edges=True

    df = read_hdf(file)
    names = df.columns.tolist()

    ### BASIC DEGREE COUNTING
    if (not edges):
        deg_all = []
        if (dir == "in"):
            for name in names:
                deg_all.append([df[name][df[name] > 0].count()])
        if (dir == "out"):
            for name in names:
                deg_all.append([df.loc[name, : ][df.loc[name, : ] > 0].count()])

    else:
        deg_all = [[item] for sublist in df.values for item in sublist]

    if (len(deg_all) > 1000):
        deg = random.sample(deg_all, 1000)
        deg.append(max(deg_all))
        deg.append(min(deg_all))
    else:
        deg = deg_all
    deg_plot = np.linspace(-max(deg)[0] / 30, max(deg) + max(deg)[0] / 30, 1000)
    # Calculate 'pretty good' (since best takes a long time) bandwidth
    grid = GridSearchCV(KernelDensity(),
                        {'bandwidth': np.linspace(0.1, 10.0, 20)},
                        cv=5,
                        iid=False)  # 5-fold cross-validation
    grid.fit(deg)
    kde = grid.best_estimator_
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

        type_dependent = "let p = document.getElementById('between-{}-degree')".format(dir) + """
            if(!p){
                p = document.createElement("p")
                """ + 'p.id = "between-{}-degree"'.format(dir) + """
                document.getElementsByClassName("bk-root")[0].appendChild(p)
            }
            
            let colored_amount = "<span style='color:red; font-weight:bold'>" + amount + "</span>"
            if (amount < 600){
                colored_amount = "<span style='color:orange; font-weight:bold'>" + amount + "</span>"
            }
            if (amount < 150){
                colored_amount = "<span style='color:green; font-weight:bold'>" + amount + "</span>"
            }
            """ + 'p.innerHTML = "Selected " + colored_amount + " nodes with {}-degree between " + Math.ceil(geometry.x0) + " and " + Math.floor(geometry.x1) + "."'.format(dir)

    else:
        type_dependent = """
            let p = document.getElementById('between-weight')
            
            if(!p){
                p = document.createElement("p")
                p.id = "between-weight"
                document.getElementsByClassName("bk-root")[0].appendChild(p)
            }
            
            let colored_amount = "<span style='color:red; font-weight:bold'>" + amount + "</span>"
            if (amount < 4000){
                colored_amount = "<span style='color:orange; font-weight:bold'>" + amount + "</span>"
            }
            if (amount < 1500){
                colored_amount = "<span style='color:green; font-weight:bold'>" + amount + "</span>"
            }

            p.innerHTML = "Selected " + colored_amount + " edges with weight between " + Math.ceil(geometry.x0*100)/100 + " and " + Math.floor(geometry.x1*100)/100 + "."
        """

    geometry_callback = CustomJS(args=dict(complete=complete, before=before, middle=middle, after=after, degrees=[item for sublist in deg_all for item in sublist]), code="""   
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
    
    let amount = 0
    for (let i = 0; i < degrees.length; i++){
      if (degrees[i] >= geometry.x0 && degrees[i] <= geometry.x1){
        amount++;
      }
    }
    """ + type_dependent)

    p = figure(plot_width=700, plot_height=700)

    select_tool = BoxSelectTool(dimensions="width", callback=geometry_callback)
    p.add_tools(select_tool)

    p.patch("x", "y", source=before, alpha=0.3, line_width=0)
    p.patch("x", "y", source=middle, alpha=1, line_width=0, color="orange")
    p.patch("x", "y", source=after, alpha=0.3, line_width=0)

    if (not edges):
        p.xaxis.axis_label = "{}-degree".format(dir)
    else:
        p.xaxis.axis_label = "Edge weight"

    p.yaxis.visible = False
    p.grid.visible = False

    p.toolbar.active_drag = select_tool
    p.toolbar.autohide = True

    return p