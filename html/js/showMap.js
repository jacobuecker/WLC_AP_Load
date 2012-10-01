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
          if(data[i].cnt > 0){
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

            google.maps.event.addListener(apCircle,'mouseover',function(event){
              //alert(pageX + " " + pageY);
              console.log(pageX + " " + pageY);
              $('#toolTip').css({"left":(pageX - 15) + "px", "top": (pageY - 15) + "px"});
              $('#toolTip').fadeIn('fast');
              $('#toolTip').html(this.radius);
            });

            google.maps.event.addListener(apCircle,'mouseout',function(event){
              //alert(pageX + " " + pageY);
              //$('#toolTip').css({"left":pageX + "px", "top":pageY + "px"});
              $('#toolTip').fadeOut('fast');
            });

            circleArray.push(apCircle);
          }
        };
    },'json');
}

var pageX = 0;
var pageY = 0;

$(window).ready(function(){
  $("#map").mousemove(function(e){
    pageX = e.pageX - this.offsetLeft;
    pageY = e.pageY - this.offsetTop;
  });


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