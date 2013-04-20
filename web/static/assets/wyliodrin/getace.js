function save () {



  var posting = $.post( "/save", { source: editor.getValue() } );

 

  /* Put the results in a div */

  posting.done(function( data ) {
  
    info = jQuery.parseJSON (data);
	if (info.result==1)
	{
		
	}
	else
	{
		alert ("Save failed");
	}
  });

}
function load () {

var posting = $.get( "/load");
 posting.done(function( data ) {
    editor.setValue(data);
 });


}


 

