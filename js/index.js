function appendHref(x) {
    var aList = document.getElementsByClassName("link");
    var i;
    for (i = 0; i < aList.length; i++) {
        aList[i].href += x;
    }
}

function keyPress() {
    appendHref("?UCCU=");
}

function loadParam() {
    var ghURL = new URL(window.location.href);
    var params = ghURL.searchParams;
    if (params.has('UCCU')) {
        appendHref("?UCCU");
    }
}