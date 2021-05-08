$(document).ready(function() {
    $.ajax({
        url:"api/cards",
        success: (data) => {
            $('#card-station-number').text(data['stations'])
            $('#card-low-battery').text(data['low_battery_devices'])
            $('#card-lifts').text(data['lifts'])
            $('#card-users').text(data['users'])
        },
        error: (xhr, data) => {
            console.log(data)
            $('#card-station-number').text("No data")
            $('#card-low-battery').text("No data")
            $('#card-lifts').text("No data")
            $('#card-users').text("No data")
        }
    });

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
        ajax: "api/stations",
        columns: [
            { data: "id", render: function(d) {return "Station " + d}},
            { data: "totalPeople", render: render_text}
        ],
        searching: false,
        order: [[1, "desc"]]
    });

    //podium
    $.ajax({
        url:"api/score",
        success: (data) => {
            let titles = $('.card-title');
            let texts = $('.card-text');
            let i = 0;
            Object.keys(data).forEach(function(key){
                texts.eq(i).text(data[key]);
                titles.eq(i).text(key);
                i++;
            });
        }
    });

} );

var markers = [];
var map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', { attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);

function render_progressbar(value, x, obj){
    if (value === '-1'){
        return '<span class="red">no data </span>'
    }
    return '<span class="'+get_color(value) + '">'+value+'%<div class="progress"><div class="progress-bar" role="progressbar" style="width: '+value+'%" aria-valuenow="'+value+'" aria-valuemin="0" aria-valuemax="100"></div></div></span>';
}

function render_text(value, x, obj){
    let color = "green";
    if (value > obj.danger_threshold){
        color = "red";
    } else if (value > obj.warning_threshold){
        color = "yellow"
    }
    //other things
    (color === "red") ? alert_manager(obj.id, true) : alert_manager(obj.id, false);
    addToMap(obj, value, color);
    return '<span class="'+color+'">'+value+'</span>';
}

function alert_manager(station, display){
    let alert = $('#alert_station_'+station);
    if (display && alert.length === 0){
        $("#alerts").append('<div class="alert alert-warning" id="alert_station_'+station+'">Station '+station+' is <strong>too crowded</strong>!\n</div>');
    } else if (display === false && alert.lenght !== 0){
        alert.remove();
    }
}

function addToMap(obj, value, color){
    //let marker = L.marker([lat, lon]).addTo(map);
    let marker = L.marker([obj.lat, obj.lon], {
                    icon: new L.AwesomeNumberMarkers({
                        number: value,
                        markerColor: color
                  })}).bindTooltip("Station "+obj.id).addTo(map);
    markers.push(marker);
    let group = new L.featureGroup(markers);
    map.fitBounds(group.getBounds());
}

function get_color(value){
    if (value >= 60)
        return "green";
    if (value >= 16)
        return "yellow";
    return "red";
}
