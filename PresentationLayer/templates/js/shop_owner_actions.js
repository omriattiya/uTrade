function updateItem(item_id) {
    let data = new FormData();
    data.append('item_id', item_id);
    data.append('item_quantity', document.getElementById("quantity").value);
    data.append('item_category', document.getElementById("category").value);
    data.append('item_keywords', document.getElementById("keywords").value);
    data.append('item_price', document.getElementById("price").value);
    data.append('item_url', document.getElementById("url").value);

    let loadHTML = new XMLHttpRequest();
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
                window.location.reload(true)
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/shop/owner/items/edit_item/", true);
    loadHTML.send(data);
}

function removeItem(item_id) {
    let data = new FormData();
    data.append('item_id', item_id);

    let loadHTML = new XMLHttpRequest();
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
                window.location.reload(true)
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/shop/owner/items/remove_item/", true);
    loadHTML.send(data);
}
