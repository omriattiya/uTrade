$(document).ready(function () {
    $('#send-message-form').submit(function () {
        return false;
    });
});


function updateMessageContent(message_id) {
    document.getElementById('message-content').innerHTML = '<p>' + document.getElementById(message_id).innerHTML + '</p>'
}

function sendMessage() {

    var data = new FormData();
    data.append('from', document.getElementById('shop-name').innerHTML);
    data.append('to', document.getElementById("message-to-modal").value);
    data.append('content', document.getElementById("message-content-modal").value);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else if (loadHTML.responseText === 'SUCCESS') {
                alert("Message Sent!");
                window.location.href = "../app/shop/messages/?content=sent&shop_name=" + document.getElementById('shop-name').innerHTML;
            }
            else {
                alert(loadHTML.responseText);
                window.location.href = "../app/home";
            }
        }
    };
    loadHTML.open("POST", "../app/messages/send_message_from_shop/", true);
    loadHTML.send(data);
}