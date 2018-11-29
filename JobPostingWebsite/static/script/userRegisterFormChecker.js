var submitBtn = document.getElementById("userSubmit");

submitBtn.onclick = function() {
    var nric = document.getElementById("nric").value;
    var contact = document.getElementById("contact").value;

    // check nric format
    if(!isNumber(nric)){
        alert("Incorrect NRIC format, your NRIC should contain only number not any alphabet or character")
    }
    else{
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
                if (document.getElementById("skillText").value == "" || document.getElementById("skillText").value == null){
                    alert("You have to add at least 1 skills");
                }
                else {
                    document.getElementById("userSubmit").type = "submit";
                    document.getElementById("userSubmit").click();
                }
            }
        }
    }
}

function isNumber(str) {
    if (isNaN(str) || str < 0){return false;}
    else{return true;}
}