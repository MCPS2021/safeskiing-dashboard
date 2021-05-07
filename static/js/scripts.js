$(document).ready(function() {
    $('#devices').DataTable({
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

function get_progressbar(value){
    return '<div class="progress"><div class="progress-bar" role="progressbar" style="width: '+value+'%" aria-valuenow="'+value+'" aria-valuemin="0" aria-valuemax="100"></div></div>';
}

function get_color(value){
    if (value >= 60)
        return "green";
    if (value >= 16)
        return "yellow";
    return "red";
}
