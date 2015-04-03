function signupWithEmail() {
    var signupForm = $("#signup-email-form");
    if (signupForm[0].elements["PASSWORD"].value != signupForm[0].elements["CONFIRM_PASSWORD"].value) {
        showErrorToast("The password must match the password confirmation!");
        return;
    }

    // Use AJAX to send as parameters.
    $.ajax({
        type: "POST",
        url: apiUrl + "create-user-website/",
        data: signupForm.serialize(),
        complete: function (xhr) {
            if (xhr.status == 200) {
                // User created. Redirect to the profile.
                window.location.replace("/my-profile/");
            } else if (xhr.status == 400) { // Server decided details specified are invalid. Use message.
                showErrorToast(xhr.responseText, 10000);
            } else {
                window.alert('An error occurred!\r\ncode: ' + xhr.status + "\r\nstatus: " + xhr.responseText);
            }
        }
    });
}

function loginWithEmail() {
    // Use AJAX to send as parameters.
    $.ajax({
        type: "POST",
        url: apiUrl + "login-email-website/",
        data: $("#login-email-form").serialize(),
        complete: function (xhr) {
            if (xhr.status == 200) {
                // User created. Redirect to the profile.
                window.location.replace("/my-profile/");
            } else if (xhr.status == 400) { // Server decided details specified are invalid. Use message.
                showErrorToast(xhr.responseText, 10000);
            } else {
                window.alert('An error occurred!\r\ncode: ' + xhr.status + "\r\nstatus: " + xhr.responseText);
            }
        }
    });
}