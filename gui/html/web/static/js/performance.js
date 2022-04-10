MAX_SET = 9;

$(document).ready(function () {
    buildSets();
});

function buildSets() {
    $.ajax({url: "/api/get_performance_set_list"}).then(function(data) { 
        createSetULs(data);
        setupSortable();
    });
}

function createSetULs(data) {
    for (var i = 0; i < data.length; i++) {
        var htmlCode = "";
        setSongs = data[i]["songs"]
        for (var s = 0; s < setSongs.length; s++) { htmlCode += "<li class='sortable-li'>" + setSongs[s] + "</li>" }
        setPos = i + 1;
        document.getElementById("set_" + setPos).innerHTML = htmlCode;
    }
}

function setupSortable() {
    Sortable.create(set_0, {group: 'songs', animation: 100 });
    Sortable.create(set_1, {group: 'songs', animation: 100 });
    Sortable.create(set_2, {group: 'songs', animation: 100 });
    Sortable.create(set_3, {group: 'songs', animation: 100 });
    Sortable.create(set_4, {group: 'songs', animation: 100 });
    Sortable.create(set_5, {group: 'songs', animation: 100 });
    Sortable.create(set_6, {group: 'songs', animation: 100 });
    Sortable.create(set_7, {group: 'songs', animation: 100 });
    Sortable.create(set_8, {group: 'songs', animation: 100 });
    Sortable.create(set_9, {group: 'songs', animation: 100 });
}

function saveClick() {
    var newSetList = buildSetListFromULs();

    $.ajax({
        url: "/api/save",
        method: "POST",
        data: { song_order: JSON.stringify(newSetList) }
    }).then(function(data) { 
        window.location.href = "/static/index.html";
    });
}

function buildSetListFromULs() {
    var output = []

    for (var s = 0; s <= MAX_SET; s++) {
        var ulName = "set_" + s;
        var setDict = {"set": s, "songs": []};

        var lis = document.getElementById(ulName).getElementsByTagName("li");
        for (var l = 0; l < lis.length; l++) {
            var song = lis[l].innerHTML;
            setDict["songs"].push(song);
        }

        output.push(setDict);
    }

    return output;
}