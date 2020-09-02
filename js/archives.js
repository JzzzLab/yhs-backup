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
    var urlAch = `https://jzzzlab.github.io/yhs-backup/archives/${today}/index.html`;
    var urlSrc = `https://jzzzlab.github.io/yhs-backup/src/${today}/index.html`;

    fetch(urlAch).then(
        function(response) {
            if(response.status == 200){     //在archives
                window.open(urlAch);
            }
            else {
                fetch(urlSrc).then(
                    function(response) {
                        if(response.status == 200){     //在src
                            window.open(urlSrc)
                        }
                        else{       //都不在
                            window.alert("日期輸入錯誤或無當天資料");
                        }
                    }
                )
            }
        }
    )

}

function redirect() {
    var dd = String(document.getElementById("day").value).padStart(2, '0');
    var mm = String(document.getElementById("month").value).padStart(2, '0');
    var yyy = document.getElementById("year").value;
    var today = yyy + "/" + mm + "/" + dd;
    checkURL(today);
}