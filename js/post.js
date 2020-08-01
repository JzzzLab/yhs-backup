//if url parameter contains "UCCU", then display.
function getHref() {
    var ghURL = new URL(window.location.href);
    var params = ghURL.searchParams;
    if (params.has('UCCU')) {
        document.getElementById("main").style.display = "";
    }
}

//press any key to display.
function keyPress() {
    document.getElementById("main").style.display = "";
}

function removeHref() {
    var aList = document.getElementsByTagName("a");
    for (var i = 0; i < aList.length; i++) {
        aList[i].removeAttribute("href");
    }
}