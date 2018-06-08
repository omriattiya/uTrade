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
    else
    {
        var reg = new RegExp('([0-9]*[.])?[0-9]+');
        if(!reg.test(document.getElementById("price").value))
        {
            alert("Field Price Must A Number");
            return;
        }
    }
    let item_kind = document.getElementById("kind").value;
    if (item_kind === 'prize')
    {
        if(document.getElementById("sale_hour").value == '')
        {
            alert('Field sale hour must not be empty');
            return;
        }
        if(document.getElementById("sale_minutes").value == '')
        {
            alert('Field sale minutes must not be empty');
            return;
        }
        var today = new Date();
        var toDecide = new Date(document.getElementById("sale_date").value);
        toDecide.setHours(parseInt(document.getElementById("sale_hour").value));
        toDecide.setMinutes(parseInt(document.getElementById("sale_minutes").value));
        if(toDecide.getTime() < today.getTime())
        {
            alert("Sale date must be bigger than today.");
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
    if (item_kind === 'prize')
    {
        data.append('sale_date', document.getElementById("sale_date").value);
        data.append('sale_hour', document.getElementById("sale_hour").value);
        data.append('sale_minutes', document.getElementById("sale_minutes").value);
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

function addDiscount(shop_name) {
    let data = new FormData();
    let kind = document.getElementById("kind").value;
    data.append('shop_name', shop_name);
    data.append('percent', document.getElementById("percent").value);
    data.append('duration', document.getElementById("duration").value.split('-'));
    data.append('kind', kind);

    switch (kind) {
        case "visible_item":
            data.append('item_id', document.getElementById("item_id").value);
            break;
        case "invisible_item":
            data.append('item_id', document.getElementById("item_id").value);
            data.append('code', document.getElementById("code").value);
            break;
        case "visible_category":
            data.append('category', document.getElementById("category").value);
            break;
        case "invisible_category":
            data.append('category', document.getElementById("category").value);
            data.append('code', document.getElementById("code").value);
            break;
    }

    let loadHTML = new XMLHttpRequest();
    loadHTML.shop_name = shop_name;
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'success') {
                alert("Discount Added Successfully");
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
    loadHTML.open("POST", "../app/shop/owner/add_discount/post", true);
    loadHTML.send(data);
}

function deleteDiscount(item_id, shop_name, from_date) {
    let data = new FormData();
    data.append('item_id', item_id);
    data.append('from_date', from_date);

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
    loadHTML.open("POST", "../app/shop/owner/delete_discount/", true);
    loadHTML.send(data);
}