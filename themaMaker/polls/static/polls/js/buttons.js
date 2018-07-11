$(document).ready(function() {
  
    console.log( "recommending stayla" );
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

     $( ".fa-question-circle" ).tooltip({
      hide: {
        effect: "slideDown",
        delay: 250
      }
      });

    var $loading = $('#loadingDiv').hide();
    $(document)
      .ajaxStart(function () {
        $loading.show();
      })
      .ajaxStop(function () {
        $loading.hide();
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
        if(buttonpressed=="Recommend colors for me!"){
          var datastring = $(this).serialize();
          var locked= []
          var checkbox = $(this).children(".groups_checkbox");
          checkbox.children().each(function( i ) {
            if ( $(this).children().hasClass("fa-lock" )) {
              locked.push($(this).attr("color-id"))
            }
          });
          var locked_serialized = JSON.stringify(locked);
          console.log(locked);
          console.log(locked_serialized);
          console.log(datastring);

          if (locked.length != 0){
            which_op = "locked_recom";
          }else{
            which_op = "just_recom";
          }
          

          $.ajax({
              type: "POST",
              url: "recommend/",
              data: {"datas":datastring,"locked": locked_serialized, "which": which_op},
              dataType: "json",
              headers: { "X-CSRFToken": getCookie("csrftoken") },
              success: function(data) {
                  //var obj = jQuery.parseJSON(data); if the dataType is not specified as json uncomment this
                  // do what ever you want with the server response
                  console.log("success datastring sent-recom");
                  $("#recommendations").removeAttr('hidden');
                  $( ".recommended" ).remove();
                  for (var i = 0; i < data.color_list.length; i++) {

                    console.log("in for")
                    var html1 = '<div class="colors recommended" style="background-color:'+ data.color_list[i] +'">'
                    var html = '<input class="colors recommended" type="color" name="favcolor" value="'+data.color_list[i]+'">'
                    $( "#recommendations" ).append( html ); //"<p>"+data.color_list[i]+"</p>"
                  }
                  console.log(data)
              },
              error: function(e) {
                  //alert('error handing here');
                  console.log("error");
              }
          });
        }
      });


});