
    $(document).ready(function(){
        var keyword_id = $("#keyword_id").val();

        $.ajax({
            type: "POST",
            url: window.location.protocol + "//" + window.location.host +"/ob_br_compare/" + keyword_id + "/",
            success: function(response) {
      console.log(response);
      console.log("Done");  
            },
            error: function(response) {
         console.log(response);
             }      
                    });
                    $.ajax({
                        type: "POST",
                        url: window.location.protocol + "//" + window.location.host +"/ob_br_compare_competitor/" + keyword_id + "/",
                        success: function(response) {
                  console.log(response);
                  console.log("done");  
                        },
                        error: function(response) {
                     console.log(response);
                         }      
                                });

                                
    });
