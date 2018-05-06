function updateItem(item_id, shop_name) {
    let data = new FormData();
    data.append('item_id', item_id);
    data.append('item_quantity', document.getElementById("quantity").value);
    data.append('item_category', document.getElementById("category").value);
    data.append('item_keywords', document.getElementById("keywords").value);
    data.append('item_price', document.getElementById("price").value);
    data.append('item_url', document.getElementById("url").value);

    let loadHTML = new XMLHttpRequest();
    loadHTML.shop_name = shop_name;
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'no permission to edit item') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText === 'success') {
                alert("Item Updated Successfully");
                window.location.href = "../app/shop/?shop_name=" + loadHTML.shop_name;
            }
        }
    };
    loadHTML.open("POST", "../app/shop/owner/items/edit_item/", true);
    loadHTML.send(data);
}

function removeItem(item_id, shop_name) {
    let data = new FormData();
    data.append('item_id', item_id);

    let loadHTML = new XMLHttpRequest();
    loadHTML.shop_name = shop_name;
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed");
                window.location.reload(true)
            }
            else if (loadHTML.responseText === 'no permission to remove item') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText === 'success') {
                alert("Item Removed Successfully");
                window.location.href = "../app/shop/?shop_name=" + loadHTML.shop_name;
            }
        }
    };
    loadHTML.open("POST", "../app/shop/owner/items/remove_item/", true);
    loadHTML.send(data);
}

function addItem(shop_name) {
    let data = new FormData();

    data.append('shop_name', shop_name);
    data.append('item_name', document.getElementById("name").value);
    data.append('item_quantity', document.getElementById("quantity").value);
    data.append('item_category', document.getElementById("category").value);
    data.append('item_keywords', document.getElementById("keywords").value);
    data.append('item_price', document.getElementById("price").value);
    data.append('item_url', document.getElementById("url").value);
    data.append('item_kind', document.getElementById("kind").value);
    let loadHTML = new XMLHttpRequest();
    loadHTML.shop_name = shop_name;
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {

            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'no permission to add item') {
                alert(loadHTML.responseText);

            }
            else if (loadHTML.responseText === 'invalid values') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText === 'success') {
                alert("Item Added Successfully");
                window.location.href = "../app/shop/?shop_name=" + loadHTML.shop_name;

            }
        }
    }
    ;

    loadHTML.open("POST", "../app/shop/owner/items/add_item/post", true);
    loadHTML.send(data);
}

function addReview(shop_name) {
    let data = new FormData();
    data.append('shop_name', shop_name);
    data.append('description', document.getElementById("description").value);
    data.append('rank', document.getElementById("rank").value);

    let loadHTML = new XMLHttpRequest();
    loadHTML.shop_name = shop_name;
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {

            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("Review Added Successfully");
                window.location.href = "../app/shop/?shop_name=" + loadHTML.shop_name;

            }
        }
    }
    ;

    loadHTML.open("POST", "../app/shop/reviews/add_review/post", true);
    loadHTML.send(data);
}
