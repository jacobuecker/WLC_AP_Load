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

    var populationOptions = {
      strokeColor: "#FF0000",
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: "#FF0000",
      fillOpacity: 0.35,
      map: map,
      center: mapPosition,
      radius: 20
    };
    cityCircle = new google.maps.Circle(populationOptions);

});