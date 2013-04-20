$("#login").submit(function(event) {

  event.preventDefault();

  var $form = $( this ),

      email = $form.find( 'input[name="email"]' ).val(),
	  password = $form.find( 'input[name="password"]' ).val(),

      url = $form.attr( 'action' );

 

  /* Send the data using post */

  var posting = $.post( url, { email: email, password: password} );

 

  /* Put the results in a div */

  posting.done(function( data ) {
  
    info = jQuery.parseJSON (data);
	if (info.result==1)
	{
		window.location = "/fluid"
	}
	else
	{
		alert ("Login failed");
	}
  });

});


 

