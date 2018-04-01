// We create the tile layers that will be the selectable backgrounds of our map.
var graymap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=" +
  "pk.eyJ1Ijoic3ViaGFzdXNoaSIsImEiOiJjamRoank0YTAwZWE0MnhvMmw5eWd1OWU1In0.t6Bzt2OPJXvtCMb2I-UaTA", {
    attribution: "Map data &copy;" +
      "<a href='http://openstreetmap.org'>OpenStreetMap</a> contributors," +
      "<a href='http://creativecommons.org/licenses/by-sa/2.0/'>" +
      "CC-BY-SA</a>" +
      "Imagery &copy;" +
      "<a href='http://mapbox.com'>Mapbox</a>",
    maxZoom: 18
  });

// We then create the map object with options.
// Adding the tile layers we just created to an array of layers.
var map = L.map("mapid", {
  center: [40.7, -94.5],
  zoom: 3,
  layers: [graymap]
});

// Adding our 'graymap' tile layer to the map.
graymap.addTo(map);

 /* data route */
var url = "/gender_disperity"
d3.json(url, function(error, response) {
    
  // console.log(response);
 
  var femaleMarkers = [];
  var maleMarkers = [];

  //Parse through json object to extract pop-up data
   for (var i = 0; i < response.length; i++) {

    femaleMarkers.push(
    L.minichart([response[i].LATITUDE, response[i].LONGITUDE], {type:'pie',data: [response[i].FEMALE, response[i].MALE],labels:'auto',
    labelMinSize:8, labelMaxSize:10,width:40,height:40})
    .bindPopup("<h5>" + response[i].COUNTRY + "</h5>\
    <ul class=list-group>\
    <li class=list-group-item>" + "Female_count: " + response[i].FEMALE + "</li>\
    <li class=list-group-item>" + "Male_count: " + response[i].MALE + "</li>"
  ))

  }  
  
  var female = L.layerGroup(femaleMarkers);
  map.addLayer(female) ;
  });
  

