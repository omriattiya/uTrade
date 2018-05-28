
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
    data.append('to', document.getElementById("message-to-modal").value);
    data.append('content', document.getElementById("message-content-modal").value);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0,6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else if (loadHTML.responseText.substring(0,7) === 'SUCCESS') {
                alert("Message Sent!");
                window.location.href = "../app/home/messages/?content=sent"
            }
        }
    };
    loadHTML.open("POST", "../app/messages/send_message/", true);
    loadHTML.send(data);
}