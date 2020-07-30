//if url parameter contains "UCCU", then display.
function getHref() {
    var ghURL = new URL(window.location.href);
    var params = ghURL.searchParams;

    //只要存在"UCCU"參數就好
    //post.html?UCCU
    //post.html?UCCU=
    //post.html?UCCU=1
    //post.html?UCCU=true
    if (params.has('UCCU')) {
        document.getElementById("main").style.display = "";
    }
}

//press any key to display.
function keyPress() {
    document.getElementById("main").style.display = "";
}