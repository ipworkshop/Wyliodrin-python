function rasp () {


var code = $.post( "/run", { program: editor.getValue() } );
 posting.done(function( data ) {
  
    info = jQuery.parseJSON (data);
	if (info.result==1)
	{
		
	}
	else
	{
		alert ("Run failed");
	}
  });
 



}


 

