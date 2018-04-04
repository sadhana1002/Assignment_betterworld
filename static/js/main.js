var map = L.map('map',{
    center:[0,0],
    zoomsnap: .25,
    zoom: 2.5,
    scrollWheelZoom: false,
});
var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
"access_token=pk.eyJ1IjoibWluY2tpbTEyMjIiLCJhIjoiY2pkaGp5NHR0MHd3eDMxbnF6bXlsazhxYiJ9.6WOQPTje5_AYqQO_4W36xQ").addTo(map);

var url = "/countries";
var geoURL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json";
d3.json(url, function(error, response){
    if(error) console.warn(error);   
    d3.json(geoURL, function(error, geoResponse){
        L.geoJson(geoResponse,{
            style: function(feature) {
                return {
                fillOpacity: 0,
                weight: 1.5
                };
            },
            onEachFeature: function(feature, layer) {
                // Set mouse events to change map styling
                layer.on({
                // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
                mouseover: function(event) {
                    layer = event.target;
                    layer.setStyle({
                    fillOpacity: 0.5
                    });
                },
                // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
                mouseout: function(event) {
                    layer = event.target;
                    layer.setStyle({
                    fillOpacity: 0
                    });
                },
                // When a feature (neighborhood) is clicked, it is enlarged to fit the screen
                click: function(event) {
                    map.fitBounds(event.target.getBounds());
                    var currentClickedCountry = event.target.feature.properties.name
                    createGraph(currentClickedCountry);
                }
                });                
            }
        }).addTo(map);   
    });
}); 
function createGraph(country){ß
    console.log(country);
    if(country === "Laos"){
        var renameCountry = "Lao People's Democratic Republic";
        var url = `/countries/${renameCountry}`;
        console.log(url);
        d3.json(url, function(error, response){
        if(error) console.warn(error);
        console.log(response);
    });
    } else if(country==="United States of America"){
        var renameCountry = "United States";
        var url = `/countries/${renameCountry}`;
        console.log(url);
        d3.json(url, function(error, response){
        if(error) console.warn(error);
        console.log(response)
    }); 
    } else if(country==="Democratic Republic of the Congo"){
    var renameCountry = "The Democratic Republic of the Congo";
    var url = `/countries/${renameCountry}`;
    console.log(url);
    d3.json(url, function(error, response){
    if(error) console.warn(error);
    console.log(response)
    });
    } else if(country==="Ivory Coast"){
        var renameCountry = "Cote D'Ivoire";
        var url = `/countries/${renameCountry}`;
        console.log(url);
        d3.json(url, function(error, response){
        if(error) console.warn(error);
        console.log(response)
    });
    } else if(country==="Myanmar"){
        var renameCountry = "Myanmar (Burma)";
        var url = `/countries/${renameCountry}`;
        console.log(url);
        d3.json(url, function(error, response){
        if(error) console.warn(error);
        console.log(response)
    });     
    } else if(country==="East Timor"){
        var renameCountry = "Timor-Leste";
        var url = `/countries/${renameCountry}`;
        console.log(url);
        d3.json(url, function(error, response){
        if(error) console.warn(error);
        console.log(response)
    }); 
     
    } else{
        var url = `/countries/${country}`;
        console.log(url);
        d3.json(url, function(error, response){
            if(error) console.warn(error);
            if(response.length != 0){
            console.log(response)
            } else {
                alert("No data for given country");
            }
        });
    }
}