var map = L.map('map',{
    center:[0,0],
    zoomsnap: .25,
    zoom: 2.5,
    scrollWheelZoom: false,
});
var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
"access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ." +
"T6YbdDixkOBWH_k9GbS8JQ").addTo(map);

var url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
d3.json(url, function(data){
    L.geoJson(data, {
    clickable: true
    }).addTo(map);
   
})


