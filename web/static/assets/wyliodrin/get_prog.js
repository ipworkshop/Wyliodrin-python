
function run ()
{
	var posting = $.get( "/values");
 	posting.done(function( data ) {
    	vals = jQuery.parseJSON (data);
    	for (i in vals)
    	{
    		info = vals[i];
    		var canvas = document.getElementById(info.signal);
    		if (canvas!=null)
    		{
				var context = canvas.getContext("2d");

				context.clearRect(0, 0, canvas.width, canvas.height);
			}
			if (info.signal == "temperature")
			{
				var thermometer = new RGraph.Thermometer(info.signal, 0,255,info.values[info.values.length-1]);
				thermometer.Draw();
			}
			if (info.signal == "series")
			{
				// Create the chart. The values are: the canvas tag ID,  the minimum, the maximum and the actual value.
				var gauge = new RGraph.Gauge(info.signal, 0, 255, info.values[info.values.length-1]);
				
				// Configure the chart to appear as wished
				gauge.Set('chart.title', 'Bandwidth');
				
				// Now call the .Draw() method to draw the chart.
				gauge.Draw();
			}
			if (info.signal == "buttons")
			{
				// Some data that is to be shown on the bar chart. To show a stacked or grouped chart
				// each number should be an array of further numbers instead.
				value = info.values[info.values.length-1]
				var data = [value & 1, (value & 2) >> 1, (value & 4) >> 2, (value & 16) >> 4];
				
				
				// An example of the data used by stacked and grouped charts
				// var data = [[1,5,6], [4,5,3], [7,8,9]]
		
				
				// Create the br chart. The arguments are the ID of the canvas tag and the data
				var bar = new RGraph.Bar(info.signal, data);
				
				
				// Now configure the chart to appear as wanted by using the .Set() method.
				// All available properties are listed below.
				bar.Set('chart.labels', ['1', '2', '3', '4']);
				bar.Set('chart.gutter.left', 45);
				bar.Set('chart.background.barcolor1', 'white');
				bar.Set('chart.background.barcolor2', 'white');
				bar.Set('chart.background.grid', true);
				bar.Set('chart.colors', ['red']);
				
				
				// Now call the .Draw() method to draw the chart
				bar.Draw();
			}
			if (info.signal == "light")
			{
				// The data for the Line chart. Multiple lines are specified as seperate arrays.
		
				// Create the Line chart object. The arguments are the canvas ID and the data array.
				// alert (info.values);
				var line = new RGraph.Line(info.signal, info.values);
				
				// The way to specify multiple lines is by giving multiple arrays, like this:
				// var line = new RGraph.Line("myLine", [4,6,8], [8,4,6], [4,5,3]);
				
				// Configure the chart to appear as you wish.
				line.Set('chart.background.barcolor1', 'white');
				line.Set('chart.background.barcolor2', 'white');
				line.Set('chart.background.grid.color', 'rgba(238,238,238,1)');
				line.Set('chart.colors', ['yellow']);
				line.Set('chart.linewidth', 2);
				line.Set('chart.filled', false);
				line.Set('chart.hmargin', 5);
				//line.Set('chart.labels', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']);
				line.Set('chart.gutter.left', 40);
				
				// Now call the .Draw() method to draw the chart.
				line.Draw();
			}
		}
    	setTimeout ("run ()", 500); 			
 	});
}

function rasp () {


var posting = $.post( "/run", { source: editor.getValue() } );
 posting.done(function( data ) {
  
    info = jQuery.parseJSON (data);
	if (info.result==1)
	{
		setTimeout ("run ()", 500); 			
	}
	else
	{
		alert ("Run failed");
	}
  });
 



}


$("#led").change(function(event) {

  event.preventDefault();

  var $form = $( this ),

      red = $form.find( 'input[name="red"]' ).val(),
	  green = $form.find( 'input[name="green"]' ).val(),
	  blue = $form.find( 'input[name="blue"]' ).val(),

      url = $form.attr( 'action' );

 

  /* Send the data using post */

  var posting = $.post( url, { red: red, green: green, blue: blue} );

 

  /* Put the results in a div */

});


 

