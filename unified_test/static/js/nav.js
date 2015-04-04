var name;

function showLogout() {
    var userNameSpan = $("#user-name");
    name = userNameSpan.text();
    userNameSpan.text("Logout");
}

function showUserName() {
    $("#user-name").text(name);
}

function logout() {
    // Use AJAX to send as parameters.
    $.ajax({
        type: "POST",
        url: "/logout/",
        data: $("#logout-form").serialize(),
        complete: function (xhr) {
            if (xhr.status == 200 || xhr.status == 0) {
                // User created. Redirect to the pages.
                window.location.replace("/pages/");
            } else if (xhr.status == 400) { // Server decided details specified are invalid. Use message.
                showErrorToast(xhr.responseText, 10000);
            } else {
                window.alert('An error occurred!\r\ncode: ' + xhr.status + "\r\nstatus: " + xhr.responseText);
            }
        }
    });
}