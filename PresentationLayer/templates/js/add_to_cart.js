function addToCart(item_id) {
    let data = new FormData();
    data.append('item_id', item_id);
    data.append('quantity', document.getElementById("quantity_input").value);
    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200)
        {
            if (loadHTML.responseText === 'fail')
            {
                alert("add to cart fail");
            }
            else
            {
                if (loadHTML.responseText !== 'OK')
                {
                    if (getCookie('guest_hash') === '')
                    {
                        setCookie('guest_hash', loadHTML.responseText, 7);
                        location.reload();
                    }
                    else
                    {
                        location.reload();
                    }
                }
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/shopping_cart/add_item_shopping_cart/", true);
    loadHTML.send(data);
}