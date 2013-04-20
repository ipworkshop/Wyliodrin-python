$("#name").submit(function(event) {

  event.preventDefault();

  var $form = $( this ),

      pr_name = $form.find( 'input[name="pr_name"]' ).val(),
	  

      url = $form.attr( 'action' );

 

  /* Send the data using post */

  var posting = $.post( url, { name: pr_name} );

 

  /* Put the results in a div */

  posting.done(function( data ) {
  
    info = jQuery.parseJSON (data);
	if (info.result==1)
	{
		alert ("Project added");
	}
	else
	{
		alert ("Error");
	}
  });

});


 

