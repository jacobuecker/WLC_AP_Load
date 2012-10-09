var zoomHistory = null;
var apID = null;

function getParameterByName(name){
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function handleStartChange(start){
	$('#start').val(start);
}

function handleStopChange(stop){
	$('#stop').val(stop);
}

function zeroFill( number, width ){
  width -= number.toString().length;
  if ( width > 0 ){
    return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
  }
  return number + ""; // always return a string
}

$(document).ready(function(){
	apID = getParameterByName("apID");

	$('#btn_zoom').click(function(){
		//var start = humanToEpoch($('#start').val());
		//var stop = humanToEpoch($('#stop').val());

		$.post('/api_get_apData_span',{id: apID, start:$('#start').val(), stop:$('#stop').val() },function(data){
			var runningTotal = 0;
			var html = "<table><tr><td>Timestamp</td><td>Num of Clients</td></tr>";
			for (var x = 0; x < data.length; x++) {
				runningTotal += data[x].val;
				html += "<tr><td>" + data[x].timestamp + "</td><td>" + data[x].val + "</td></tr>";
			}
			html += "</table>";
			
			$('#zoom_max').html('Max: ' + Math.max.apply(Math,data.map(function(o){return o.val;})));
			$('#zoom_min').html('Min: ' + Math.min.apply(Math,data.map(function(o){return o.val;})));
			$('#zoom_avg').html('Max: ' + Math.round(runningTotal / data.length));
			$('#zoom_raw_data').html(html);
			$('#zoom_details').fadeIn('fast');


			$('#zoom_history').slidePicker({data:data});
		},'json');

	});

	
	$.post("/api_get_apData",{id:apID},function(data){
		var chartData = [];
		$('#dawn_of_time').html(data[0].timestamp + " <--> " + data[data.length-1].timestamp);
		handleStartChange(data[0].timestamp);
		handleStopChange(data[data.length-1].timestamp)
		var runningTotal = 0;
		for (var i = 0; i < data.length; i++) {
			runningTotal += data[i].val;
			//var stamp = epochToHuman(data[i].timestamp);
			//chartData.push({val:data[i].val,
			//				timestamp: stamp});
		};

		var totalAverage = Math.round(runningTotal / data.length);
		$("#average_since_dawn").html(totalAverage);


		zoomHistory = $('#entire_history').slidePicker({
						data:data,
						startChange: handleStartChange,
						stopChange: handleStopChange
					});


	},'json');

});