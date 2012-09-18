wsEnabled = null;

function create_socket(){
	var ws = new WebSocket("ws://10.0.40.39:9999/");
	ws.onmessage = function(event){
		
	}

	ws.onopen = function() {
	          
	};
}

function updatePage(){
	if(wsEnabled == false){
		setInterval(function(){
			$.post('/api_get_currentLoad',{},function(data){
				if(data != null){
					var series = [];
					var ticks = [];
					for (var i = data.length-1; i >= 0; i--) {
						series.push(data[i].cnt);
						ticks.push(data[i].name);
					};

					var plot = $.jqplot('currentLoad',[series],{

						seriesDefaults:{
							renderer:$.jqplot.BarRenderer,
							pointLabels: { show: true, location: 'e', edgeTolerance: -15 },
							rendererOptions: { fillToZero: false,
											   barDirection: 'horizontal'
							}
						},

						axes:{
							xaxis:{ 
							},
							yaxis: {renderer:$.jqplot.CategoryAxisRenderer,
									ticks: ticks,
									pad: 1.05
							}
							
						}

					});

				}
			},'json');
		},1000*60*15)
	}
}


$(window).ready(function(){
	if(window.WebSocket){
		//Browser supports websockets .... YES
		wsEnabled = true;
		$('#header').append("<div style='float:right;'>Websockets Enabled Page will update in real time.</div>")
		create_socket();
	} else {
		//Do it the old way
		wsEnabled = false;
		$('#header').append("<div style='float:right;'>Next Refresh is in <span id='timer'>900</span> seconds.</div>")
		setInterval(function countDown(){
											var timer = $('#timer').html();
											timer = timer - 1;
											if (timer == 0){
												$('#timer').html(900);
											} else {
												$('#timer').html(timer);
											}		
										},1000);
	}

	
});
