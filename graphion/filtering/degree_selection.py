#%%
from sklearn.neighbors import KernelDensity
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import BoxSelectTool, Circle, CustomJS, ColumnDataSource
import pandas
from pandas import read_hdf

def generate_selection(file, kind="degree"):
    df = read_hdf(file)
    names = df.columns.tolist()

    ### BASIC DEGREE COUNTING
    deg = []

    N = len(names)
    for name in names:
        deg.append([df[name][df[name] > 0].count()])

    deg_plot = np.linspace(-max(deg)[0]/30, max(deg)+max(deg)[0]/30, 1000)

    kde = KernelDensity(kernel="gaussian", bandwidth=1).fit(deg)
    log_dens = kde.score_samples(deg_plot)
    X = np.append(deg_plot[:, 0], deg_plot[:, 0][-1])
    Y = np.append(np.exp(log_dens), 0)
    complete = ColumnDataSource(data=dict(x=X, y=Y))
    before = ColumnDataSource(data=dict(x=[], y=[]))
    middle = ColumnDataSource(data=dict(x=X, y=Y))
    after = ColumnDataSource(data=dict(x=[], y=[]))

    geometry_callback = CustomJS(args=dict(complete=complete, before=before, middle=middle, after=after, degrees=[item for sublist in deg for item in sublist]), code="""
    let p = document.getElementById('between')
    let geometry = cb_data["geometry"]
    
    if(!p){
    p = document.createElement("p")
    p.id = "between"
    document.getElementsByClassName("bk-root")[0].appendChild(p)
    }
    
    
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
    
    bYs[0] = 0
    bYs[bYs.length-1] = 0
    mYs[0] = 0
    mYs[mYs.length-1] = 0
    aYs[0] = 0
    aYs[aYs.length-1] = 0
    
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
    
    colored_amount = "<span style='color:red'>" + amount + "</span>"
    if (amount < 600){
    colored_amount = "<span style='color:orange'>" + amount + "</span>"
    }
    if (amount < 150){
    colored_amount = "<span style='color:green'>" + amount + "</span>"
    }
    
    p.innerHTML = "Selected " + colored_amount + " nodes with degree between " + Math.ceil(geometry.x0) + " and " + Math.floor(geometry.x1)
    """)

    p = figure(plot_width=700, plot_height=700)

    select_tool = BoxSelectTool(dimensions="width", callback=geometry_callback)
    p.add_tools(select_tool)

    p.patch("x", "y", source=before, alpha=0.3, line_width=0)
    p.patch("x", "y", source=middle, alpha=1, line_width=0, color="orange")
    p.patch("x", "y", source=after, alpha=0.3, line_width=0)

    p.xaxis.axis_label = "Degree"
    p.yaxis.visible = False
    p.grid.visible = False

    p.toolbar.active_drag = select_tool
    p.toolbar.autohide = True

    return p