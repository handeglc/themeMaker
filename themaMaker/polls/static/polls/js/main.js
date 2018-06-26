console.log('OUTSIDE callback function'); 

/*function loadDoc() {
  console.log('inside callback function'); 
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", '/more/', true);
  xhttp.send(null);
}*/
$(document).ready(function() {
    $(document).on('change', '.one_file', add);
    //$(document).on('click', '#logout', logout_function);

    $( "#user_l" ).fadeOut("fast");

    function add() {
      $('#files').append("<input type='file' class='one_file' name='filee'/><br/>");
      console.log("appended");
    };

    //function logout_function(){
      console.log("heyo");
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

      /* e.preventDefault();
       $.ajax({
           url: "index.html",
           method: $(this).attr('method'),
           success: function(data){ $('#target_logout').html(data) }
       });  */
    });

    

});
   
//};

/*function submit() {
  $('#colors_files').append("hello");
  console.log("submitted");

};*/

/*$('form').on('submit',function(e){
    //e.preventDefault();
    $('#colors_files').append("hello");

    fd = new FormData();
		fd.append('file', $(".one_file").get(0).files[0]);
});*/

/*$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});*/

	