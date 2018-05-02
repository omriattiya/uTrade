$(document).ready(function () {
    $('#create-shop-form').submit(function () {
        createShop();
        return false;
    });

});


function createShop() {
    var data = new FormData();
    var name = document.getElementById("shop-name-modal").value;
    data.append('name', name);
    data.append('status',"Inactive");


    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                //alert("Failed")
            }
            else {
                alert("Your shop has been opened!");
                window.location.href = "http://localhost:8000/app/my/shops/"
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/shops/create_shop/", true);
    loadHTML.send(data);
}