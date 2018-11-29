var addBtn = document.getElementById("addSkill");
var clearBtn = document.getElementById("clearSkill");

addBtn.style.display = "inline-block";
clearBtn.style.display = "inline-block";

addBtn.onclick = function() {
    select = document.getElementById("skillRequired");
    option = select.options;
    var selected = option[select.value-1].text;
    if (document.getElementById("skillText").value == "") {
        document.getElementById("skillText").value += selected;
    }
    else {
        document.getElementById("skillText").value += ", "+selected;
    }
}

clearBtn.onclick = function() {
    document.getElementById("skillText").value = "";
}

