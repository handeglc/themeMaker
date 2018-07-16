
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


    $('.lock-icon').on('click', function () {
      console.log("should be locked");
      $(this)
        .find('[data-fa-i2svg]')
        .toggleClass('fa-lock-open')
        .toggleClass('fa-lock');
    });

    $('.fa-times').on('click', function () {
      console.log("carping"); 
      var the = $(this);
      var chil = the.parentsUntil(".groups_checkbox").parent();

      var index = the.attr("color-id");
      console.log("index: "+index);
      var nearest = chil.parent().children().eq(2).children().eq(index);
      console.log(nearest.val());
      nearest.addClass("deleted");
      nearest.fadeOut();

      chil.children().eq(index*2+1).addClass("deleted");
      chil.children().eq(index*2).addClass("deleted");

      chil.children().eq(index*2+1).fadeOut();
      chil.children().eq(index*2).fadeOut();
            /*var el = nearest.val()
      console.log(el);
      var elem = $(".colors").eq(index);
      console.log(elem.val());*/
    });

    
});

    

   
