function onClickOnSearch1() {
    if (document.getElementById("SearchForm1").value === '') {
        alert("No Search Value.");
    }
    else {
        url = '../app/search/item/?searchBy=name&name=' + document.getElementById("SearchForm1").value;
        let loadHTML = new XMLHttpRequest();
        loadHTML.url = url;
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else {
                    window.location.href = loadHTML.url
                }
            }
        };
        loadHTML.open("GET", url, true);
    }
}

function onClickOnSearch2() {
    if (document.getElementById("SearchForm2").value === '') {
        alert("No Search Value.");
    }
    else {
        url = '../app/search/item/?searchBy=category&category=' + document.getElementById("SearchForm2").value;
        let loadHTML = new XMLHttpRequest();
        loadHTML.url = url;
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else {
                    window.location.href = loadHTML.url
                }
            }
        };
        loadHTML.open("GET", url, true);
    }
}

function onClickOnSearch3() {
    if (document.getElementById("SearchForm3").value === '') {
        alert("No Search Value.");
    }
    else {
        url = '../app/search/item/?searchBy=keywords&keywords=' + document.getElementById("SearchForm3").value;
        let loadHTML = new XMLHttpRequest();
        loadHTML.url = url;
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else {
                    window.location.href = loadHTML.url
                }
            }
        };
        loadHTML.open("GET", url, true);
    }
}

function onClickOnSearch4() {
    if (document.getElementById("SearchForm4").value === '') {
        alert("No Search Value.");
    }
    else {
        let url = '../app/shop/?shop_name=' + document.getElementById("SearchForm4").value;
        let loadHTML = new XMLHttpRequest();
        loadHTML.url = url;
        loadHTML.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                if (loadHTML.responseText === 'fail') {
                    alert("Search Failed.")
                }
                else {
                    window.location.href = loadHTML.url
                }
            }
        };
        loadHTML.open("GET", url, true);
    }
}