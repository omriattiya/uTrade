function onClickOnSearch1() {
    if (document.getElementById("SearchForm1").value == '') {
        alert("No Search Value.");
    }
    else {
        var url = 'http://localhost:8000/app/search/item/?searchBy=name&name=' + document.getElementById("SearchForm1").value;
        var loadHTML = new XMLHttpRequest();
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else if (loadHTML.responseText === 'FAIL: suspect sql injection')
                    alert(loadHTML.responseText);
                else {
                    window.location.href = url
                }
            }
        };
        loadHTML.open("GET", url, true);
        loadHTML.send(null);
    }
}

function onClickOnSearch2() {
    if (document.getElementById("SearchForm2").value == '') {
        alert("No Search Value.");
    }
    else {
        var url = 'http://localhost:8000/app/search/item/?searchBy=category&category=' + document.getElementById("SearchForm2").value;
        var loadHTML = new XMLHttpRequest();
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else if (loadHTML.responseText === 'FAIL: suspect sql injection')
                    alert(loadHTML.responseText);
                else {
                    window.location.href = url
                }
            }
        };
        loadHTML.open("GET", url, true);
        loadHTML.send(null);
    }
}

function onClickOnSearch3() {
    if (document.getElementById("SearchForm3").value == '') {
        alert("No Search Value.");
    }
    else {
        var url = 'http://localhost:8000/app/search/item/?searchBy=keywords&keywords=' + document.getElementById("SearchForm3").value;
        var loadHTML = new XMLHttpRequest();
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else if (loadHTML.responseText === 'FAIL: suspect sql injection')
                    alert(loadHTML.responseText);
                else {
                    window.location.href = url
                }
            }
        };
        loadHTML.open("GET", url, true);
        loadHTML.send(null);
    }
}

function onClickOnSearch4() {

    if (document.getElementById("SearchForm4").value == '') {
        alert("No Search Value.");
    }
    else {
        var url = 'http://localhost:8000/app/shop/?shop_name=' + document.getElementById("SearchForm4").value;
        var loadHTML = new XMLHttpRequest();
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else if (loadHTML.responseText === 'FAIL: suspect sql injection')
                    alert(loadHTML.responseText);
                else {
                    window.location.href = url
                }
            }
        };
        loadHTML.open("GET", url, true);
        loadHTML.send(null);
    }
}