$(window).on("load", function() {
  "use strict";

  //  ============= Transfer POPUP FUNCTION =========

  //
  // $(document).ready(function(){
  //   $("button").click(function(){
  //     alert($("#butt").attr("value"));
  //     $.ajax({
  //       type: 'POST',
  //       url: '/signup_two',
  //       data:{
  //         albumid:$("#butt").attr("value"),
  //         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
  //       },
  //       success:function(){
  //         alert("gone");
  //       }
  //     });
  //   });
  // });





  //  ============= FOLLOWING POPUP FUNCTION =========

  $("#following-popup").on("click", function(){

    var url = '/'+($(".wrapper").attr("type"));



    $.ajax({
      type: 'GET',
      url: url,
      data: {
        type:"followings",
      },
      success:function(data){

        $('#load-followings').html(data);

        $(".suggestion-usd").on("click", function(f){

            if( $(f.target).attr("class") != "la la-plus" && $(f.target).attr("class") != "la la-minus" ){
                window.location = "//127.0.0.1:8000/"+($(this).attr("href"));
            }
            return false;
        });

        //  ============= FOLLOW-UNFOLLOW FUNCTION =========

        $(".la.la-plus").on("click",function(){

            var un_followed_email = $(this).attr("followed-email");
            var id = "#"+$(this).attr("id");
            var type = $(this).attr("type");
            var num_followings = $("#following-popup").attr("num");

            if( $(id).attr("class") === "la la-plus"){

            $.ajax({
                    type: 'POST',
                    url: url,
                    data:{
                      followed_email:un_followed_email,
                      type:type,
                      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success:function(){

                        num_followings = parseInt(num_followings,10)+1;
                        $(id).removeClass("la-plus").addClass("la-minus");
                        if($(".wrapper").attr("visit") != "true"){

                        $("#following-popup").text(num_followings);
                        $("#following-popup").attr("num",num_followings);
                      }

                    }

                  });

                }

                else if( $(id).attr("class") === "la la-minus"){

                $.ajax({
                        type: 'POST',
                        url: url,
                        data:{
                          un_followed_email:un_followed_email,
                          type:type,
                          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        },
                        success:function(){

                            num_followings = parseInt(num_followings,10)-1;
                            $(id).removeClass("la-minus").addClass("la-plus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);
                          }
                        }

                      });

                    };

        });


        //  ============= UNFOLLOW-FOLLOW FUNCTION =========

        $(".la.la-minus").on("click",function(){

          var followed_email = $(this).attr("followed-email");
          var id = "#"+$(this).attr("id");
          var div_id = "#div-"+$(this).attr("id");
          var type = $(this).attr("type");
          var num_followings = $("#following-popup").attr("num");

          if( $(id).attr("class") === "la la-minus"){
            $.ajax({
                    type: 'POST',
                    url: url,
                    data:{
                      un_followed_email:followed_email,
                      type:type,
                      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success:function(){
                      num_followings = parseInt(num_followings,10)-1;

                      if($(".wrapper").attr("visit") != "true"){
                        $(div_id).fadeOut("slow");
                        $("#following-popup").text(num_followings);
                        $("#following-popup").attr("num",num_followings);
                      }
                      else{
                        $(id).removeClass("la-minus");
                        $(id).addClass("la-plus");
                      }

                    }
            });
          }
          else if( $(id).attr("class") === "la la-plus"){
            $.ajax({
                    type: 'POST',
                    url: url,
                    data:{
                      followed_email:followed_email,
                      type:type,
                      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success:function(){
                      num_followings = parseInt(num_followings,10)+1;
                      $(id).removeClass("la-plus");
                      $(id).addClass("la-minus");
                      if($(".wrapper").attr("visit") != "true"){

                      $("#following-popup").text(num_followings);
                      $("#following-popup").attr("num",num_followings);
                    }


                    }
            });

          };

        });

      }


    });

    $(".following-popup.pst-pj").addClass("active");
    $(".wrapper").addClass("overlay");
    return false;

  });

  $(".following-box > a").on("click", function(){
      $(".following-popup.pst-pj").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= FOLLOWER POPUP FUNCTION =========

  $("#follower-popup").on("click", function(){

    var url = '/'+($(".wrapper").attr("type"));


      $.ajax({
        type: 'GET',
        url: url,
        data: {
          type:"followers",
        },
        success:function(data){
          $('#load-followers').html(data);

          $(".suggestion-usd").on("click", function(f){

              if( $(f.target).attr("class") != "la la-plus" && $(f.target).attr("class") != "la la-minus" ){
                window.location = "//127.0.0.1:8000/"+($(this).attr("href"));
              }
              return false;
          });

              //  ============= FOLLOW-UNFOLLOW FUNCTION =========

              $(".la.la-plus").on("click",function(){

                  var un_followed_email = $(this).attr("followed-email");
                  var id = "#"+$(this).attr("id");
                  var type = $(this).attr("type");
                  var num_followings = $("#following-popup").attr("num");

                  if( $(id).attr("class") === "la la-plus"){

                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            followed_email:un_followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){

                              num_followings = parseInt(num_followings,10)+1;
                              $(id).removeClass("la-plus").addClass("la-minus");
                              if($(".wrapper").attr("visit") != "true"){

                              $("#following-popup").text(num_followings);
                              $("#following-popup").attr("num",num_followings);
                            }

                          }

                        });

                      }

                      else if( $(id).attr("class") === "la la-minus"){

                      $.ajax({
                              type: 'POST',
                              url: url,
                              data:{
                                un_followed_email:un_followed_email,
                                type:type,
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                              },
                              success:function(){

                                  num_followings = parseInt(num_followings,10)-1;
                                  $(id).removeClass("la-minus").addClass("la-plus");
                                  if($(".wrapper").attr("visit") != "true"){

                                  $("#following-popup").text(num_followings);
                                  $("#following-popup").attr("num",num_followings);
                                }
                              }

                            });

                          };

              });

              //  ============= UNFOLLOW-FOLLOW FUNCTION =========

              $(".la.la-minus").on("click",function(){

                var followed_email = $(this).attr("followed-email");
                var id = "#"+$(this).attr("id");
                var div_id = "#div-"+$(this).attr("id");
                var type = $(this).attr("type");
                var num_followings = $("#following-popup").attr("num");

                if( $(id).attr("class") === "la la-minus"){
                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            un_followed_email:followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){
                            num_followings = parseInt(num_followings,10)-1;
                            $(id).removeClass("la-minus");
                            $(id).addClass("la-plus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);
                          }

                          }
                  });
                }
                else if( $(id).attr("class") === "la la-plus"){
                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            followed_email:followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){
                            num_followings = parseInt(num_followings,10)+1;
                            $(id).removeClass("la-plus");
                            $(id).addClass("la-minus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);
                          }


                          }
                  });

                };

              });


        }
      });

      $(".follower-popup.pst-pj").addClass("active");
      $(".wrapper").addClass("overlay");
      return false;
  });

  $(".follower-box > a").on("click", function(){
      $(".follower-popup.pst-pj").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= SHARE FUNCTION =========

  $(".la.la-share").on("click",function(){
      var num_shares = $(this).attr("shares");
      var update_id = $(this).attr("update_id");
      var status_id = '#share'+update_id
      var not_status_id = '#not-share'+update_id
      var album_id = $(this).attr("album_id")

      var url = '/'+($(".wrapper").attr("type"));


      if($(status_id).attr("status") === "not-shared"){
        num_shares = parseInt(num_shares,10)+1;
        $.ajax({
          type: 'POST',
          url: url,
          data:{
            num_shares:num_shares,
            update_id:update_id,
            album_id:album_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success:function(){
            $(status_id).text("Shares "+num_shares);
            $(status_id).attr("status","shared");

          }
        });
      }
    else{
        alert("You have already shared this status")
      };
  });


  //  ============= LIKE-UNLIKE FUNCTION =========

  $(".like-button").on("click",function(){
      var num_likes = $(this).attr("likes");
      var update_id = $(this).attr("update_id");
      var shared = $(".job_descp").attr("shared");

      if(shared == 'true'){
        var share_update_id_id = '#share-'+($(this).attr("update_id"));
        var share_update_id_main = '#share-'+update_id+'-main';
        var share_like_switch = '#share-like-switch'+update_id;
        var share_unlike_switch = '#share-unlike-switch'+update_id;
      }

      var update_id_id = '#'+($(this).attr("update_id"));
      var update_id_main = '#'+update_id+'-main';
      var like_switch = '#like-switch'+update_id;
      var unlike_switch = '#unlike-switch'+update_id;


      var preliked = $(this).attr("preliked");;

      var album_id = $(this).attr("album_id")

      var url = '/'+($(".wrapper").attr("type"));

      if($(this).attr("status") === "liked"){

          if(preliked == "1"){
            num_likes = parseInt(num_likes,10)-1;
            $.ajax({
              type: 'POST',
              url: url,
              data:{
                num_likes:num_likes,
                update_id:update_id,
                album_id : album_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){
                $(update_id_id).text(num_likes);
                $(like_switch).attr("preliked","1");
                $(unlike_switch).attr("preliked","1");
                if(shared == "true"){
                  $(share_update_id_id).text(num_likes);
                  $(share_like_switch).attr("preliked","1");
                  $(share_unlike_switch).attr("preliked","1");
                }
              }
            });
          };
          if (preliked == "0") {
            $.ajax({
              type: 'POST',
              url: url,
              data:{
                num_likes:num_likes,
                update_id:update_id,
                album_id : album_id,

                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){
                $(update_id_id).text(num_likes);
                $(like_switch).attr("preliked","0");
                $(unlike_switch).attr("preliked","0");
                if(shared == "true"){
                  $(share_update_id_id).text(num_likes);
                  $(share_like_switch).attr("preliked","0");
                  $(share_unlike_switch).attr("preliked","0");
                }
              }
            });
          };


          var final_id = "#"+($(this).attr("id"));

          if(final_id == like_switch){
            $(like_switch).attr("status","unliked");
            $(update_id_main).removeClass("active");
            if(shared == "true"){
              $(share_like_switch).attr("status","unliked");
              $(share_update_id_main).removeClass("active");
            }
          }
          if(final_id == unlike_switch){
            $(unlike_switch).attr("status","unliked");
            $(update_id_main).removeClass("active");
            if(shared == "true"){
              $(share_unlike_switch).attr("status","unliked");
              $(share_update_id_main).removeClass("active");
            }
          }
          if(final_id == share_like_switch){
            $(like_switch).attr("status","unliked");
            $(update_id_main).removeClass("active");
            $(share_like_switch).attr("status","unliked");
            $(share_update_id_main).removeClass("active");
          }
          if(final_id == share_unlike_switch){
            $(unlike_switch).attr("status","unliked");
            $(update_id_main).removeClass("active");
            $(share_unlike_switch).attr("status","unliked");
            $(share_update_id_main).removeClass("active");
          }



        // $(this).attr("status","unliked");
        // $(update_id_main).removeClass("active");
        // var final_id = ($(this).attr("id"));
        // alert(final_id);
        // alert(like_switch);
        // alert(unlike_switch);
        // alert(share_like_switch);
        // alert(share_unlike_switch);
        //
        // if(shared == "true"){
        //   alert($(this).attr("id"));
        //   $(id).attr("status","unliked");
        //   $(share_update_id_main).removeClass("active");
        // }

      }//function to unlike


      else if($(this).attr("status") === "unliked"){

        if (preliked === "1"){
          $.ajax({
            type: 'POST',
            url: url,
            data:{
              num_likes:num_likes,
              update_id:update_id,
              album_id : album_id,

              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(){
              $(update_id_id).text(num_likes);
              $(like_switch).attr("preliked","1");
              $(unlike_switch).attr("preliked","1");
              if(shared == "true"){
                $(share_update_id_id).text(num_likes);
                $(share_like_switch).attr("preliked","1");
                $(share_unlike_switch).attr("preliked","1");
              }
            }
          });
        };
        if (preliked === "0"){
            num_likes = parseInt(num_likes,10)+1;
            $.ajax({
              type: 'POST',
              url: url,
              data:{
                num_likes:num_likes,
                update_id:update_id,
                album_id : album_id,

                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){
                $(update_id_id).text(num_likes);
                $(like_switch).attr("preliked","0");
                $(unlike_switch).attr("preliked","0");
                if(shared == "true"){
                  $(share_update_id_id).text(num_likes);
                  $(share_like_switch).attr("preliked","0");
                  $(share_unlike_switch).attr("preliked","0");
                }
              }
            });
        };


        var final_id = "#"+($(this).attr("id"));

        if(final_id == like_switch){
          $(like_switch).attr("status","liked");
          $(update_id_main).addClass("active");
          if(shared == "true"){
            $(share_like_switch).attr("status","liked");
            $(share_update_id_main).addClass("active");
          }
        }
        if(final_id == unlike_switch){
          $(unlike_switch).attr("status","liked");
          $(update_id_main).addClass("active");
          if(shared == "true"){
            $(share_unlike_switch).attr("status","liked");
            $(share_update_id_main).addClass("active");
          }
        }
        if(final_id == share_like_switch){
          $(like_switch).attr("status","liked");
          $(update_id_main).addClass("active");
          $(share_like_switch).attr("status","liked");
          $(share_update_id_main).addClass("active");
        }
        if(final_id == share_unlike_switch){
          $(unlike_switch).attr("status","liked");
          $(update_id_main).addClass("active");
          $(share_unlike_switch).attr("status","liked");
          $(share_update_id_main).addClass("active");
        }
        //
        // alert(final_id);
        // alert(like_switch);
        // alert(unlike_switch);
        // alert(share_like_switch);
        // alert(share_unlike_switch);


      };//function to like
  });

  //  ============= LIKER POPUP FUNCTION =========

  $(".likers").on("click", function(){
      var update_id = $(this).attr("update_id")
      var num_likes = $(this).attr("likes")
      var album_id = $(this).attr("album_id")

      var url = '/'+($(".wrapper").attr("type"));


      $.ajax({
        type: 'POST',
        url: url,
        data:{
          update_id :$(this).attr("update_id"),
          album_id : album_id,

          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
          $.ajax({
            type: 'GET',
            url: url,
            data: {
              update_id:update_id,
              album_id : album_id,

              num_likes:num_likes
            },
            success:function(data){
              $('#likers').html(data);

              $(".suggestion-usd").on("click", function(f){

                  if( $(f.target).attr("class") != "la la-plus" && $(f.target).attr("class") != "la la-minus" ){
                    window.location = "//127.0.0.1:8000/"+($(this).attr("href"));
                  }
                  return false;
              });

              //  ============= FOLLOW-UNFOLLOW FUNCTION =========

              $(".la.la-plus").on("click",function(){

                  var un_followed_email = $(this).attr("followed-email");
                  var id = "#"+$(this).attr("id");
                  var type = $(this).attr("type");
                  var num_followings = $("#following-popup").attr("num");

                  if( $(id).attr("class") === "la la-plus"){

                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            followed_email:un_followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){

                              num_followings = parseInt(num_followings,10)+1;
                              $(id).removeClass("la-plus").addClass("la-minus");
                              if($(".wrapper").attr("visit") != "true"){

                              $("#following-popup").text(num_followings);
                              $("#following-popup").attr("num",num_followings);
                            }

                          }

                        });

                      }

                      else if( $(id).attr("class") === "la la-minus"){

                      $.ajax({
                              type: 'POST',
                              url: url,
                              data:{
                                un_followed_email:un_followed_email,
                                type:type,
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                              },
                              success:function(){

                                  num_followings = parseInt(num_followings,10)-1;
                                  $(id).removeClass("la-minus").addClass("la-plus");
                                  if($(".wrapper").attr("visit") != "true"){

                                  $("#following-popup").text(num_followings);
                                  $("#following-popup").attr("num",num_followings);
                                }
                              }

                            });

                          };

              });

              //  ============= UNFOLLOW-FOLLOW FUNCTION =========

              $(".la.la-minus").on("click",function(){

                var followed_email = $(this).attr("followed-email");
                var id = "#"+$(this).attr("id");
                var div_id = "#div-"+$(this).attr("id");
                var type = $(this).attr("type");
                var num_followings = $("#following-popup").attr("num");

                if( $(id).attr("class") === "la la-minus"){
                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            un_followed_email:followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){
                            num_followings = parseInt(num_followings,10)-1;
                            $(id).removeClass("la-minus");
                            $(id).addClass("la-plus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);
                          }
                          }
                  });
                }

                else if( $(id).attr("class") === "la la-plus"){

                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            followed_email:followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){
                            num_followings = parseInt(num_followings,10)+1;
                            $(id).removeClass("la-plus");
                            $(id).addClass("la-minus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);

                          }
                          }

                  });

                };

              });

            }
          });
        }
      });
      $(".liker-popup.pst-pj").addClass("active");
      $(".wrapper").addClass("overlay");
      return false;
  });

  $(".liker-box > a").on("click", function(){
      $(".liker-popup.pst-pj").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });


  //  ============= SHARER POPUP FUNCTION =========

  $(".sharer").on("click", function(){
      var update_id = $(this).attr("update_id")
      var num_shares = $(this).attr("shares")

      var url = '/'+($(".wrapper").attr("type"));


      $.ajax({
        type: 'POST',
        url: url,
        data:{
          update_id :$(this).attr("update_id"),
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
          $.ajax({
            type: 'GET',
            url: url,
            data: {
              update_id:update_id,
              num_shares:num_shares
            },
            success:function(data){
              $('#sharer').html(data);

              $(".suggestion-usd").on("click", function(f){

                  if( $(f.target).attr("class") != "la la-plus" && $(f.target).attr("class") != "la la-minus" ){
                    window.location = "//127.0.0.1:8000/"+($(this).attr("href"));
                  }
                  return false;
              });

              //  ============= FOLLOW-UNFOLLOW FUNCTION =========

              $(".la.la-plus").on("click",function(){

                  var un_followed_email = $(this).attr("followed-email");
                  var id = "#"+$(this).attr("id");
                  var type = $(this).attr("type");
                  var num_followings = $("#following-popup").attr("num");

                  if( $(id).attr("class") === "la la-plus"){

                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            followed_email:un_followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){

                              num_followings = parseInt(num_followings,10)+1;
                              $(id).removeClass("la-plus").addClass("la-minus");
                              if($(".wrapper").attr("visit") != "true"){

                              $("#following-popup").text(num_followings);
                              $("#following-popup").attr("num",num_followings);
                            }

                          }

                        });

                      }

                      else if( $(id).attr("class") === "la la-minus"){

                      $.ajax({
                              type: 'POST',
                              url: url,
                              data:{
                                un_followed_email:un_followed_email,
                                type:type,
                                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                              },
                              success:function(){

                                  num_followings = parseInt(num_followings,10)-1;
                                  $(id).removeClass("la-minus").addClass("la-plus");

                                  if($(".wrapper").attr("visit") != "true"){

                                  $("#following-popup").text(num_followings);
                                  $("#following-popup").attr("num",num_followings);

                                }
                              }

                            });

                          };

              });

              //  ============= UNFOLLOW-FOLLOW FUNCTION =========

              $(".la.la-minus").on("click",function(){

                var followed_email = $(this).attr("followed-email");
                var id = "#"+$(this).attr("id");
                var div_id = "#div-"+$(this).attr("id");
                var type = $(this).attr("type");
                var num_followings = $("#following-popup").attr("num");

                if( $(id).attr("class") === "la la-minus"){
                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            un_followed_email:followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){
                            num_followings = parseInt(num_followings,10)-1;
                            $(id).removeClass("la-minus");
                            $(id).addClass("la-plus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);
                          }

                          }
                  });
                }
                else if( $(id).attr("class") === "la la-plus"){
                  $.ajax({
                          type: 'POST',
                          url: url,
                          data:{
                            followed_email:followed_email,
                            type:type,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                          },
                          success:function(){
                            num_followings = parseInt(num_followings,10)+1;
                            $(id).removeClass("la-plus");
                            $(id).addClass("la-minus");
                            if($(".wrapper").attr("visit") != "true"){

                            $("#following-popup").text(num_followings);
                            $("#following-popup").attr("num",num_followings);
                            }


                          }
                  });

                };

              });


            }
          });
        }
      });
      $(".sharer-popup.pst-pj").addClass("active");
      $(".wrapper").addClass("overlay");
      return false;
  });

  $(".liker-box > a").on("click", function(){
      $(".sharer-popup.pst-pj").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });


  //  ============= FOLLOW-UNFOLLOW FUNCTION =========

  $(".la.la-plus").on("click",function(){

      var un_followed_email = $(this).attr("followed-email");
      var id = "#"+$(this).attr("id");
      var type = $(this).attr("type");
      var num_followings = $("#following-popup").attr("num");

      var url = '/'+($(".wrapper").attr("type"));


      if( $(id).attr("class") === "la la-plus"){

      $.ajax({
              type: 'POST',
              url: url,
              data:{
                followed_email:un_followed_email,
                type:type,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){

                  num_followings = parseInt(num_followings,10)+1;
                  $(id).removeClass("la-plus").addClass("la-minus");
                  if($(".wrapper").attr("visit") != "true"){
                    $("#following-popup").text(num_followings);
                    $("#following-popup").attr("num",num_followings);
                  }


              }

            });

          }

          else if( $(id).attr("class") === "la la-minus"){

          $.ajax({
                  type: 'POST',
                  url: url ,
                  data:{
                    un_followed_email:un_followed_email,
                    type:type,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                  },
                  success:function(){

                      num_followings = parseInt(num_followings,10)-1;
                      $(id).removeClass("la-minus").addClass("la-plus");
                      if($(".wrapper").attr("visit") != "true"){

                      $("#following-popup").text(num_followings);
                      $("#following-popup").attr("num",num_followings);
                    }
                  }

                });

              };

        });


  //  ============= MAIN FOLLOW FUNCTION =========

  $(".flww.active").on("click",function(e){

      var followed_email = $(this).attr("followed-email");
      var type = $(this).attr("type");
      var followers = $(this).attr("num");

      var url = '/'+($(".wrapper").attr("type"));

      if( $("#follow").attr("class") === "flww active"){

      followers = parseInt(followers,10)+1;

      $.ajax({
              type: 'POST',
              url: url,
              data:{
                followed_email:followed_email,
                type:type,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){

                  $("#follow").removeClass("active");
                  $("#flww-icon").removeClass("la-plus").addClass("la-minus");
                  $("#flww-text").text(" Unfollow");
                  $("#follower-popup").text(followers);
                  location.reload(true);


              }

            });

          }

      if( $("#follow").attr("class") === "flww"){

      $.ajax({
              type: 'POST',
              url: url,
              data:{
                un_followed_email:followed_email,
                type:type,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){

                  $("#follow").addClass("active");
                  $("#flww-icon").removeClass("la-minus").addClass("la-plus");
                  $("#flww-text").text(" Follow");
                  $("#follower-popup").text(followers);
                  location.reload(true);


              }

            });

          };


  });

  $(".flww").on("click",function(f){

      var un_followed_email = $(this).attr("followed-email");
      var type = $(this).attr("type");
      var followers = $(this).attr("num");

      var url = '/'+($(".wrapper").attr("type"));

      if( $("#follow").attr("class") === "flww active"){

      $.ajax({
              type: 'POST',
              url: url,
              data:{
                followed_email:un_followed_email,
                type:type,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){

                  $("#follow").removeClass("active");
                  $("#flww-icon").removeClass("la-plus").addClass("la-minus");
                  $("#flww-text").text(" Unfollow");
                  $("#follower-popup").text(followers);
                  location.reload(true);

                  // $("#following-popup").attr("num",num_followings);

              }

            });

          }

      if( $("#follow").attr("class") === "flww"){

      followers = parseInt(followers,10)-1;

      $.ajax({
              type: 'POST',
              url: url,
              data:{
                un_followed_email:un_followed_email,
                type:type,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){

                  $("#follow").addClass("active");
                  $("#flww-icon").removeClass("la-minus").addClass("la-plus");
                  $("#flww-text").text(" Follow");
                  $("#follower-popup").text(followers);
                  location.reload(true);


              }

            });

          };


  });

  //  ============= VISIT FUNCTION =========

  $(".suggestion-usd").on("click", function(f){

      if( $(f.target).attr("class") != "la la-plus" && $(f.target).attr("class") != "la la-minus" ){
          window.location = "//127.0.0.1:8000/"+($(this).attr("href"));
      };
      return false;
  });

  //  ============= POST PROJECT POPUP FUNCTION =========

  $(".post_project").on("click", function(){
      $(".post-popup.pst-pj").addClass("active");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".post-project > a").on("click", function(){
      $(".post-popup.pst-pj").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });

     //  ============= POST IMG POPUP FUNCTION =========

     $(".post_img").on("click", function(){
      $(".post-popup.image").addClass("active");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".post-project > a").on("click", function(){
      $(".post-popup.image").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= POST JOB POPUP FUNCTION =========

  $(".post-jb").on("click", function(){
      $(".post-popup.job_post").addClass("active");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".post-project > a").on("click", function(){
      $(".post-popup.job_post").removeClass("active");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= SIGNIN CONTROL FUNCTION =========

  $('.sign-control li').on("click", function(){
      var tab_id = $(this).attr('data-tab');
      $('.sign-control li').removeClass('current');
      $('.sign_in_sec').removeClass('current');
      $(this).addClass('current animated fadeIn');
      $("#"+tab_id).addClass('current animated fadeIn');
      return false;
  });

  //  ============= SIGNIN TAB FUNCTIONALITY =========

  $('.signup-tab ul li').on("click", function(){
      var tab_id = $(this).attr('data-tab');
      $('.signup-tab ul li').removeClass('current');
      $('.dff-tab').removeClass('current');
      $(this).addClass('current animated fadeIn');
      $("#"+tab_id).addClass('current animated fadeIn');
      return false;
  });

  //  ============= SIGNIN SWITCH TAB FUNCTIONALITY =========

  $('.tab-feed ul li').on("click", function(){
      var tab_id = $(this).attr('data-tab');
      $('.tab-feed ul li').removeClass('active');
      $('.product-feed-tab').removeClass('current');
      $(this).addClass('active animated fadeIn');
      $("#"+tab_id).addClass('current animated fadeIn');
      return false;
  });

  //  ============= COVER GAP FUNCTION =========

  var gap = $(".container").offset().left;
  $(".cover-sec > a, .chatbox-list").css({
      "right": gap
  });

  //  ============= OVERVIEW EDIT FUNCTION =========

  $(".overview-open").on("click", function(){
      $("#overview-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#overview-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= OVERVIEW EDIT FUNCTION =========

  $(".overview-open").on("click", function(){
      $("#overview-box_2").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#overview-box_2").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= EXPERIENCE EDIT FUNCTION =========

  $(".exp-bx-open").on("click", function(){
      $("#experience-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#experience-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= EDUCATION EDIT FUNCTION =========

  $(".ed-box-open").on("click", function(){
      $("#education-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#education-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= LOCATION EDIT FUNCTION =========

  $(".lct-box-open").on("click", function(){
      $("#location-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#location-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= SKILLS EDIT FUNCTION =========

  $(".skills-open").on("click", function(){
      $("#skills-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#skills-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= ESTABLISH EDIT FUNCTION =========

  $(".esp-bx-open").on("click", function(){
      $("#establish-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#establish-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  ============= UPLOAD PIC FUNCTION =========

  $(".gallery_pt > a").on("click", function(){
      var album_id = $(this).attr("id")

      if($(".wrapper").attr("type")==="profile"){

        var url = '/profile'

      };

      if($(".wrapper").attr("type")==="page"){

        var url = '/page'

      };

      $.ajax({
        type: 'POST',
        url: url,
        data:{
          album_id :$(this).attr("id"),
          csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
          $.ajax({
            type: 'GET',
            url: url,
            data: {album_id:album_id},
            success:function(data){
              $('#checkers').html(data);
            }
          });
        }
      });
      $("#create-portfolio").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });

  $(".close-box").on("click", function(){
      $("#create-portfolio").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });


  //  ============= OPEN PIC FUNCTION =========

  $(".job_descp > img").on("click", function(){
      // alert("image_clicked");
      var caption = $(this).attr("caption");
      var img = $(this).attr("src");
      var update_id = $(this).attr("update_id");
      var model_id = "#modal-"+update_id;
      var model_img_id = "#img-"+update_id;
      var og_img = "#og-img-"+update_id;
      var close_id = "#close-"+update_id;

      $(model_id).css("display" , "block");
      // $(og_img).css("width" , "100px");
      // $(".job_descp > img").css("width" , "10px");
      $(model_img_id).attr("src",img);

      $(close_id).on("click", function(){
        $(model_id).css("display" , "none");
        $(og_img).css("width" , "2000px");
        // $(og_img).css("max-width" , "100%");

      });

  });


  //  ============= CREATE PORTFOLIO FUNCTION =========

  $("#album-add").on("click", function(){
      $("#create-portfolio-2").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#create-portfolio-2").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });



  //  ============= EMPLOYEE EDIT FUNCTION =========

  $(".emp-open").on("click", function(){
      $("#total-employes").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#total-employes").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });

  //  =============== Ask a Question Popup ============

  $(".ask-question").on("click", function(){
      $("#question-box").addClass("open");
      $(".wrapper").addClass("overlay");
      return false;
  });
  $(".close-box").on("click", function(){
      $("#question-box").removeClass("open");
      $(".wrapper").removeClass("overlay");
      return false;
  });


  //  ============== ChatBox ==============


  $(".chat-mg").on("click", function(){
      $(this).next(".conversation-box").toggleClass("active");
      return false;
  });
  $(".close-chat").on("click", function(){
      $(".conversation-box").removeClass("active");
      return false;
  });

  //  ================== Edit Options Function =================


  $(".ed-opts-open").on("click", function(){
      $(this).next(".ed-options").toggleClass("active");
      return false;
  });


  // ============== Menu Script =============

  $(".menu-btn > a").on("click", function(){
      $("nav").toggleClass("active");
      return false;
  });


  //  ============ Notifications Open =============

  $(".not-box-open").on("click", function(){
      $(this).next(".notification-box").toggleClass("active");
  });

  // ============= User Account Setting Open ===========

  $(".user-info").on("click", function(){
      $(this).next(".user-account-settingss").toggleClass("active");
  });

  //  ============= FORUM LINKS MOBILE MENU FUNCTION =========

  $(".forum-links-btn > a").on("click", function(){
      $(".forum-links").toggleClass("active");
      return false;
  });
  $("html").on("click", function(){
      $(".forum-links").removeClass("active");
  });
  $(".forum-links-btn > a, .forum-links").on("click", function(){
      e.stopPropagation();
  });

  //  ============= PORTFOLIO SLIDER FUNCTION =========

  $('.profiles-slider').slick({
      slidesToShow: 3,
      slck:true,
      slidesToScroll: 1,
      prevArrow:'<span class="slick-previous"></span>',
      nextArrow:'<span class="slick-nexti"></span>',
      autoplay: true,
      dots: false,
      autoplaySpeed: 2000,
      responsive: [
      {
        breakpoint: 1200,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          infinite: true,
          dots: false
        }
      },
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]


  });





});
