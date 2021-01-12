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
        console.log("ok")
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

        if($(status_id).attr("status") === "not-shared"){
          num_shares = parseInt(num_shares,10)+1;
          $.ajax({
            type: 'POST',
            url: '/profile',
            data:{
              num_shares:num_shares,
              update_id:update_id,
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
        var update_id_id = '#'+($(this).attr("update_id"));
        var update_id_main = '#'+update_id+'-main';
        var preliked = $(this).attr("preliked");;
        var like_switch = '#like-switch'+update_id;
        var unlike_switch = '#unlike-switch'+update_id;

        if($(this).attr("status") === "liked"){

            if(preliked == "1"){
              num_likes = parseInt(num_likes,10)-1;
              $.ajax({
                type: 'POST',
                url: '/profile',
                data:{
                  num_likes:num_likes,
                  update_id:update_id,
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success:function(){
                  $(update_id_id).text(num_likes);
                  $(like_switch).attr("preliked","1");
                  $(unlike_switch).attr("preliked","1");
                }
              });
            };
            if (preliked == "0") {
              $.ajax({
                type: 'POST',
                url: '/profile',
                data:{
                  num_likes:num_likes,
                  update_id:update_id,
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success:function(){
                  $(update_id_id).text(num_likes);
                  $(like_switch).attr("preliked","0");
                  $(unlike_switch).attr("preliked","0");
                }
              });
            };

          $(this).attr("status","unliked");
          $(update_id_main).removeClass("active");

        }//function to unlike


        else if($(this).attr("status") === "unliked"){

          if (preliked === "1"){
            $.ajax({
              type: 'POST',
              url: '/profile',
              data:{
                num_likes:num_likes,
                update_id:update_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success:function(){
                $(update_id_id).text(num_likes);
                $(like_switch).attr("preliked","1");
                $(unlike_switch).attr("preliked","1");
              }
            });
          };
          if (preliked === "0"){
              num_likes = parseInt(num_likes,10)+1;
              $.ajax({
                type: 'POST',
                url: '/profile',
                data:{
                  num_likes:num_likes,
                  update_id:update_id,
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success:function(){
                  $(update_id_id).text(num_likes);
                  $(like_switch).attr("preliked","0");
                  $(unlike_switch).attr("preliked","0");
                }
              });
          };

          $(this).attr("status","liked");
          $(update_id_main).addClass("active");

        };//function to like
    });

    //  ============= LIKER POPUP FUNCTION =========

    $(".likers").on("click", function(){
        var update_id = $(this).attr("update_id")
        var num_likes = $(this).attr("likes")
        $.ajax({
          type: 'POST',
          url: '/profile',
          data:{
            update_id :$(this).attr("update_id"),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success:function(){
            $.ajax({
              type: 'GET',
              url: '/profile',
              data: {
                update_id:update_id,
                num_likes:num_likes
              },
              success:function(data){
                $('#likers').html(data);
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
        $.ajax({
          type: 'POST',
          url: '/profile',
          data:{
            update_id :$(this).attr("update_id"),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success:function(){
            $.ajax({
              type: 'GET',
              url: '/profile',
              data: {
                update_id:update_id,
                num_shares:num_shares
              },
              success:function(data){
                $('#sharer').html(data);
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
        $.ajax({
          type: 'POST',
          url: '/profile',
          data:{
            album_id :$(this).attr("id"),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success:function(){
            $.ajax({
              type: 'GET',
              url: '/profile',
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
