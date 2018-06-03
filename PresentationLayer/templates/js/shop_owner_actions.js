function updateItem(item_id, shop_name)
{
    let data = new FormData();
    data.append('item_id', item_id);
    data.append('item_quantity', document.getElementById("quantity" + item_id.toString()).value);
    data.append('item_category', document.getElementById("category" + item_id.toString()).value);
    data.append('item_keywords', document.getElementById("keywords" + item_id.toString()).value);
    data.append('item_price', document.getElementById("price" + item_id.toString()).value);
    data.append('item_url', document.getElementById("url" + item_id.toString()).value);

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
    if(document.getElementById("name").value == '')
    {
        alert("Field Name Must Not Be Empty");
        return;
    }
    if(document.getElementById("quantity").value  == '')
    {
        alert("Field Quantity Must Not Be Empty");
        return;
    }
    if(document.getElementById("category").value  == '')
    {
        alert("Field Quantity Must Not Be Empty");
        return;
    }
    else
    {
        var re = new RegExp("^([a-zA-Z]{1,20})$");
        if(!re.test(document.getElementById("category").value ))
        {
            alert("Field Category Must Contain Only Letters");
            return;
        }
    }
    if(document.getElementById("price").value  == '')
    {
        alert("Field Price Must Not Be Empty");
        return;
    }
    let item_kind = document.getElementById("kind").value;
    if (item_kind === 'auction')
    {
        if(document.getElementById("sale_duration").value  == '')
        {
            alert("Field Sale Duration Must Not Be Empty");
            return;
        }
    }
    else if (item_kind === 'prize')
    {
        if(document.getElementById("sale_duration").value  == '')
        {
            alert("Field Sale Duration Must Not Be Empty");
            return;
        }
    }
    let data = new FormData();
    data.append('shop_name', shop_name);
    data.append('item_name', document.getElementById("name").value);
    data.append('item_quantity', document.getElementById("quantity").value);
    data.append('item_category', document.getElementById("category").value);
    data.append('item_keywords', document.getElementById("keywords").value);
    data.append('item_price', document.getElementById("price").value);
    data.append('item_url', document.getElementById("url").value);
    data.append('item_kind', item_kind);

    if (item_kind === 'auction')
    {
        data.append('item_auction_initial_price', document.getElementById("price").value);
        data.append('item_auction_sale_duration', document.getElementById("sale_duration").value);
    }
    else if (item_kind === 'prize')
    {
        data.append('item_prize_sale_duration', document.getElementById("sale_duration").value);
    }
    let loadHTML = new XMLHttpRequest();
    loadHTML.shop_name = shop_name;
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'success') {
                alert("Item Added Successfully");
                window.location.href = "../app/shop/?shop_name=" + loadHTML.shop_name;
            }
            else if (loadHTML.responseText === 'user not logged in' ||
                loadHTML.responseText === 'not owner or manager in this shop') {
                alert(loadHTML.responseText);
                window.location.href = "../app/home"
            }
            else alert(loadHTML.responseText);

        }
    };
    loadHTML.open("POST", "../app/shop/owner/items/add_item/post", true);
    loadHTML.send(data);
}