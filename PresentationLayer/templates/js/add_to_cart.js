function addToCart(item_id) {
    alert("5");
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
                if (getCookie('login_hash') === '')
                {
                    if (getCookie('guest_hash') === '')
                    {
                        alert("add to cart fail1");
                        setCookie('guest_hash', loadHTML.responseText, 7);
                        location.reload();
                    }
                    else
                    {
                        alert("add to cart fail2");
                        location.reload();
                    }
                }
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/shopping_cart/add_item_shopping_cart/", true);
    loadHTML.send(data);
}