var map = null;
var circleArray = new Array();

function clearCircles(){
  for (var i = 0; i < circleArray.length; i++) {
    circleArray[i].setMap(null);
  }
  circleArray = new Array();
}


function updateMap(){
  clearCircles();
  $.post("/api_get_groups",{},function(data){
        for (var i = 0; i < data.length; i++) {
          var circlePos = new google.maps.LatLng(data[i].lat,data[i].lng);
          var populationOptions = {
              strokeColor: "#FF0000",
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: "#FF0000",
              fillOpacity: 0.35,
              map: map,
              center: circlePos,
              radius: data[i].cnt
          };
          apCircle = new google.maps.Circle(populationOptions);
          circleArray.push(apCircle);
        };
    },'json');
}


$(window).ready(function(){
	//http://maps.google.com/?ll=34.727241,-82.763754&spn=0.005881,0.013078&t=k&z=17
	var mapPosition = new google.maps.LatLng(34.727241,-82.761812);
	var mapOptions = {
        zoom: 17,
        center: mapPosition,
        mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    var mapElement = document.getElementById("map");
    map = new google.maps.Map(mapElement,mapOptions);

    updateMap();
    setInterval("updateMap()",1000 * 60);
});