var controlType, controlUsername, controlPassword, controlHeaderName, controlHeaderValue, controlToken, controlValue;
var liUsername, liPassword, liHeaderName, liHeaderValue, liToken;
var selectedType;

function updateControls() {
    selectedType = controlType.find("option:selected").val();

    if (selectedType == "Basic") {
        liUsername.show();
        liPassword.show();
        liHeaderName.hide();
        liHeaderValue.hide();
        liToken.hide();
    } else if (selectedType == "Headers") {
        liUsername.hide();
        liPassword.hide();
        liHeaderName.show();
        liHeaderValue.show();
        liToken.hide();
    } else if (selectedType == "OAuth") {
        liUsername.hide();
        liPassword.hide();
        liHeaderName.hide();
        liHeaderValue.hide();
        liToken.show();
    }

    calculateValue();
}

function calculateValue() {
    if (selectedType == "Basic") {
        if ((controlUsername.val() + ":" + controlPassword.val()).length > 1) {
            controlValue.val(Base64.encode(controlUsername.val() + ":" + controlPassword.val()));
        }
    } else if (selectedType == "Headers") {
        controlValue.val(controlHeaderName.val() + ":" + controlHeaderValue.val());
    } else if (selectedType == "OAuth") {
        controlValue.val(controlToken.val());
    }
}

$(document).ready(function () {
    /* Store references to controls and add events. */
    controlType = $("#id_type");
    controlType.on('change', function () {
        updateControls();
    });

    controlUsername = $("#id_username");
    controlUsername.on("input", null, null, calculateValue);
    liUsername = controlUsername.parent();

    controlPassword = $("#id_password");
    controlPassword.on("input", null, null, calculateValue);
    liPassword = controlPassword.parent();

    controlHeaderName = $("#id_header_name");
    controlHeaderName.on("input", null, null, calculateValue);
    liHeaderName = controlHeaderName.parent();

    controlHeaderValue = $("#id_header_value");
    controlHeaderValue.on("input", null, null, calculateValue);
    liHeaderValue = controlHeaderValue.parent();

    controlToken = $("#id_token");
    controlToken.on("input", null, null, calculateValue);
    liToken = controlToken.parent();

    controlValue = $("#id_value");

    updateControls();
});