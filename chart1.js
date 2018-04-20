function draw () {
	var chart = new CanvasJS.Chart("chartContainer",
	{
		title: {
			text: "Temperature Test"
		},
		axisX: {
			labelFormatter: function (e) {
				return CanvasJS.formatDate( e.value, "DDDMM HH:mm");
			},
		},

		data: [
		{
			type: "spline",
			dataPoints:GdataPoints
		}
		]
	});
	chart.render();
}

function graph(choice){
  GdataPoints = choice;
	draw();
}
