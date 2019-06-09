/* 
Authors: Sam Baggen, Steven van den Broek, Tom Udding(?)
Created: Unkown...
Last Edited: 2019-06-06
*/

function darkMode(){
    if (document.getElementById('dark-mode-chk-box').checked) {
        document.getElementById('left-bar-shown').style.backgroundColor = '#424242';
        document.getElementById('right-bar-shown').style.backgroundColor = '#424242';
        changeColorToWhite();
    } else {
        document.getElementById('left-bar-shown').style.backgroundColor = '#FDFCF9';
        document.getElementById('right-bar-shown').style.backgroundColor = '#F7F7F7';
        changeColorToGrey();
    }
}

function changeColorToWhite(){
    var elements = document.getElementsByClassName('white-text');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = '#FFFFFF';
    }
}

function changeColorToGrey(){
    var elements = document.getElementsByClassName('white-text');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.color = '#747474';
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

function displayReordering(id){
    $.post("/switch-ordering", {to: id});
}

function displayMetric(id){
    $.post("/switch-metric", {to: id});
}

function displayPalette(id){
    $.post("/switch-palette", {to: id});
}