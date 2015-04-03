function register() {
    var signupForm = $("#register-form");
    if (signupForm[0].elements["PASSWORD"].value != signupForm[0].elements["CONFIRM_PASSWORD"].value) {
        showErrorToast("The password must match the password confirmation!");
        return;
    }

    // Use AJAX to send as parameters.
    $.ajax({
        type: "POST",
        url: "/register/",
        data: signupForm.serialize(),
        complete: function (xhr) {
            if (xhr.status == 200) {
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

function login() {
    // Use AJAX to send as parameters.
    $.ajax({
        type: "POST",
        url: "/login/",
        data: $("#login-form").serialize(),
        complete: function (xhr) {
            if (xhr.status == 200) {
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
        url: "/logout-user/",
        data: $("#logout-form").serialize(),
        complete: function (xhr) {
            if (xhr.status == 200) {
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