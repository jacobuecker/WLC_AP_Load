var groupPlot = null;
var apPlot = null;
var groupData = null;
var apData = null;

function compare(a,b) {
  if (a.cnt < b.cnt)
     return -1;
  if (a.cnt > b.cnt)
    return 1;
  return 0;
}


function updatePage(){
	$.post('/api_get_currentLoad',{},function(data){
		if(data != null){
			//data = data.sort(compare);

			apData = data;
			var series = [];
			var ticks = [];
			for (var i = data.length-1; i >= 0; i--) {
				series.push(data[i].cnt);
				ticks.push(data[i].name);
			};

			if(apPlot != null){
				apPlot.destroy();
			}

			apPlot = $.jqplot('currentLoad_by_ap',[series],{

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

	$.post("/api_get_groups",{},function(data){
		var series = [];
		var ticks = [];

		groupData = data.sort(compare);

		var totalCnt = 0;
		for (var i = 0; i < data.length; i++) {
			series.push(data[i].cnt);
			ticks.push(data[i].name);
			totalCnt += data[i].cnt;
		};

		$('#total_client_cnt').html(totalCnt);

		if(groupPlot != null){
			groupPlot.destroy();
		}


		groupPlot = $.jqplot('currentLoad_by_group',[series],{

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

		$('#currentLoad_by_group').bind('jqplotDataClick',
            function (ev, seriesIndex, pointIndex, data) {
                window.location.href = "/showGroupDetails?groupID=" + groupData[pointIndex].id;
            }
        );
	},'json');
}


$(window).ready(function(){
		$('#header').append("<div style='float:right;'>Next Refresh is in <span id='timer'>300</span> seconds.</div>");
		updatePage();
		setInterval(function countDown(){
			var timer = $('#timer').html();
			timer = timer - 1;
			if (timer == 0){
				$('#timer').html(300);
				updatePage(); 
				//document.location.reload(true);
			} else {
				$('#timer').html(timer);
			}		
		},1000);
});