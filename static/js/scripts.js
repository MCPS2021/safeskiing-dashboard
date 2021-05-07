$(document).ready(function() {
    $('#devices').DataTable({
        ajax: "api/skipass",
        columns: [
            { data: "uuid"},
            { data: "last_position", render: function(d) {return "Station " + d}},
            { data: "last_battery", render: render_progressbar}
        ],
        searching: false,
        order: [[2, "asc"]]
    });
    $('#stations').DataTable({
        searching: false,
        order: [[1, "desc"]]
    });


} );

var map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);

function render_progressbar(value, x, y){
    return '<span class="'+get_color(value) + '">'+value+'%<div class="progress"><div class="progress-bar" role="progressbar" style="width: '+value+'%" aria-valuenow="'+value+'" aria-valuemin="0" aria-valuemax="100"></div></div></span>';
}

function get_color(value){
    if (value >= 60)
        return "green";
    if (value >= 16)
        return "yellow";
    return "red";
}
