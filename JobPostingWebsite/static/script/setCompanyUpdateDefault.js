// set company type default
var companyType = document.getElementById("company_type").value;

var typeSelectOptions = document.getElementById("companyType").options;
for (var i=0; i<typeSelectOptions.length; i++) {
    if (typeSelectOptions[i].text == companyType){
        document.getElementById("companyType").value = typeSelectOptions[i].text;
        document.getElementById("companyType").selectedIndex = typeSelectOptions[i].index;
    }
}