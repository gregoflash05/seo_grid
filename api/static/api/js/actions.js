
    $(document).ready(function(){
        var main_country = $("#index_country").val();
        $("#edit_campaign_country option:selected").html(main_country);
        var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        // $(this).siblings(".bidbutton")
        var all_keyword_ids = $(".all_keyword_ids");
        for(var i = 0; i < all_keyword_ids.length; i++){
            console.log($(all_keyword_ids[i]).val());
            var  k_id = $(all_keyword_ids[i]).val();
            var c_1 = $(all_keyword_ids[i]).siblings(".Competitor_1"+k_id);
            var c_2 = $(all_keyword_ids[i]).siblings(".Competitor_2"+k_id);
            // c_1.html('Pending...');
            // c_2.html('Pending...');


            $.ajax({
                type: "POST",
                url: window.location.protocol + "//" + window.location.host +"/top_2_competitors/" + k_id + "/",
                success: function(response) {
                    let json = null;
                    try {
                        json = JSON.parse(response); 
                    } catch (e) {
                        json = response;
                    }
                    console.log(json);
                    console.log(json.competitor_one + k_id);
                    console.log(json.competitor_two + k_id);
                    c_1.html(json.competitor_one + k_id);
                    c_2.html(json.competitor_two + k_id);
          console.log(response); 
                },
                error: function(response) {
             console.log(response);
                 }      
                        });


        }


        for(var i = 0; i < all_keyword_ids.length; i++){
            console.log($(all_keyword_ids[i]).val());
            var  k_id = $(all_keyword_ids[i]).val();
            var r_1 = $(all_keyword_ids[i]).siblings("#ranking"+k_id);
            var t_1 = $(all_keyword_ids[i]).siblings("#top_ranking"+k_id);
            // c_1.html('Pending...');
            // c_2.html('Pending...');


            $.ajax({
                type: "POST",
                url: window.location.protocol + "//" + window.location.host +"/get_rank/" + k_id + "/",
                success: function(response) {
                    let json = null;
                    try {
                        json = JSON.parse(response); 
                    } catch (e) {
                        json = response;
                    }
                    console.log(json);
                    console.log(json.ranking);
                    console.log(json.top_rank); 
                    r_1.html(json.ranking+k_id + "<span class='iconify' data-icon='" + json.rank_data_icon+k_id +"' data-inline='false'></span>");
                    t_1.html(json.top_rank+k_id);
          console.log(response); 
                },
                error: function(response) {
             console.log(response);
                 }      
                        });


        }



     $("#add_campaign_submit").click(function(event){
      event.preventDefault();
      var link = $("#add_campaign_websiteLink").val();
      var keyword = $("#add_campaign_keyword").val();
    //  var language = $("#language").val();
      var language = $("#add_campaign_language option:selected").html();
      var country =  $("#add_campaign_country option:selected").html();
      var campaign_name =  $("#add_campaign_campaignName").val();
      var submit =    $("#add_campaign_submit").val();
      //console.log(link + ' ' + keyword + ' ' + language + ' ' + country + ' ' + campaign_name);
          if(campaign_name==''){
            $("#campaignName").css({"background-color": "transparent", "border-color": "red"});
            $(".add_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Campaign Name is empty</p>");
    }else{
            $("#campaignName").css({"border-color": "green"});
                if(link==''){
                   $(".add_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Website link is empty</p>");
                  $("#websiteLink").css({"background-color": "transparent", "border-color": "red"});
    }else{
           $("#websiteLink").css({"border-color": "green"});     
           if(language==''){
                   $(".add_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Select language</p>");
                  $("#language").css({"background-color": "transparent", "border-color": "red"});
    }else{
           $("#language").css({"border-color": "green"});
           if(country==''){
                   $(".add_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Select country</p>");
                  $("#country").css({"background-color": "transparent", "border-color": "red"});
    }else{
           $("#country").css({"border-color": "green"});
           if(keyword==''){
                   $(".add_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Enter keyword</p>");
                  $("#keyword").css({"background-color": "transparent", "border-color": "red"});
    }else{
           $("#keyword").css({"border-color": "green"});
       $(".add_campaign_error_message").html("<p style='padding:7px' class='success-alert'>Please wait...</p>");
$.ajax({

    type: "POST",
    url: window.location.protocol + "//" + window.location.host +"/create_campaign/",
//    contentType: "application/json",
//    dataType: "json",
    data: {       csrfmiddlewaretoken: csrfmiddlewaretoken,
                  link : link,
                  keyword : keyword,
                  language : language,
                  country : country,
                  campaign_name : campaign_name,
                  submit : submit
    },
    success: function(response) {
$(".add_campaign_error_message").html(response);

        
    },
    error: function(response) {
 $(".add_campaign_error_message").html("<p class='error-alert' style='text-align:center;padding:7px'>An error occured<p>");
     }       

            
            });


    }
          }
      }
    }
    }


     });



     
     

     $("#edit_campaign_submit").click(function(event){
        event.preventDefault();
        var link = $("#edit_campaign_websiteLink").val();
      //  var language = $("#language").val();
        var language = $("#edit_campaign_language option:selected").html();
        var country =  $("#edit_campaign_country option:selected").html();
        var campaign_name =  $("#edit_campaign_campaignName").val();
        var cam_id =  $("#camp_main_id").val();
        var submit =    $("#edit_campaign_submit").val();
        console.log(link + ' ' + language + ' ' + country + ' ' + campaign_name + ' ' + cam_id);
            if(campaign_name==''){
              $("#campaignName").css({"background-color": "transparent", "border-color": "red"});
              $(".edit_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Campaign Name is empty</p>");
      }else{
              $("#campaignName").css({"border-color": "green"});
                  if(link==''){
                     $(".edit_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Website link is empty</p>");
                    $("#websiteLink").css({"background-color": "transparent", "border-color": "red"});
      }else{
             $("#websiteLink").css({"border-color": "green"});     
             if(language==''){
                     $(".edit_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Select language</p>");
                    $("#language").css({"background-color": "transparent", "border-color": "red"});
      }else{
             $("#language").css({"border-color": "green"});
             if(country==''){
                     $(".edit_campaign_error_message").html("<p style='' class='error-alert' style='padding:7px'>Select country</p>");
                    $("#country").css({"background-color": "transparent", "border-color": "red"});
      }else{
             $("#country").css({"border-color": "green"});
         $(".edit_campaign_error_message").html("<p style='padding:7px' class='success-alert'>Please wait...</p>");
  $.ajax({
  
      type: "PUT",
      url: window.location.protocol + "//" + window.location.host +"/edit_campaign/" + cam_id + "/",
  //    contentType: "application/json",
  //    dataType: "json",
      data: {       csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[1].value,
                    link : link,
                    language : language,
                    country : country,
                    campaign_name : campaign_name,
                    submit : submit
      },
      success: function(response) {
  $(".edit_campaign_error_message").html(response);
  
          
      },
      error: function(response) {
   $(".edit_campaign_error_message").html("<p class='error-alert' style='text-align:center;padding:7px'>An error occured<p>");
       }       
  
              
              });
  
  
            }
        }
      }
      }
  
  
       });  

       
       

       $("#delete_campaign_submit").click(function(event){
        event.preventDefault();
        var cam_id =  $("#camp_main_id").val();
           
         $(".edit_campaign_error_message").html("<p style='padding:7px' class='success-alert'>Please wait...</p>");
  $.ajax({
  
      type: "DELETE",
      url: window.location.protocol + "//" + window.location.host +"/edit_campaign/" + cam_id + "/",
  //    contentType: "application/json",
  //    dataType: "json",
      success: function(response) {
  $(".edit_campaign_error_message").html(response);
  
          
      },
      error: function(response) {
   $(".edit_campaign_error_message").html("<p class='error-alert' style='text-align:center;padding:7px'>Couldn't delete campaign<p>");
       }       
  
              
              });
  
  
  
  
       });  

       
       
       $("#add_keyword_submit").click(function(event){
        event.preventDefault();
        var keyword =  $("#keywordName").val();
        var campaign =  $("#camp_main_id").val();
        // console.log(keyword + ' ' + campaign);
            if(keyword ==''){
              $("#keywordName").css({"background-color": "transparent", "border-color": "red"});
              $(".add_keyword_error_message").html("<p style='' class='error-alert' style='padding:7px'>Enter keyword</p>");
      }else{
              $("#keywordName").css({"border-color": "green"});
         $(".add_keyword_error_message").html("<p style='padding:7px' class='success-alert'>Please wait...</p>");
  $.ajax({
  
      type: "POST",
      url: window.location.protocol + "//" + window.location.host +"/edit_keyword/",
  //    contentType: "application/json",
  //    dataType: "json",
      data: {       csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[1].value,
                    keyword : keyword,
                    campaign : campaign
      },
      success: function(response) {
  $(".add_keyword_error_message").html(response);
  
          
      },
      error: function(response) {
   $(".add_keyword_error_message").html("<p class='error-alert' style='text-align:center;padding:7px'>An error occured<p>");
       }       
  
              
              });
  

      }
  
  
       }); 



       
       $(".delete_a_keyword").click(function(event){
        event.preventDefault();
        
        // var keyword_id = $(".delete_a_keyword").attr("href");
        // var keyword_id = $(this).find("input")[0].val();
        var keyword_id = $(this).find("input").val();
        var campaign =  $("#camp_main_id").val();
        console.log(keyword_id + ' ' + campaign);
        $('.delete_a_keyword'). unbind('click');
        $("#confirm_keyword_delete_submit").one('click', function(e) {
            console.log(keyword_id + ' ' + campaign);
         $(".edit_campaign_error_message").html("<p style='padding:7px' class='success-alert'>Please wait...</p>");
  $.ajax({
  
      type: "DELETE",
      url: window.location.protocol + "//" + window.location.host +"/edit_keyword/" + keyword_id + "/",
  //    contentType: "application/json",
  //    dataType: "json",
  data: {           campaign : campaign
      },
      success: function(response) {
  $(".edit_campaign_error_message").html(response);
  
          
      },
      error: function(response) {
   $(".edit_campaign_error_message").html("<p class='error-alert' style='text-align:center;padding:7px'>Couldn't delete keyword<p>");
       }       
  
              
              });
  
  
  
});
       }); 



       

       $(".compare-btn").click(function(event){
        event.preventDefault();
        var response1;
        var response2;
        var keyword_id = $(this).find("input").val();
        $(this).html("Processing...");
        console.log(keyword_id);
        // $('.delete_a_keyword'). unbind('click');
        //  $(".edit_campaign_error_message").html("<p style='padding:7px' class='success-alert'>Please wait...</p>");
        var completed = 0;

///////////////////////////////////////////////////first///////////////////////////////////////////
        $.ajax({
            type: "POST",
            url: window.location.protocol + "//" + window.location.host +"/url_compare_title/" + keyword_id + "/",
            success: function(response) {
      console.log(response);
      completed = completed +1;
      console.log(completed);  
            },
            error: function(response) {
         console.log(response);
             }      
                    });
                    $.ajax({
                        type: "POST",
                        url: window.location.protocol + "//" + window.location.host +"/url_compare_responsive/" + keyword_id + "/",
                        success: function(response) {
                  console.log(response);
                  completed = completed +1;
                  console.log(completed);  
                        },
                        error: function(response) {
                     console.log(response);
                         }      
                                });
                                $.ajax({
                                    type: "POST",
                                    url: window.location.protocol + "//" + window.location.host +"/url_compare_sitemap/" + keyword_id + "/",
                                    success: function(response) {
                              console.log(response);
                              completed = completed +1;
                              console.log(completed);  
                                    },
                                    error: function(response) {
                                 console.log(response);
                                     }      
                                            });
                                            $.ajax({
                                                type: "POST",
                                                url: window.location.protocol + "//" + window.location.host +"/url_compare_ssl_status/" + keyword_id + "/",
                                                success: function(response) {
                                          console.log(response);
                                          completed = completed +1;
                                          console.log(completed);  
                                                },
                                                error: function(response) {
                                             console.log(response);
                                                 }      
                                                        });
                                                        $.ajax({
                                                            type: "POST",
                                                            url: window.location.protocol + "//" + window.location.host +"/url_compare_run_time/" + keyword_id + "/",
                                                            success: function(response) {
                                                      console.log(response);
                                                      completed = completed +1;
                                                      console.log(completed);  
                                                            },
                                                            error: function(response) {
                                                         console.log(response);
                                                             }      
                                                                    });
///////////////////////////////////////////////////End first///////////////////////////////////////////
///////////////////////////////////////////////////second///////////////////////////////////////////

            $.ajax({

                type: "POST",
                url: window.location.protocol + "//" + window.location.host +"/url_compare_competitor_title/" + keyword_id + "/",
                success: function(response) {
        console.log(response);
        completed = completed +1;
        console.log(completed);     
                },
                error: function(response) {
        console.log(response);
                }      
                        });
                        $.ajax({

                            type: "POST",
                            url: window.location.protocol + "//" + window.location.host +"/url_compare_competitorr_responsive/" + keyword_id + "/",
                            success: function(response) {
                    console.log(response);
                    completed = completed +1;
                    console.log(completed);     
                            },
                            error: function(response) {
                    console.log(response);
                            }      
                                    });
                                    $.ajax({

                                        type: "POST",
                                        url: window.location.protocol + "//" + window.location.host +"/url_compare_competitor_sitemap/" + keyword_id + "/",
                                        success: function(response) {
                                console.log(response);
                                completed = completed +1;
                                console.log(completed);     
                                        },
                                        error: function(response) {
                                console.log(response);
                                        }      
                                                });
                                                $.ajax({

                                                    type: "POST",
                                                    url: window.location.protocol + "//" + window.location.host +"/url_compare_competitor_ssl_status/" + keyword_id + "/",
                                                    success: function(response) {
                                            console.log(response);
                                            completed = completed +1;
                                            console.log(completed);     
                                                    },
                                                    error: function(response) {
                                            console.log(response);
                                                    }      
                                                            });
                                                            $.ajax({

                                                                type: "POST",
                                                                url: window.location.protocol + "//" + window.location.host +"/url_compare_competitor_run_time/" + keyword_id + "/",
                                                                success: function(response) {
                                                        console.log(response);
                                                        completed = completed +1;
                                                        console.log(completed);     
                                                                },
                                                                error: function(response) {
                                                        console.log(response);
                                                                }      
                                                                        });

 ///////////////////////////////////////////////////End second///////////////////////////////////////////
                        var request_interval = window.setInterval(function(){
                            if(completed == 10){
                                console.log("complete");
                                window.location.href = "../../compare/" + keyword_id + "/";
                                clearInterval(request_interval);
                            }else{
                                console.log("not yet"); 
                            }
                          }, 1000);
  
                        // $('.compare-btn'). unbind('click');

       });





    });
