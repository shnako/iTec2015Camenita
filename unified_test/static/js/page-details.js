/* region Toasts */

/* endregion */

/* region Authentication controls */
var controlType, controlUsername, controlPassword, controlHeaderName, controlHeaderValue, controlToken, controlValue;
var liUsername, liPassword, liHeaderName, liHeaderValue, liToken, liValue;
var selectedType;

function updateControls() {
    selectedType = controlType.find("option:selected").val();

    if (selectedType == "None") {
        liUsername.hide();
        liPassword.hide();
        liHeaderName.hide();
        liHeaderValue.hide();
        liToken.hide();
        liValue.hide();
    } else if (selectedType == "Basic") {
        liUsername.show();
        liPassword.show();
        liHeaderName.hide();
        liHeaderValue.hide();
        liToken.hide();
        liValue.show();
    } else if (selectedType == "Headers") {
        liUsername.hide();
        liPassword.hide();
        liHeaderName.show();
        liHeaderValue.show();
        liToken.hide();
        liValue.show();
    } else if (selectedType == "OAuth") {
        liUsername.hide();
        liPassword.hide();
        liHeaderName.hide();
        liHeaderValue.hide();
        liToken.show();
        liValue.show();
    }

    calculateValue();
}

function calculateValue() {
    controlValue.val(""); // Reset value to empty.

    if (selectedType == "None") {
        return; // Do nothing as already empty. Using unneeded return to prevent future problems.
    } else if (selectedType == "Basic") {
        if ((controlUsername.val() + ":" + controlPassword.val()).length > 1) {
            controlValue.val(Base64.encode(controlUsername.val() + ":" + controlPassword.val()));
        }
    } else if (selectedType == "Headers") {
        controlValue.val(controlHeaderName.val() + ":" + controlHeaderValue.val());
    } else if (selectedType == "OAuth") {
        controlValue.val(controlToken.val());
    }
}

function loadInitialValue(initialValue) {
    if (initialValue <= 1) return;

    if (selectedType == "Basic") {
        initialValue = Base64.decode(initialValue);
        var split = initialValue.split(":");
        controlUsername.val(split[0]);
        controlPassword.val(split[1]);
    } else if (selectedType == "Headers") {
        var split = initialValue.split(":");
        controlHeaderName.val(split[0]);
        controlHeaderValue.val(split[1]);
    } else if (selectedType == "OAuth") {
        controlToken.val(initialValue);
    }

    calculateValue();
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
    liValue = controlValue.parent();

    var initialValue = controlValue.val();

    updateControls();

    loadInitialValue(initialValue);

    /* Drag and drop controls. */
    var textarea_response = document.getElementById('id_response');
    textarea_response.addEventListener('dragover', handleDragOver, false);
    textarea_response.addEventListener('drop', handleFileSelect, false);
    textarea_response.setAttribute('placeholder', 'You can also drag a file here!');
    var textarea_dynamic_code = document.getElementById('id_dynamic_code');
    textarea_dynamic_code.addEventListener('dragover', handleDragOver, false);
    textarea_dynamic_code.addEventListener('drop', handleFileSelect, false);
    textarea_dynamic_code.setAttribute('placeholder', 'You can also drag a file here!');
});
/* endregion */