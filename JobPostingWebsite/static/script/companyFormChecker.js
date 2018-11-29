var submitBtn = document.getElementById("submitForm");

submitBtn.onclick = function() {
    var contact = document.getElementById("contact").value;

    // check contact format
    if(!isNumber(contact)){
        alert("Incorrect contact format, your contact should contain only number not any alphabet or character");
    }
    else{
        if (contact.length < 9 || contact.length > 11){
            if (contact.length < 9){
                alert("Incorrect contact format, your contact should not less than 9 numbers");
            }
            else if (contact.length > 11){
                alert("Incorrect contact format, your contact should not more than 10 or 11 numbers");
            }
        }
        else{
            document.getElementById("submitForm").type = "submit";
            document.getElementById("submitForm").click();
        }
    }
}

function isNumber(str) {
    if (isNaN(str) || str < 0){return false;}
    else{return true;}
}