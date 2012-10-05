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


$(document).ready(function(){
	var id = getParameterByName("groupID");
	$.post("/api_get_groupData",{id:id},function(data){
		var chartData = [];
		var start = new Date(data[0].timestamp * 1000);
		var end = new Date(data[data.length-1].timestamp * 1000);

		var startStr = start.getHours() + ":" + start.getMinutes() + ":" + start.getSeconds() + " " + (start.getMonth() + 1) + "/" + start.getDate() + "/" + start.getFullYear();
		var endStr = end.getHours() + ":" + end.getMinutes() + ":" + end.getSeconds() + " " + (end.getMonth() + 1) + "/" + end.getDate() + "/" + end.getFullYear();
		
		$('#dawn_of_time').html(startStr + " <--> " + endStr);

		var runningTotal = 0;
		for (var i = 0; i < data.length; i++) {
			runningTotal += data[i].val;
			var stamp = new Date(data[i].timestamp * 1000);
			stamp = stamp.getHours() + ":" + stamp.getMinutes() + ":" + stamp.getSeconds() + " " + (stamp.getMonth() + 1) + "/" + stamp.getDate() + "/" + stamp.getFullYear();
			chartData.push({val:data[i].val,
							timestamp: stamp});
		};

		var totalAverage = Math.round(runningTotal / data.length);
		$("#average_since_dawn").html(totalAverage);


		$('#entire_history').slidePicker({data:chartData});
	},'json');

});