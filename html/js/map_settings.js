var groupData = null;
var apData = null;
var currentGroup = null;
var map = null;
var currentLat = null;
var currentLng = null;

function compare(el1, el2, index) {
  return el1[index] == el2[index] ? 0 : (el1[index] < el2[index] ? -1 : 1);
}

function boxup_groups(){
	$('.groupNode').each(function(){
		$(this).css({  "width":"100px",
					   "height":"100px",
					   "padding": "5px"
					});
		$('.title',this).show();
		$('.details',this).hide();
	});
}

function unbox_groups(){
	$('.groupNode').each(function(){
		$(this).css({  "width":"300px",
					   "height":"",
					   "padding": "20px"
					});
		$('.title',this).hide();
		$('.details',this).show();
	});
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
					if (currentAP == apData[x].key){
						apData[x].grouped = true;
						break;
						
					}
				};
			};
		}
	};
}

function bind_droppable(){
	$('.name').keyup(function(){
		$('.title',$(this).parent().parent()).html($(this).val() + "<br><br>::Drop Here::");
	});

	$('.btn_delete_group').click(function(){
		$.post("/api_delete_group",{id:$('.hid_id',$(this).parent().parent()).val()},function(data){
			if (data.success){
				location.reload();
			}
		},'json');
	});

	$('#btn_mod_save_cords').click(function(){
		$('.lat',$(currentGroup)).val(currentLat);
		$('.lng',$(currentGroup)).val(currentLng);
		$.modal.close();
		currentLat = null;
		currentLng = null;
	});

	$('.btn_cordHelp').click(function(){
		$.modal($('#modalDiv'));
		currentGroup = $(this).parent().parent();

		var templat = $('.lat',$(currentGroup)).val();
		var templng = $('.lng',$(currentGroup)).val();

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
			currentLat = newCenter.lat();
			currentLng = newCenter.lng();
			marker.setPosition(map.getCenter());
		});
		marker = new google.maps.Marker({
		    position: map.getCenter(),
		    map: map
	  	});

		if (templng != "" && templat != ""){
			map.setCenter(new google.maps.LatLng(templat,templng));
		} else {
			map.setCenter(mapPosition);
		}

		
	});

	$( ".groupNode" ).droppable({
		hoverClass: "hover_active",
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
			location.reload();
		}
	},'json');
}

function display_groups(){
	var holder = $('#groups');
	for (var i = 0; i < groupData.length; i++) {
		var aps = "";
		var apnames = "";
		for (var x = 0; x < groupData[i].aps.length; x++) {
			aps += ":" + groupData[i].aps[x].key;
			apnames +=  groupData[i].aps[x].name + "<br />"
		};
		$(holder).append(generateGroup(groupData[i].name,  groupData[i].lat,  groupData[i].lng,  aps, groupData[i].id  ,  apnames));
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
		$(this).draggable({
			start:function(){
				boxup_groups();
			},
			stop: function(){
				unbox_groups();
			}
		});
	});
}

function generateGroup(name,lat,lng,aps_key,id,aps){
	var html = "<div class='groupNode'>";
	html += "<span class='title' style='display:none; width:100%; height:100%; text-align:center;'>" + name + "<br /><br /> ::Drop Here::</span>";
	html += "<div class='details'>";
	html += "<img class='btn_delete_group' src='/html/imgs/x.png' style='position:absolute; top:-14px; right:-14px; cursor:pointer;' title='Delete Group' />";
	html += "Group Name:<br /> <input class='name' type='text' value='" + name + "'></input><br />";
	html += "<input class='btn_cordHelp' type='button' value='Help with Cords' /><br />";
	html += "Lat:<br /> <input class='lat' type='text' value='" + lat + "'></input><br />";
	html += "Lng:<br /> <input class='lng' type='text' value='" + lng + "'></input><br />";
	html += "APs<br />";
	html += "<input type='hidden' class='hid_aps' value='" + aps_key + "' />" ;
	html += "<input type='hidden' class='hid_id' value='" + id + "' />" ;
	html += "<div class='aps'>" + aps + "</div>"
	html += "</div>";
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
	bind_droppable();

	$('#btn_newGroup').click(function(){
		//create a new group and allow for dragging to that new group
		$('#groups').prepend(generateGroup("","","","","",""));
		bind_droppable();
	});
});