MAX_DATA = 10;

/* S T A R T U P */
$(document).ready(function () {
    loadHistory();
});

/* E V E N T S */

function selectClick() {
    selFile = getSelectedFile();

    $.ajax({url: "/api/history_select?file=" + selFile}).then(function(data) { 
        window.location.href = "/static/performance.html";
    });
}

function deleteClick() {
    selFile = getSelectedFile();

    $.ajax({url: "/api/history_delete?file=" + selFile}).then(function(data) { 
        loadHistory();
    });
}

/* U T I L I T Y */

function loadHistory() {
    $.ajax({url: "/api/history_list"}).then(function(data) { 
        fillHistory(data);
    });
}

function fillHistory(data) {
    innerHtml = "";

    for (var i = 0; i < data.length; i++) {
        entry = data[i];
        innerHtml += "<option value='" + entry + "'>" + entry + "</option>";
    }

    $("#historyEntries").html(innerHtml);
}

function getSelectedFile() {
    var ctrl = document.getElementById("historyEntries");
    return ctrl.value;
}