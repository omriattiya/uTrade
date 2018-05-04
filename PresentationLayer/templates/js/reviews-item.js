$(document).ready(function () {
    $('#create-shop-form').submit(function () {
        return false;
    });

    $('#add-review-form').submit(function () {
        return false;
    });
});

function addReviewOnItem(item_id, username) {
    var data = new FormData();
    var rank = document.getElementById("rank-modal").value;
    var description = document.getElementById("description-modal").value;
    data.append('writer_name', username);
    data.append('item_id', item_id);
    data.append('rank', rank);
    data.append('description', description);


    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (username = "guest"){
                alert("Failed: Guest can't add a review")
            }
            else {
                alert("Review added!");
                window.location.href = "http://localhost:8000/app/item/reviews/"
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/users/owner/add_manager/", true);
    loadHTML.send(data);
}
