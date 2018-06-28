
$(document).ready(function() {
    console.log( "mrb" );


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


    $('i').on('click', function () {
      console.log("should be locked");
      $(this)
        .find('[data-fa-i2svg]')
        .toggleClass('fa-lock-open')
        .toggleClass('fa-lock');
    });


    });

    

   
