/*
Authors: Sam Baggen, Steven van den Broek, Tom Udding
Created: Unkown... (sometime in May probably)
Last Edited: 2019-06-20
*/

var currentColor = 'rgb(49, 137, 255)'

function darkMode(){
    if (document.getElementById('dark-mode-chk-box').checked) {
        
        var elements = document.getElementsByClassName('slider');
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.backgroundColor = currentColor;
        }

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
        var elements = document.getElementsByClassName('slider');
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.backgroundColor = '#ccc';
        }

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

function changeLogoColor(id) {
    if (id == 'kgy') {
        document.getElementById('graphion-logo').style.color = '#22980C';
        currentColor = '#22980C';
    } else if (id == 'kbc') {
        document.getElementById('graphion-logo').style.color = 'rgb(49, 137, 255)';
        currentColor = 'rgb(49, 137, 255)';
    } else if (id == 'bgy') {
        document.getElementById('graphion-logo').style.color = '#D1EE1E';
        currentColor = '#D1EE1E';
    } else if (id == 'bmw') {
        document.getElementById('graphion-logo').style.color = '#D526FF';
        currentColor = '#D526FF';
    } else if (id == 'bmy') {
        document.getElementById('graphion-logo').style.color = '#898678';
        currentColor = '#898678';
    } else if (id == 'cividis') {
        document.getElementById('graphion-logo').style.color = '#FF366B';
        currentColor = '#FF366B';
    } else if (id == 'dimgray') {
        document.getElementById('graphion-logo').style.color = '#909498';
        currentColor = '#909498';
    } else if (id == 'fire') {
        document.getElementById('graphion-logo').style.color = '#FA3B00';
        currentColor = '#FA3B00';
    } else if (id == 'inferno') {
        document.getElementById('graphion-logo').style.color = '#A42C60';
        currentColor = '#A42C60';
    } else if (id == 'viridis') {
        document.getElementById('graphion-logo').style.color = '#1E9D88';
        currentColor = '#1E9D88';
    }
    darkMode();
    updateDiagramColor();
}

function updateDiagramColor() {

    var elements1 = document.getElementsByClassName('icon-selected');
    for (var i = 0; i < elements1.length; i++) {
        elements1[i].style.backgroundColor = currentColor;
    }
/*
    document.getElementById(selectedDiagram).style.backgroundColor = currentColor;
*/
    var elements = document.getElementsByClassName('icon');
    for (var i = 0; i < elements.length; i++) {
        elements[i].style.backgroundColor = 'rgba(0,0,0,0)';
    }
}
/*
function updateMatrixColor() {
    if (matrixState == 1) {
        document.getElementById('')
    }
}
*/
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


        $.post("/switch-nodelink", {to: id}, function(){removeRightToolbar();});
    }
    updateDiagramColor();
}

function displayMatrix() {
    var targetNode = document.getElementById("matrix");
    var currentState = (targetNode.className == "icon-selected") ? true : false;

    var screen1 = document.querySelector(".screen-1");
    var screen2 = document.querySelector(".screen-2");

    if (currentState == true) {
        targetNode.className = "icon";
        targetNode.style.backgroundColor = 'rgba(0,0,0,0)';
        screen2.style.display = "none";
        screen1.style.left = "calc(25% - 5px)";
    } else {
        targetNode.className = "icon-selected";
        targetNode.style.backgroundColor = currentColor;
        screen2.style.display = "block";
        screen1.style.left = "5px";
    }
}

function fixMatrix() {
    var targetNode = document.getElementById("matrix");
    var currentState = (targetNode.className == "icon-selected") ? true : false;
    
    var screen1 = document.querySelector(".screen-1");
    var screen2 = document.querySelector(".screen-2");

    if (currentState == true) {
        targetNode.className = "icon-selected";
        screen2.style.display = "block";
        screen1.style.left = "5px";
    } else {
        targetNode.className = "icon";
        screen2.style.display = "none";
        screen1.style.left = "calc(25% - 5px)";
    }
}

function displayReordering(id){
    $.post("/switch-ordering", {to: id}, function(){removeRightToolbar()});
}

function displayMetric(id){
    $.post("/switch-metric", {to: id}, function(){removeRightToolbar()});
}

function displayPalette(id){
    $.post("/switch-palette", {to: id}, function(){removeRightToolbar()});
}

function displayNodeSize(id){
    $.post("/switch-size", {to: id}, function(){removeRightToolbar()});
}

function displayNodeColor(id){
    $.post("/switch-color", {to: id}, function(){removeRightToolbar()});
}

function removeRightToolbar(){
    // const trash = document.getElementsByClassName("trash")[0];
    // trash.classList.add("invisible");
    document.getElementsByClassName("right-bar-shown")[0].classList.add("invisible");
    document.getElementsByClassName("right-bar-hidden")[0].classList.add("invisible");
}