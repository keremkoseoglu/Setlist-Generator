$(document).ready(function () {
    loadBands();
    loadEvents();
});

/* BANDS */

function loadBands() {
    $.ajax({url: "/api/band_list"}).then(function(data) { 
        fillCombo(data, "bands");
        bandOrEventChanged();
    });
}

function editBand() {
    editFile("bands", "edit_band");
}

function bandOrEventChanged() {
    var bandFile = document.getElementById("bands").selectedOptions[0].value;
    if (bandFile == "") {return;}
    var eventFile = document.getElementById("events").selectedOptions[0].value;
    if (eventFile == "") {return;}

    var apiUrl = "/api/get_selection_variant?band_json_file=" + bandFile + "&event_json_file=" + eventFile;

    $.ajax({url: apiUrl}).then(function(data) {
        for (var i = 0; i < data.length; i++) {
            var entry = data[i];
            var chkField = "";
            var prioField = "";

            if (entry.song_criteria == "key") {
                chkField = "sepKeyChk";
                prioField = "sepKeyPrio";
            }
            else if (entry.song_criteria == "genre") {
                chkField = "grpGenChk";
                prioField = "grpGenPrio";
            }
            else if (entry.song_criteria == "mood") {
                chkField = "grpMoodChk";
                prioField = "grpMoodPrio";
            }
            else if (entry.song_criteria == "age") {
                chkField = "grpAgeChk";
                prioField = "grpAgePrio";
            }
            else if (entry.song_criteria == "chord") {
                chkField = "grpChordChk";
                prioField = "grpChordPrio";
            }

            if (chkField == "" || prioField == "") { continue; }
            document.getElementById(chkField).checked = entry.selected;
            document.getElementById(prioField).value = entry.priority;
        }
    });
}

/* EVENTS */

function loadEvents() {
    $.ajax({url: "/api/event_list"}).then(function(data) { 
        fillCombo(data, "events");
        bandOrEventChanged();
    });
}

function editEvent() {
    editFile("events", "edit_event");
}

/* BOTTOM BUTTONS */

function generateStats() {
    editFile("bands", "stats");
}

function generateSetlist() {
    bandFile = getSelectedFile("bands");
    eventFile = getSelectedFile("events");
    selectionVariant = buildSelectionVariant();

    $.ajax({
        url: "/api/generate",
        method: "POST",
        data: {
            band_json_file: bandFile,
            event_json_file: eventFile,
            selection_variant: JSON.stringify(selectionVariant)
        }
    }).then(function(data) { 
        window.location.href = "/static/performance.html";
    });
}

function buildSelectionVariant() {
    return [
        {
            "priority": parseInt(document.getElementById("sepKeyPrio").value), 
            "selected": document.getElementById("sepKeyChk").checked, 
            "song_criteria": "key"
        }, 
        {
            "priority": parseInt(document.getElementById("grpGenPrio").value), 
            "selected": document.getElementById("grpGenChk").checked,
            "song_criteria": "genre"
        }, 
        {
            "priority": parseInt(document.getElementById("grpMoodPrio").value), 
            "selected": document.getElementById("grpMoodChk").checked,
            "song_criteria": "mood"
        }, 
        {
            "priority": parseInt(document.getElementById("grpAgePrio").value), 
            "selected": document.getElementById("grpAgeChk").checked,
            "song_criteria": "age"
        }, 
        {
            "priority": parseInt(document.getElementById("grpChordPrio").value), 
            "selected": document.getElementById("grpChordChk").checked,
            "song_criteria": "chord"
        }
      ];
}

function showHistory() {
    window.location.href = "/static/history.html";
}

/* UTILITY */

function fillCombo(data, id) {
    var combo = document.getElementById(id);
    combo.innerHTML = "";

    for (var i = 0; i < data.length; i++) {
        var data_entry = data[i];
        var opt = document.createElement("option");
        opt.value = data_entry;
        opt.innerHTML = data_entry.replace(".json", "");
        combo.appendChild(opt);
    }
}

function editFile(elementName, apiName) {
    var fileName = getSelectedFile(elementName);
    apiUrl = "/api/" + apiName + "?json_file=" + fileName
    $.ajax({url: apiUrl}).then(function(data) {  });
}

function getSelectedFile(elementName) {
    return document.getElementById(elementName).selectedOptions[0].value;
}
