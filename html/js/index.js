$(window).ready(function(){
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
});
