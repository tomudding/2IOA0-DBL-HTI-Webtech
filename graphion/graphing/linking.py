"""
Author(s): Sam Baggen, Steven van den Broek
Created: 2019-06-03
Edited: 2019-06-16
"""

from holoviews.plotting.bokeh.callbacks import LinkCallback
from holoviews.plotting.links import Link
import param
import holoviews as hv

hv.extension('bokeh')

# Linking classes
class SelectMatrixToNodeLink(Link):
    _requires_target = True
    indices = param.List(default=[], doc="The list of indices to be passed to the callback")

class SelectMatrixToNodeCallback(LinkCallback):
    source_model = 'selected'
    source_handles = ['cds']
    on_source_changes = ['indices']

    target_model = 'cds'

    source_code = """// console.log("TRIGGERED MtN")
        // console.log(Array.from(target_cds.data['count']))
        //console.log(source_cds.data['index1'])
        if (target_cds.data["count"][0] < 1){
        let len = indices.length
        let new_indices = []
        for (let i = 0; i < source_selected.indices.length; i++){
            let index = source_selected.indices[i]
            j = len-1-(index%len)+Math.floor(index/(len))*(len)
            new_indices[i] = j
        }
        var inds = source_selected.indices
        var d = source_cds.data

        selected_data = []
        // selected_data['index1'] = []
        //selected_data['index2'] = []
        // selected_data['value'] = []
        // selected_data['zvalues'] = []

        for (var i = 0; i < inds.length; i++){
            if (!selected_data.includes(d['index1'][inds[i]])){
                selected_data.push(d['index1'][inds[i]]);
            }
            if (!selected_data.includes(d['index2'][inds[i]])){
                selected_data.push(d['index2'][inds[i]]);
            }
        }
        //    selected_data['index1'].push(d['index1'][inds[i]])
        //    selected_data['index2'].push(d['index2'][inds[i]])
        //    selected_data['value'].push(d['value'][inds[i]])
        //    selected_data['zvalues'].push(d['zvalues'][inds[i]])
        
        //console.log(selected_data)
        //console.log(target_cds.data)
        let nodelink_indices = []
        for (let i = 0; i < selected_data.length; i++){
            let index = target_cds.data.index.indexOf(selected_data[i]);
            nodelink_indices.push(index);
        }
        //console.log(target_cds.selected.indices)
        
        //var cds = target_glyph_renderer.edge_renderer.data_source.data
        //var startIndex = cds['start']
        //var endIndex = cds['end']

        //target_glyph_renderer.node_renderer.data_source.selected.indices = selected_data
        target_cds.data["count"][0] += 1;
        
        target_cds.selected.indices = nodelink_indices;
        }
        else{
            target_cds.data["count"][0]=0;
        }
    """

class SelectNodeToMatrixLink(Link):
    _requires_target = True
    
class SelectNodeToMatrixCallback(LinkCallback):
    source_model = 'selected'
    source_handles = ['cds']
    on_source_changes = ['indices']

    target_model = 'cds'

    source_code = """
        // console.log("TRIGGERED NtM")
        // console.log(Array.from(source_cds.data['count']));
        if(source_cds.data["count"][0] < 1){
        var nodeIndices = []
        //console.log(source_selected.indices)
        for (var i = 0; i < source_selected.indices.length; i++){
            nodeIndices.push(source_cds.data['index'][source_selected.indices[i]])
        }
        //console.log(nodeIndices)
        
        var matrixIndices = []
        for (var i = 0; i < nodeIndices.length; i++){
            for (var j = 0; j < target_cds.data['index2'].length; j++){
                if (target_cds.data['index2'][j] == nodeIndices[i]){
                    matrixIndices.push(j)
                }
            }
        }
        for (var i = 0; i < nodeIndices.length; i++){
            for (var j = 0; j < target_cds.data['index1'].length; j++){
                if (target_cds.data['index1'][j] == nodeIndices[i]){
                    matrixIndices.push(j)
                }
            }
        }
        //console.log(target_cds.data)
        //console.log(matrixIndices)
        
        source_cds.data["count"][0] += 1;
        
        target_cds.selected.indices = matrixIndices
        }
        else{
         source_cds.data["count"][0] = 0;
         }
    """


class SelectNodeToTableLink(Link):
    _requires_target = True


class SelectNodeToTableCallback(LinkCallback):
    source_model = 'selected'
    source_handles = ['cds']
    on_source_changes = ['indices']

    target_model = 'cds'

    source_code = """
        target_cds.selected.indices = source_selected.indices
    """

class SelectEdgeLink(Link):
    _requires_target = True
    
class SelectEdgeCallback(LinkCallback):
    source_model = 'selected'
    source_handles = ['cds']
    on_source_changes = ['indices']

    target_model = 'glyph_renderer'

    source_code = """
        console.log("TRIGGERED E")
        var cds = target_glyph_renderer.edge_renderer.data_source.data
        var startIndex = cds['start']
        var endIndex = cds['end']
        var indices = []
        var startIndices = []
        var endIndices = []

        for (var i = 0; i < source_selected.indices.length; i++){
            startIndices.push(source_cds.data['index2'][i])
            endIndices.push(source_cds.data['index1'][i])
        }

        for (var e = 0; e < startIndices.length; e++){
             var entry = startIndices[e]
            for (var i = 0; i < startIndex.length; i++){
                if (startIndex[i] == entry){
                    indices.push(i)
                }
            }
        }

        for (var e = 0; e < endIndices.length; e++){
             var entry = endIndices[e]
            for (var i = 0; i < endIndex.length; i++){
                if (endIndex[i] == entry){
                    indices.push(i)
                }
            }
        }

        if(indices.length == 0){
            target_glyph_renderer.edge_renderer.data_source.selected.indices = []
        } else {
            target_glyph_renderer.edge_renderer.data_source.selected.indices = indices
        }
    """

class SelectLink(Link):
    _requires_target = True

class SelectCallback(LinkCallback):
    names = []
    source_model = 'selected'
    # source_handles = ['cds']
    on_source_changes = ['indices']

    target_model = 'selected'

    source_code = "let len = {}".format(len(names)) + """
        let new_indices = []
        for (let i = 0; i < source_selected.indices.length; i++){
            let index = source_selected.indices[i]
            j = len-1-(index%len)+Math.floor(index/(len))*(len)
            new_indices[i] = j
        }
        target_selected.indices = new_indices
    """