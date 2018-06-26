console.log('OUTSIDE callback function'); 


$(document).ready(function() {
    $(document).on('change', '.one_file', add);
    //$(document).on('click', '#logout', logout_function);
    if ($('#user_p').is(':visible')){
      $( "#user_l" ).hide();
    }

    function add() {
      $('#files').append("<input type='file' class='one_file' name='filee'/><br/>");
      console.log("appended");
    };

    //function logout_function(){

    //$(document).on("click","#submit_logout",function() {
    $( "#logout" ).submit(function( e ) {
      console.log("logout clicked");
      e.preventDefault();
      var request = $.ajax({
        url: "logout/",
        method: "GET",
      });
      request.done(function( msg ) {
        $( "#user_p" ).fadeOut( "slow" );
        $( "#user_l" ).show();
        console.log("logout happened");
      });
    });


});


	