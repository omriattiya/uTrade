$(document).ready(function () {
    $('#create-shop-form').submit(function () {
        return false;
    });

    $('#add-manager-form').submit(function () {
        return false;
    });
    $('#add-owner-form').submit(function () {
        return false;
    });
});

let currentlyWorkingOnShop = "";

function addManager() {
    let data = new FormData();
    let name = document.getElementById("manager-name-modal").value;
    data.append('shop_name', currentlyWorkingOnShop);
    data.append('target_id', name);
    data.append('add_item_permission', 0);
    data.append('remove_item_permission', 0);
    data.append('edit_item_permission', 0);
    data.append('reply_message_permission', 0);
    data.append('get_all_message_permission', 0);
    data.append('get_purchase_history_permission', 0);
    data.append('get_discount_permission', 0);


    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0,6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else {
                alert("Manager has been added!");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "../app/users/owner/add_manager/", true);
    loadHTML.send(data);
}

function removeManager(manager_name) {
    let data = new FormData();
    data.append('shop_name', currentlyWorkingOnShop);
    data.append('target_id', manager_name);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("Manager has been removed!");
                window.location.href = "../app/my/shops/"
            }
        }
    };
    loadHTML.open("POST", "../app/users/owner/remove_manager/", true);
    loadHTML.send(data);
}

function applyPermissions(manager_name) {
    let data = new FormData();
    data.append('shop_name', currentlyWorkingOnShop);
    data.append('target_id', manager_name);
    data.append('add_item_permission', +document.getElementById("AIP_" + manager_name).checked);
    data.append('remove_item_permission', +document.getElementById("RIP_" + manager_name).checked);
    data.append('edit_item_permission', +document.getElementById("EIP_" + manager_name).checked);
    data.append('reply_message_permission', +document.getElementById("RMP_" + manager_name).checked);
    data.append('get_all_message_permission', +document.getElementById("GAP_" + manager_name).checked);
    data.append('get_purchase_history_permission', +document.getElementById("GPHP_" + manager_name).checked);
    data.append('get_discount_permission', +document.getElementById("DP_" + manager_name).checked);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("Manager permissions has been updated!");
                window.location.href = "../app/my/shops/"
            }
        }
    };
    loadHTML.open("POST", "../app/users/owner/update_permissions/", true);
    loadHTML.send(data);
}


function createShop() {
    let data = new FormData();
    let name = document.getElementById("shop-name-modal").value;
    data.append('name', name);
    data.append('status', "Inactive");


    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0,6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else {
                alert("Your shop has been opened!");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "../app/shops/create_shop/", true);
    loadHTML.send(data);
}

/*function setNotification() {
    let current_status = document.getElementById(shop_name + "_notify").textContent;

    let data = new FormData();
    data.append('modify_notifications', current_status === 'On' ? 0 : 1);
    alert(current_status);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                //alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                window.location.href = "../app/my/shops/"
            }
        }
    };
    loadHTML.open("POST", "../app/users/owner/modify_notifications/", true);
    loadHTML.send(data);

}
*/
function setStatus(shop_name) {
    let current_status = document.getElementById(shop_name + "_status").textContent;

    let data = new FormData();
    data.append('shop_name', shop_name);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                window.location.href = "../app/my/shops/"
            }
        }
    };
    let route = current_status === 'Active' ?
        "close_shop/" : "re_open_shop/";
    loadHTML.open("POST", "../app/users/owner/" + route, true);
    loadHTML.send(data);

}

function shopModalOpened(shop_name) {
    currentlyWorkingOnShop = shop_name;

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else {
                document.getElementById('edit-managers-modal-body').innerHTML = loadHTML.responseText;
            }
        }
    };

    loadHTML.open("GET", "http://localhost:8000/app/my/shops/manager/?shop_name=" + shop_name, true);
    loadHTML.send();


}

function addOwnerOpened(shop_name) {
    currentlyWorkingOnShop = shop_name;
}

function addOwner() {
    let data = new FormData();
    let name = document.getElementById("owner-name-modal").value;
    data.append('shop_name', currentlyWorkingOnShop);
    data.append('target_id', name);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0,6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if(loadHTML.responseText.substring(0,7) === 'SUCCESS'){
                alert("Owner has been added!");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/users/owner/add_owner/", true);
    loadHTML.send(data);
}

function gotoMessages(shop_name) {
    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("No Permissions!")
            }
            else{
                window.location.href = "http://localhost:8000/app/shop/messages/?content=received&shop_name="+shop_name;
            }
        }
    };
    loadHTML.open("GET", "http://localhost:8000/app/shop/messages/?content=received&shop_name="+shop_name, true);
    loadHTML.send();
}

function getHistory(shop_name)
{
    document.write(5);
    var data = new FormData();
    data.append('shop_name', shop_name);
    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else {
                document.getElementById('show-history-appointings-body').innerHTML = loadHTML.responseText;
            }
        }
    };

    loadHTML.open("GET", "http://localhost:8000/app/my/historyappointings", true);
    loadHTML.send(data);
}