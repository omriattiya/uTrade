$(document).ready(function () {
    $('#change-password-form').submit(function () {
        return false;
    });

    $('#update-details-form').submit(function () {
        return false;
    });

});


function changePassword() {
    var pass_old = document.getElementById("password_old").value;
    var pass_new1 = document.getElementById("password_1").value;
    var pass_new2 = document.getElementById("password_2").value;
    if (pass_new1 !== pass_new2) {
        alert('New passwords doesn\'t match');
        return;
    }
    var data = new FormData();
    data.append('current_password', pass_old);
    data.append('new_password', pass_new1);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else if (loadHTML.responseText === 'FAIL: suspect sql injection')
                alert(loadHTML.responseText);
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("Updated successfully");
                window.location.reload();
            }
            else {
                alert(loadHTML.responseText);
                window.location.href = "../app/home";
            }
        }
    };
    loadHTML.open("POST", "../app/users/edit_password/", true);
    loadHTML.send(data);
}

function updateDetails() {
    let state = document.getElementById("state").value;
    let age = document.getElementById("age").value;
    let sex = document.getElementById("sex").value;
    if (age > 120 || age < 0) {
        alert("Age must be between 0 and 120");
        return;
    }
    if (sex !== "Male" && sex !== "Female") {
        alert("Sex must be 'Male' or 'Female'");
        return;
    }

    let data = new FormData();
    data.append('state', state);
    data.append('age', age);
    data.append('sex', sex);

    let loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText.substring(0, 6) === 'FAILED') {
                alert(loadHTML.responseText)
            }
            else if (loadHTML.responseText === 'FAIL: suspect sql injection')
                alert(loadHTML.responseText);
            else if (loadHTML.responseText.substring(0, 7) === 'SUCCESS') {
                alert("Updated successfully");
                window.location.reload();
            }
        }
    };
    loadHTML.open("POST", "../app/users/update_details/", true);
    loadHTML.send(data);

}