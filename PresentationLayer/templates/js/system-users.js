function deleteUser(username) {
    var data = new FormData();
    data.append('registered_user', username);

    var loadHTML = new XMLHttpRequest();
    loadHTML.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            if (loadHTML.responseText === 'fail') {
                alert("Failed")
            }
            else if (loadHTML.responseText === 'success') {
                alert("User has been removed.");
                location.reload()
            }
        }
    };
    loadHTML.open("POST", "../app/users/remove_user/", true);
    loadHTML.send(data);
}