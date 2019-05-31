function showLeftBar(){
    document.getElementById('left-bar-shown').hidden = false;
    document.getElementById('left-bar-hidden').hidden = true;
}

function hideLeftBar(){
    document.getElementById('left-bar-shown').hidden = true;
    document.getElementById('left-bar-hidden').hidden = false;
}

function showRightBar(){
    document.getElementById('right-bar-shown').hidden = false;
    document.getElementById('right-bar-hidden').hidden = true;
}

function hideRightBar(){
    document.getElementById('right-bar-shown').hidden = true;
    document.getElementById('right-bar-hidden').hidden = false;
}

let selectedDiagram = 'force';

function displayDiagram(id){
    if (selectedDiagram !== id){
        document.getElementById(selectedDiagram).className = 'icon';
        selectedDiagram = id;
        document.getElementById(selectedDiagram).className = 'icon-selected';
        if (id === 'radial'){
            // TODO switch to radial view
        } else if (id === 'force'){
            // TODO switch to force-directed view
        } else if (id === 'hierarchical'){
            // TODO switch to hierarchical view
        } else {
            // TODO switch to 3d view
        }
    }
}