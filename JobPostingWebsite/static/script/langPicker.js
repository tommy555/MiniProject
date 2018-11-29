var engLang = document.getElementById("engLang");
var mandLang = document.getElementById("mandLang");
var malayLang = document.getElementById("malayLang");

engLang.onclick = function() {
    checkLang();
}

mandLang.onclick = function() {
    checkLang();
}

malayLang.onclick = function() {
    checkLang();
}

var textField = document.getElementById("spokenLang");
var defaultText = textField.value;

if (defaultText.indexOf("English") != -1){
    var engChecked = document.getElementById("engLang").checked = true;
}

if (defaultText.indexOf("Mandarin") != -1){
    var mandChecked = document.getElementById("mandLang").checked = true;
}

if (defaultText.indexOf("Malay") != -1){
    var malayChecked = document.getElementById("malayLang").checked = true;
}

textField.style.display = "none";

function checkLang(){
    var txt = "";
    var engChecked = document.getElementById("engLang").checked;
    var mandChecked = document.getElementById("mandLang").checked;
    var malayChecked = document.getElementById("malayLang").checked;

    if(engChecked){
        txt += "English "
    }

    if(mandChecked){
        txt += "Mandarin "
    }

    if(malayChecked){
        txt += "Malay"
    }

    document.getElementById("spokenLang").value = txt;
}