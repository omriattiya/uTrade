var openedItem = "";
var openedShop = "";


$(document).ready(function () {
    $('#review-shop-form').submit(function () {
        return false;
    });

    $('#review-item-form').submit(function () {
        return false;
    });
    $('#report-item-form').submit(function () {
        return false;
    });
});

function reviewShop() {
    if (!checkRank(Number(document.getElementById('shop-rank-modal').value))) {
        return;
    }

    var data = new FormData();
    data.append('shop_name', openedShop);
    data.append('description', document.getElementById('shop-review-content-modal').value);
    data.append('rank', document.getElementById('shop-rank-modal').value);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'has reviews') {
                alert('You have already reviewed this shop');
                return;
            }
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("Review has been added!");
                location.reload()
            }
            else {
                alert(loadHTML.responseText);
                window.location.href = "../app/home";
            }
        }
    };
    loadHTML.open("POST", "../app/shops/add_review_on_shop/", true);
    loadHTML.send(data);
}

function reviewItem() {
    if (isNaN(document.getElementById('message-to-modal').value)) {
        alert("Review rank must be a number.");
        return;
    }
    if (!checkRank(Number(document.getElementById('message-to-modal').value))) {
        return;
    }
    if (document.getElementById('message-content-modal').value == '') {
        alert("Message content must not be empty.");
        return;
    }
    var data = new FormData();
    data.append('item_id', openedItem);
    data.append('description', document.getElementById('message-content-modal').value);
    data.append('rank', document.getElementById('message-to-modal').value);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'has reviews') {
                alert('You have already reviewed this item');
                return;
            }
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("Review has been added!");
                location.reload()
            }
            else {
                alert(loadHTML.responseText);
                window.location.href = "../app/home";
            }
        }
    };
    loadHTML.open("POST", "../app/items/add_review_on_item/", true);
    loadHTML.send(data);
}

function checkRank(rank) {
    if (rank < 1 || rank > 10) {
        alert('Rank must be between 1 to 10');
        return false;
    }
    return true;
}

function reportItem() {
    var data = new FormData();
    data.append('to', 'System');
    data.append('content', document.getElementById('report-content-modal').value);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("Reported successfully!");
                location.reload()
            }
            else {
                alert(loadHTML.responseText);
                window.location.href = "../app/home";
            }
        }
    };
    loadHTML.open("POST", "../app/messages/send_message/", true);
    loadHTML.send(data);
}