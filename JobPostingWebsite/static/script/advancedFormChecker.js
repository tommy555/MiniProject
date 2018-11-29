var submitBtn = document.getElementById("submitBtn");
document.getElementById("advSearch").onclick = function() {
    var advancedSearch = document.getElementById("advSearchField");
    if (advancedSearch.style.display != "none"){
        advancedSearch.style.display = "none";
    }
    else {
        advancedSearch.style.display = "block"
    }
}

submitBtn.onclick = function() {
    var minsalary = document.getElementById("minSalary").value;
    var maxsalary = document.getElementById("maxSalary").value;
    var startTime = document.getElementById("startTime").value;
    var endTime = document.getElementById("endTime").value;

    var isSalaryValid = true;
    var isTimeValid = true;

    if(minsalary!="" && maxsalary != ""){
        if(minsalary > maxsalary){
            alert(minsalary)
            alert(maxsalary)
            alert("Minimum salary should not more than maximum salary");
            isSalaryValid = false;
        }
    }

    if(startTime != "" && endTime != ""){
        if(startTime > endTime){
            alert("End time should not earlier than start time!")
            isTimeValid = false;
        }
    }

    if (isSalaryValid && isTimeValid){
        document.getElementById("advancedForm").submit();
    }
}