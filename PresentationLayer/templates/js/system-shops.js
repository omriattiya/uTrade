function closeShop(shop_name) {
    var data = new FormData();
    data.append('shop_name', shop_name);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("Shop has been closed.");
                location.reload()
            }
        }
    };
    loadHTML.open("POST", "../app/shops/close_shop_permanently/", true);
    loadHTML.send(data);
}

function showOwners(shop_name) {
    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else {
                alert(loadHTML.responseText);
            }
        }
    };
    loadHTML.open("GET", "../app/shop/get_owners/?shop_name=" + shop_name, true);
    loadHTML.send();
}

function showManagers(shop_name) {
    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else {
                alert(loadHTML.responseText);
            }
        }
    };
    loadHTML.open("GET", "../app/shop/get_managers/?shop_name=" + shop_name, true);
    loadHTML.send();
}

