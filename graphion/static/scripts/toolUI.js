/*
Authors: Sam Baggen, Steven van den Broek, Tom Udding
Created: Unkown...
Last Edited: 2019-06-17
*/

function darkMode(){
    if (document.getElementById('dark-mode-chk-box').checked) {
        document.getElementById('left-bar-shown').style.backgroundColor = 'rgb(66,66,66)';
        document.getElementById('left-bar-hidden').style.backgroundColor = 'rgb(66,66,66)';
        document.getElementById('right-bar-shown').style.backgroundColor = 'rgb(66,66,66)';
        document.getElementById('right-bar-hidden').style.backgroundColor = 'rgb(66,66,66)';
        document.getElementById('body').style.backgroundColor = '#7E8288';
        document.getElementById('after-loading').style.backgroundColor = '#7E8288';

        /*Recolor the text*/
        changeColorToWhite();
        /*
        Change color of the icons
        */
        document.getElementById('radial').src="/static/images/icons/icon-radial-diagram.svg";
        document.getElementById('force').src="/static/images/icons/icon-forcedirected-diagram.svg";
        document.getElementById('hierarchical').src="/static/images/icons/icon-hierarchical-diagram.svg";
        document.getElementById('3d').src="/static/images/icons/icon-3d-diagram.svg";
        document.getElementById('matrix').src="/static/images/icons/icon-matrix.svg";

        /*changeIconSelectedBackgroundColorToGrey();*/

    } else {
        document.getElementById('left-bar-shown').style.backgroundColor = '#F7F7F7';
        document.getElementById('right-bar-shown').style.backgroundColor = '#F7F7F7';
        document.getElementById('left-bar-hidden').style.backgroundColor = '#F7F7F7';
        document.getElementById('right-bar-hidden').style.backgroundColor = '#F7F7F7';
        document.getElementById('body').style.backgroundColor = '#EAEAEA';
        document.getElementById('after-loading').style.backgroundColor = '#EAEAEA';

        /*Recolor the text*/
        changeColorToGrey();
        /*
        Change color of the icons
        */
        document.getElementById('radial').src="/static/images/icons/icon-radial-diagram-black.svg";
        document.getElementById('force').src="/static/images/icons/icon-forcedirected-diagram-black.svg";
        document.getElementById('hierarchical').src="/static/images/icons/icon-hierarchical-diagram-black.svg";
        document.getElementById('3d').src="/static/images/icons/icon-3d-diagram-black.svg";
        document.getElementById('matrix').src="/static/images/icons/icon-matrix-black.svg";

        /*changeIconSelectedBackgroundColorToBlue()*/
    }
}

/*
function changeIconSelectedBackgroundColorToBlue(){
    var iconSelected = document.getElementsByClassName('icon-selected');
    for (var i = 0; i < iconSelected.length; i++) {
        iconSelected[i].style.backgroundColor = 'rgb(49, 137, 255)';
    }
}

function changeIconSelectedBackgroundColorToGrey(){
    var iconSelected = document.getElementsByClassName('icon-selected');
    for (var i = 0; i < iconSelected.length; i++) {
        iconSelected[i].style.backgroundColor = 'rgb(100,100,100)';
    }
}
*/

function changeColorToWhite(){
    var elements = document.getElementsByClassName('white-text');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = '#FFFFFF';
    }
}

function changeColorToGrey(){
    var elements = document.getElementsByClassName('white-text');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = 'rgb(66,66,66)';
    }
}

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

        $.post("/switch-nodelink", {to: id});

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

function displayMatrix() {
    var targetNode = document.getElementById("matrix");
    var currentState = (targetNode.className == "icon-selected") ? true : false;

    var screen1 = document.querySelector(".screen-1");
    var screen2 = document.querySelector(".screen-2");

    if (currentState == true) {
        targetNode.className = "icon";
        screen2.style.display = "none";
    } else {
        targetNode.className = "icon-selected";
        screen2.style.display = "block";
    }
}

function displayReordering(id){
    $.post("/switch-ordering", {to: id});
}

function displayMetric(id){
    $.post("/switch-metric", {to: id});
}

function displayPalette(id){
    $.post("/switch-palette", {to: id});
}

function displayNodeSize(id){
    $.post("/switch-size", {to: id});
}

function displayNodeColor(id){
    $.post("/switch-color", {to: id});
}