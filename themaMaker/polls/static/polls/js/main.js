console.log('OUTSIDE callback function'); 

function getCookie(c_name)
    {
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
     }

$(document).ready(function() {
    $( "#tabs" ).tabs();

    $(document).on('change', '.one_file', add);
    //$(document).on('click', '#logout', logout_function);
    if ($('.row').is(':visible')){
      $( "#tabs" ).hide();
    }

    function add() {
      $('#files').append("<input type='file' class='one_file' name='filee'/><br/>");
      console.log("appended");
    };

    $(".c_info").hide();
    
    $(".color").on("mouseenter", function() {
       $(this).find('.c_info').show();
    });
    $(".color").on("mouseleave", function() {
       $(this).find('.c_info').hide();  //or $('.overlay').hide()
    });

    $('.fa-trash-alt').on('click', function () {
      var cg_list_id = $(this).attr("cg_list_id");
      console.log("should be deleted "+ cg_list_id);

      $.ajax({
            type: "POST",
            url: "delete_cg/",
            data: {"id": cg_list_id},
            dataType: "json",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data) {
                //var obj = jQuery.parseJSON(data); if the dataType is not specified as json uncomment this
                // do what ever you want with the server response
                console.log("success delete");
                if(data["saved"]=="deleted"){
                  window.location.reload();
                }

            },
            error: function() {
                //alert('error handing here');
            }
        });

    });


    $('#login-form').submit(function( e ) {
      e.preventDefault();
      console.log("login clicked");
      var uname = $('#username').val();
      var pass = $('#password').val();

      $.ajax({
          type: "POST",
          url: "/",
          data: {"username":uname, "password": pass},
          dataType: "json",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          success: function(data) {
              //var obj = jQuery.parseJSON(data); if the dataType is not specified as json uncomment this
              // do what ever you want with the server response
              console.log("login data sent");
              console.log(warning);
              var warning= data["message"];
              if(warning == "done" ){
                window.location.reload();
              }
              else{
                $( "#error" ).empty();
                $("#error").removeAttr('hidden');
                $("#error").append(warning);
              }
              
            

          },
          error: function() {
              //alert('error handing here');
          }
      });
      
     
    });



      
    $('#signup').submit(function( e ) {
      e.preventDefault();
      console.log("signup clicked");
      var uname = $('#un').val();
      var pass = $('#ps').val();
      var repass = $('#ps2').val();

      if(pass != repass){
        $("#notMatch").removeAttr('hidden');
        console.log("should show");
      }
      else{
        $.ajax({
            type: "POST",
            url: "signup/",
            data: {"username":uname, "password": pass},
            dataType: "json",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function(data) {
                //var obj = jQuery.parseJSON(data); if the dataType is not specified as json uncomment this
                // do what ever you want with the server response
                console.log("success datastring sent");
                if(data["saved"]=="registered"){
                  window.location.reload();
                }
                else{
                  var warning= "<h4>This username was already taken, try another one!<h4>"
                  $(warning).insertAfter("#notMatch")
                }

            },
            error: function() {
                //alert('error handing here');
            }
        });
      }
     
    });


    $( "#logout" ).submit(function( e ) {
      console.log("logout clicked");
      e.preventDefault();
      var request = $.ajax({
        url: "logout/",
        method: "GET",
      });
      request.done(function( msg ) {
        $( ".row" ).fadeOut( "slow" );
        $( "#tabs" ).show();
        console.log("logout happened");
      });
    });


});


	