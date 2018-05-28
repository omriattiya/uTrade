var Socket = null;
var connected = true;


$(document).ready(function () {
    Socket = new WebSocket('ws://localhost:8000/live_alerts/');
    Socket.onopen = function () {
        connected = true;
        var result = Socket.send(getCookie('login_hash'));
    };
    Socket.onmessage = function (evt) {
        document.getElementById('alerts-count').innerHTML = evt.data
    };
    $('#login-form').submit(function () {
        return false;
    });

});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function login() {
    var data = new FormData();
    var name = document.getElementById("email-modal").value;
    var pass = document.getElementById("password-modal").value;
    data.append('username', name);
    data.append('password', pass);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0,6) === 'FAILED') {
                alert(loadHTML.responseText);
            }
            else {
                setCookie('login_hash', loadHTML.responseText, 7);
                location.reload(true)
            }
        }
    };
    loadHTML.open("POST", "../app/users/login/", true);
    loadHTML.send(data);
}


function logout() {
    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'success') {
                setCookie('login_hash', "", 7);
                setTimeout(function () {
                    window.location.href = "../app/home/"
                }, 200)
            }
        }
    };
    loadHTML.open("POST", "../app/users/logout/", true);
    loadHTML.send();
}

function clearAlerts() {
    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'success'){
                location.reload()
            }
            else {
                alert(loadHTML.responseText)
            }
        }
    };
    loadHTML.open("POST", "../app/users/clear_alerts/", true);
    loadHTML.send();
}