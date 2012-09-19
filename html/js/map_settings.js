var groupData = null;
var apData = null;
var currentGroup = null;

function compare(el1, el2, index) {
  return el1[index] == el2[index] ? 0 : (el1[index] < el2[index] ? -1 : 1);
}


function find_outliers(){
	for (var i = 0; i < apData.length; i++) {
		apData[i].grouped = false;
	};

	for (var i = 0; i < groupData.length; i++) {
		// Foreach group
		if (typeof(groupData[i].aps) !== "undefined") {
			for (var j = 0; j < groupData[i].aps.length; j++) {
			var currentAP = groupData[i].aps[j].key;
			for (var x = 0; x < apData.length; x++) {
				if (currentAP = apData[x].key){
					apData[x].grouped = true;
				}
			};
		};
		}
		
	};
}

function bind_droppable(){
	$('#btn_mod_save_cords').click(function(){
		var group  = currentGroup;
		$('.lat',$(group)).val($('#mod_lat').val());
		$('.lng',$(group)).val($('#mod_lng').val());
		$.modal.close();
	});

	$('.btn_cordHelp').click(function(){
		var mapPosition = new google.maps.LatLng(34.727241,-82.761812);
		var mapOptions = {
	        zoom: 17,
	        center: mapPosition,
	        mapTypeId: google.maps.MapTypeId.SATELLITE
	    };
	    var mapElement = document.getElementById("map");
	    var marker;
	    map = new google.maps.Map(mapElement,mapOptions);
	    google.maps.event.addListener(map, 'center_changed', function() {
		   var newCenter = map.getCenter();
		   $('#mod_lat').val(newCenter.lat());
		   $('#mod_lng').val(newCenter.lng());
		   marker.setPosition(map.getCenter());
		});
		marker = new google.maps.Marker({
		    position: map.getCenter(),
		    map: map
	  	});
		currentGroup = $(this).parent();

		$.modal($('#modalDiv'));
	});

	$( ".groupNode" ).droppable({
		drop: function( event, ui ) {
			var droppedNode = ui.draggable;
			$(ui.draggable).hide();
			$('.hid_aps',$(this)).val($('.hid_aps',$(this)).val() + ":" + $('input',$(droppedNode)).val())
			$('.aps',$(this)).append(droppedNode.text() + '<br />');
			//alert(ui.draggable.text());
		}
	});
}

function save_groups(){
	var data = new Array();
	$('.groupNode').each(function(){
		var dataNode = new Object();
		if ($('.hid_id',$(this)).val() == ""){
			dataNode['id'] = null
		} else {
			dataNode['id'] = $('.hid_id',$(this)).val();
		}
		
		dataNode["aps"] = $('.hid_aps',$(this)).val();
		dataNode["name"] = $('.name',$(this)).val();
		dataNode["lat"] = $('.lat',$(this)).val();
		dataNode["lng"] = $('.lng',$(this)).val();
		data[data.length] = dataNode;
	});
	data = JSON.stringify(data);
	$.post('/api_save_groups',{data:data},function(data){
		if(data.success){
			window.reload();
		}
	},'json');
}

function display_groups(){
	var holder = $('#groups');
	for (var i = 0; i < groupData.length; i++) {
		$(holder).append(generateGroup(groupData[i].name,groupData[i].lat,groupData[i].lng,"",""));
	};
}

function display_loners(){
	var holder = $('#aps');
	for (var i = 0; i < apData.length; i++) {
		if (apData[i].grouped == false){
			$(holder).append("<div class='apNode' draggable='true'><img src='/html/imgs/ap.png' />" + apData[i].name + "<input type='hidden' value='" + apData[i].key + "' /></div>");
		}
	};
	$('.apNode').each(function(){
		$(this).draggable();
	});
}

function generateGroup(name,lat,lng,aps_key,id,aps){
	var html = "<div class='groupNode'>";
	html += "Group Name:<br /> <input class='name' type='text' value='" + name + "'></input><br />";
	html += "<input class='btn_cordHelp' type='button' value='Help with Cords' /><br />";
	html += "Lat:<br /> <input class='lat' type='text' value='" + lat + "'></input><br />";
	html += "Lng:<br /> <input class='lng' type='text' value='" + lng + "'></input><br />";
	html += "APs<br />";
	html += "<input type='hidden' class='hid_aps' value='" + aps_key + "' />" ;
	html += "<input type='hidden' class='hid_id' value='" + id + "' />" ;
	html += "<div class='aps'>" + aps + "</div>"
	html += "</div>";
	return html;
}

$(window).ready(function(){
	$('#btn_saveGroups').click(function(){
		save_groups();
	});

	$.ajax({
        type: "GET",
        url: '/api_get_groups',
        async: false,
        dataType: "json",
        beforeSend: function(x) {
		  if(x && x.overrideMimeType) {
		   x.overrideMimeType("application/j-son;charset=UTF-8");
		  }
		 },
		 success: function(data){
		  groupData = data;
		}
    });

    $.ajax({
        type: "GET",
        url: '/api_get_currentLoad',
        async: false,
        dataType: "json",
        beforeSend: function(x) {
		  if(x && x.overrideMimeType) {
		   x.overrideMimeType("application/j-son;charset=UTF-8");
		  }
		 },
		 success: function(data){
		  apData = data;
		  apData = apData.sort(function(el1,el2){
		  	return compare(el1,el2,"name");
		  });
		}
    });

	find_outliers();
	display_groups();
	display_loners();

	$('#btn_newGroup').click(function(){
		//create a new group and allow for dragging to that new group
		$('#groups').append(generateGroup("","","","","",""));
		bind_droppable();
	});

});