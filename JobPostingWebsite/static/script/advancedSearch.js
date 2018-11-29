document.getElementById("advSearch").onclick = function() {
    var advancedSearch = document.getElementById("advSearchField");
    if (advancedSearch.style.display != "none"){
        advancedSearch.style.display = "none";
    }
    else {
        advancedSearch.style.display = "block"
    }
}