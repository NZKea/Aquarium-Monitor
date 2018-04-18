function draw () {
	var chart = new CanvasJS.Chart("chartContainer",
	{
		title: {
			text: "Temperature Test"
		},
		axisX: {
			labelFormatter: function (e) {
				return CanvasJS.formatDate( e.value, "MMDDD HH:mm:ss");
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
