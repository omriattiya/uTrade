$(document).ready(function () {
    $('#change-password-form').submit(function () {
        return false;
    });

});


function changePassword() {
    var pass_old = document.getElementById("password_old").value;
    var pass_new1 = document.getElementById("password_1").value;
    var pass_new2 = document.getElementById("password_2").value;
    if(pass_new1 !== pass_new2){
        alert('New passwords doesn\'t match');
        return;
    }
    var data = new FormData();
    data.append('current_password', pass_old);
    data.append('new_password',pass_new1);

    var loadHTML = new XMLHttpRequest();
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
    loadHTML.open("POST", "../app/users/edit_password/", true);
    loadHTML.send(data);
}