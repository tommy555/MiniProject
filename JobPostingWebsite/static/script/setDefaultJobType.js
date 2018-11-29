// set job type default
var j = document.getElementById("jobType");
var jobType = j.value;
j.style.display = "none";
var typeSelectOptions = document.getElementById("job_type").options;
for (var i=0; i<typeSelectOptions.length; i++) {
    if (typeSelectOptions[i].text == jobType){
        document.getElementById("job_type").value = typeSelectOptions[i].text;
        document.getElementById("job_type").selectedIndex = typeSelectOptions[i].index;
    }
}