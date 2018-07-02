
$(document).ready(function() {
  
    console.log( "mrb" );
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

    $("#sellectall").on("click", function(){
      console.log("selectall is cliked");
      //$("input:checkbox").attr('checked', true);
      $('.fa-lock-open').toggleClass('fa-lock');
    });

    $("#un-sellectall").on("click", function(){
      console.log("un-selectall is cliked");
      //$("input:checkbox").attr('checked', false);
      $('.fa-lock').toggleClass('fa-lock-open');
    });


    $('div i').on('click', function () {
      console.log("should be locked");
      $(this)
        .find('[data-fa-i2svg]')
        .toggleClass('fa-lock-open')
        .toggleClass('fa-lock');
    });

    
    $( ".fa-question-circle" ).tooltip({
      hide: {
        effect: "slideDown",
        delay: 250
      }
    });

    var buttonpressed; 
    $('.submit-form').click(function() { 
        buttonpressed = $(this).attr('value');
         
    });

    $('.color-picker').submit(function( e ) {
      console.log("submit clicked");
      
      e.preventDefault();

        if(buttonpressed=="I liked this color set!"){
          var datastring = $(this).serialize();
          console.log(datastring);
          $.ajax({
              type: "POST",
              url: "save/",
              data: {"datas":datastring},
              dataType: "json",
              headers: { "X-CSRFToken": getCookie("csrftoken") },
              success: function(data) {
                  //var obj = jQuery.parseJSON(data); if the dataType is not specified as json uncomment this
                  // do what ever you want with the server response
                  console.log("success datastring sent");
              },
              error: function() {
                  //alert('error handing here');
              }
          });
        }
      });


});

    

   
