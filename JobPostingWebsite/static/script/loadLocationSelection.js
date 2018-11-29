// var
var countries = ["Malaysia", "Singapore", "Indonesia", "Thailand", "China", ""];
var stateMY = [
    "Johor", "Kedah", "Kelantan", "Malacca", "Sembilan", "Pahang", "Perak", "Perlis", "Penang", "Sabah", 
    "Sarawak", "Selangor", "Terengganu", ""
];

var countriesSelect = document.getElementById("countrySelect");
var stateSelect = document.getElementById("stateSelect");

// function

function getCustomOptionsNode(value, txt) {
    var options = document.createElement("OPTION");
    options.setAttribute("value", value);
    var text = document.createTextNode(txt);
    options.appendChild(text);

    return options;
}
function clearChildsNode(parentNode) {
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}

function setStateMY() {
    clearChildsNode(document.getElementById("stateSelect"))
    for (var i = 0; i < stateMY.length; i++){
        document.getElementById("stateSelect").appendChild(getCustomOptionsNode(stateMY[i], stateMY[i]));
    }

    document.getElementById("stateSelect").value = "";
}

function hideStateSelect() {
    document.getElementById("labelState").style.display = "none";
    document.getElementById("stateSelect").style.display = "none";
}

function showStateSelect() {
    document.getElementById("labelState").style.display = "inline-block";
    document.getElementById("stateSelect").style.display = "inline-block";
}

// main process
// set default
// clean all
clearChildsNode(document.getElementById("countrySelect"));
clearChildsNode(document.getElementById("stateSelect"));

// set countries
for (var i = 0; i < countries.length; i++){
    document.getElementById("countrySelect").appendChild(getCustomOptionsNode(countries[i], countries[i]));
}

// set default state- MY
setStateMY();

// if user change country
countriesSelect.onclick = function() {
    // countries[0] = Malaysia
    if (countriesSelect.value == countries[0]) {
        setStateMY();
        showStateSelect();
        document.getElementById("state").value = null;
    }
    else {
        hideStateSelect();
    }
    document.getElementById("country").value = document.getElementById("countrySelect").value
}

document.getElementById("stateSelect").onclick = function() {
    document.getElementById("state").value = document.getElementById("stateSelect").value
}

// set company location default
// set location default
var companyCountry = document.getElementById("company_country").value;
var companyState = document.getElementById("company_state").value;

var countrySelectOptions = document.getElementById("countrySelect").options;
for (var i=0; i<countrySelectOptions.length; i++) {
    if (countrySelectOptions[i].text == companyCountry){
        document.getElementById("countrySelect").value = countrySelectOptions[i].text;
        document.getElementById("countrySelect").selectedIndex = countrySelectOptions[i].index;
    }
}

if (companyCountry == "Malaysia"){
    var stateSelectOptions = document.getElementById("stateSelect").options;
    for (var i=0; i<countrySelectOptions.length; i++) {
        if (stateSelectOptions[i].text == companyState){
            document.getElementById("stateSelect").value = stateSelectOptions[i].text;
            document.getElementById("stateSelect").selectedIndex = stateSelectOptions[i].index;
        }
    }
}
else {
    document.getElementById("labelState").style.display = "none";
    document.getElementById("stateSelect").style.display = "none";
}