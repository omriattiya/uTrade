let item_currentlyOpenedPolicy;
let category_currentlyOpenedPolicy;
let global_currentlyOpenedPolicy;


function insertAtCursor(myField, myValue) {
    //IE support
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
    }
    //MOZILLA and others
    else if (myField.selectionStart || myField.selectionStart === '0') {
        let startPos = myField.selectionStart;
        let endPos = myField.selectionEnd;
        myField.value = myField.value.substring(0, startPos)
            + myValue
            + myField.value.substring(endPos, myField.value.length);
    } else {
        myField.value += myValue;
    }
}


/* Item Policies */
function item_qualifierChanged(id) {
    let currentQualifier = document.getElementById("item-select-qualifier" + id).value;
    document.getElementById("item-policy-quantity" + id).disabled = currentQualifier === "N";


    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'restrict');
    data.append('new_value', currentQualifier);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/item/update/", true);
    loadHTML.send(data);
}

function item_quantityChange(id) {
    let currentQuantity = document.getElementById("item-policy-quantity" + id).value;

    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'quantity');
    data.append('new_value', currentQuantity);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/item/update/", true);
    loadHTML.send(data);
}

function item_nameChanged(id) {
    let currentName = document.getElementById("item-name" + id).value;

    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'item_name');
    data.append('new_value', currentName);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/item/update/", true);
    loadHTML.send(data);
}


function item_addNewPolicy() {
    let data = new FormData();

    data.append('item_name', "");
    data.append('conditions', "");
    data.append('restrict', "N");
    data.append('quantity', "0");

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("new policy has been added");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/item/add/", true);
    loadHTML.send(data);
}

function item_logicOpened(id) {
    item_currentlyOpenedPolicy = id;

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else {
                document.getElementById("item-expressions-modal-body").innerHTML = loadHTML.responseText;
            }
        }
    };
    loadHTML.open("GET", "http://localhost:8000/app/system/policies/item/get/conditions/?policy_id=" + id, true);
    loadHTML.send();

}


function item_savePolicyChanges() {
    let data = new FormData();
    let conditions = document.getElementById("item-expressions-modal-body").value;
    data.append('policy_id', item_currentlyOpenedPolicy);
    data.append('field_name', 'conditions');
    data.append('new_value', conditions);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("Rules saved!");
                //window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/item/update/", true);
    loadHTML.send(data);
}


/* Category Policies */

function category_addNewPolicy() {
    let data = new FormData();

    data.append('category', "");
    data.append('conditions', "");
    data.append('restrict', "N");
    data.append('quantity', "0");

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("new policy has been added");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/category/add/", true);
    loadHTML.send(data);
}

function category_qualifierChanged(id) {
    let currentQualifier = document.getElementById("category-select-qualifier" + id).value;
    document.getElementById("category-policy-quantity" + id).disabled = currentQualifier === "N";


    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'restrict');
    data.append('new_value', currentQualifier);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/category/update/", true);
    loadHTML.send(data);
}

function category_quantityChange(id) {
    let currentQuantity = document.getElementById("category-policy-quantity" + id).value;

    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'quantity');
    data.append('new_value', currentQuantity);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/category/update/", true);
    loadHTML.send(data);
}

function category_nameChanged(id) {
    let currentName = document.getElementById("category-name" + id).value;

    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'category');
    data.append('new_value', currentName);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/category/update/", true);
    loadHTML.send(data);
}

function category_logicOpened(id) {
    category_currentlyOpenedPolicy = id;

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else {
                document.getElementById("category-expressions-modal-body").innerHTML = loadHTML.responseText;
            }
        }
    };
    loadHTML.open("GET", "http://localhost:8000/app/system/policies/category/get/conditions/?policy_id=" + id, true);
    loadHTML.send();
}

function category_savePolicyChanges() {
    let data = new FormData();
    let conditions = document.getElementById("category-expressions-modal-body").value;
    data.append('policy_id', category_currentlyOpenedPolicy);
    data.append('field_name', 'conditions');
    data.append('new_value', conditions);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("Rules saved!");
                //window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/category/update/", true);
    loadHTML.send(data);
}


/* Global Policies */

function global_addNewPolicy() {
    let data = new FormData();

    data.append('conditions', "");
    data.append('restrict', "N");
    data.append('quantity', "0");

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("new policy has been added");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/global/add/", true);
    loadHTML.send(data);
}

function global_qualifierChanged(id) {
    let currentQualifier = document.getElementById("global-select-qualifier" + id).value;
    document.getElementById("global-policy-quantity" + id).disabled = currentQualifier === "N";


    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'restrict');
    data.append('new_value', currentQualifier);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/global/update/", true);
    loadHTML.send(data);
}

function global_quantityChange(id) {
    let currentQuantity = document.getElementById("global-policy-quantity" + id).value;

    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'quantity');
    data.append('new_value', currentQuantity);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/global/update/", true);
    loadHTML.send(data);
}

function global_nameChanged(id) {
    let currentName = document.getElementById("global-name" + id).value;

    let data = new FormData();

    data.append('policy_id', id);
    data.append('field_name', 'category');
    data.append('new_value', currentName);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/global/update/", true);
    loadHTML.send(data);
}

function global_logicOpened(id) {
    category_currentlyOpenedPolicy = id;

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else {
                document.getElementById("global-expressions-modal-body").innerHTML = loadHTML.responseText;
            }
        }
    };
    loadHTML.open("GET", "http://localhost:8000/app/system/policies/global/get/conditions/?policy_id=" + id, true);
    loadHTML.send();
}

function global_savePolicyChanges() {
    let data = new FormData();
    let conditions = document.getElementById("global-expressions-modal-body").value;
    data.append('policy_id', category_currentlyOpenedPolicy);
    data.append('field_name', 'conditions');
    data.append('new_value', conditions);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("Rules saved!");
                //window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "http://localhost:8000/app/system/policies/global/update/", true);
    loadHTML.send(data);
}


function printAllStates() {
    let state_strings = "";
    let states = document.getElementById("global-states").children;
    for (let i = 0; i < states.length; i++) {
        if (states[i] !== undefined) {
            state_strings = state_strings + '"\''+states[i].value+ '\'",'
        }
    }
    console.log(state_strings)
}