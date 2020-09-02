function getToday() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyy = today.getFullYear() - 1911;

    document.getElementById("year").value = yyy;
    document.getElementById("month").value = mm;
    document.getElementById("day").value = dd;
}

function keyUpInput() {
    if (event.keyCode === 13)
        document.getElementById("redirect").click();
}

function checkURL(today) {
    //var urlSrc = "https://jzzzlab.github.io/yhs-backup/src/109/09/01/index.html";
    //var urlArc = "https://jzzzlab.github.io/yhs-backup/archives/109/08/05/index.html";
    //1.read status.json
    //2.if today is SRC
    var urlSrc = `https://jzzzlab.github.io/yhs-backup/src/${today}/index.html`;
    return urlSrc;
    //3.elif today is ARC
    //var urlArc = `https://jzzzlab.github.io/yhs-backup/archives/${today}/index.html`;
    //return urlArc;
    //4.else return
    //window.alert("日期輸入錯誤或無當天資料");
    //return '';
}

function redirect() {
    var dd = String(document.getElementById("day").value).padStart(2, '0');
    var mm = String(document.getElementById("month").value).padStart(2, '0');
    var yyy = document.getElementById("year").value;
    var today = yyy + "/" + mm + "/" + dd;
    var url = checkURL(today);
    window.alert(url);
}