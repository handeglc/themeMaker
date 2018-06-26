
$(document).ready(function() {
    console.log( "mrb" );
    $( ".colors" ).on( "click", function() {
        console.log( "clicked" );
        var html = '<fieldset> \
    <legend>Choose the color</legend> \
  \
      <div>\
          <input type="color" id="head" name="color"\
                 value="#e66465" />\
          <label for="head">Head</label>\
      </div>\
  </fieldset>'

    //$( html ).insertAfter( ".groups" );


      });



    });

    

   
