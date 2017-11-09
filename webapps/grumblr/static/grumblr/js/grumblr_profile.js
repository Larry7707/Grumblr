// var req;
// function show_comment() {
//     if (window.XMLHttpRequest) {
//         req = new XMLHttpRequest();
//     } else {
//         req = new ActiveXObject("Microsoft.XMLHTTP");
//     }
//     // console.log("run!");
//     req.onreadystatechange = handleResponse;
//     req.open("POST", "", true);
//     req.send(); 
// }

// function handleResponse() {
//     if (req.readyState != 4 || req.status != 200) {
//         return;
//     }

//   // Removes the old to-do list items
//   //   var k = document.getElementById("content");

//   //   var dic = JSON.parse(req.responseText);
//   //   var current = dic["fortune"];
//   //   var new_content = document.createElement("p");
//   //   var new_content = "<p id='content'>"+ current + "</p>";

//   //   k.innerHTML = current;
//   // console.log("yeah");
// }


// TODO List
var $j = jQuery.noConflict();
// var popolate_done = false
function populateList() {
    var id = $j(".profile-store-id").attr("id");
    console.log("now loading posts of user " + id);
    $j.get("/grumblr/get_profile_stream/" + id)
    .done(function(data) {
        console.log("populateList is running.");
        var list = $j("#post-list");
        console.log(list);
        list.data('max-time', data['max-time']);
        list.html('');
        // add posts
        for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];
            var new_post = $j(post.html); // new post html
            new_post.data("post-id", post.id);
            list.append(new_post);
            // add data for comment form
            var comment_btn = $j("#comment_btn_" + post.id);
            comment_btn.data("post-id", post.id);
            $j("#post_comment_" + post.id).data("post-id", post.id);
            // add comment for each post
            $j.get("/grumblr/get_comment/" + post.id)
            .done(function(comment_data) {
              var post_id = comment_data.post_id
              console.log("populate comments" + post_id);
              var comment_list = $j("#comments_" + post_id);
              comment_list.data("max-time", data["max-time"]);
              for (var i = 0; i < comment_data.comments.length; i++){
                comment = comment_data.comments[i];
                var new_comment = $j(comment.html);
                comment_list.append(new_comment);
              }
            });
        }
        // add event listener from id
        $j(".comment-form").on('submit', function(event) {
          event.preventDefault();
          console.log(event.target);
          var id = $j(event.target).data("post-id");
          console.log("now commenting post"+ id);

          var post_form = $j(event.target).serialize();
          $j.post("/grumblr/add_comment/" + id, post_form)
          .done(function(data) {
            console.log("Comment done.");
            var list = $j("#comments_" + id);
            list.append(data.html);
            $j(".comment").val("");
            // getUpdates();
          });
});
        // popolate_done = true
      }).fail(function() {
      console.log("Failed to populateList.")
    });
}



// function show_comment() {
//     var id = $j(e.target).parent().data("item-id");
//     if (typeof id != "number") 
//         return;
//     $j.post("/show_comment"+id).done(function(data) {
//         getUpdates();
//     });
// }

$j('#new-post').on('submit', function(event) {
  event.preventDefault();

  var post_form = $j("#new-post").serialize();
  $j.post("/grumblr/post", post_form)
  .done(function() {
    console.log("Post done.");
    getUpdates();
  });
});

// function deleteItem(e){
//     var id = $j(e.target).parent().data("item-id");
//     if (typeof id != "number") 
//         return;
//     $j.post("/shared-todo-list/delete-item/" + id)
//       .done(function(data) {
//           getUpdates();
//           $j("#item-field").val("").focus()
//       });
// }


// function getUpdates() {
//     var list = $j("#post-list");
//     var max_time = list.data("max-time");
//     $j.get("/grumblr/get_changes/"+ max_time)
//       .done(function(data) {
//           console.log("Updating changes...")
//           list.data('max-time', data['max-time']);
//           for (var i = 0; i < data.posts.length; i++) {
//               var post = data.posts[i];
//               console.log("found post: " + post.id)
//               if (post.deleted) {
//                   $j("#post_" + post.id).remove();
//               } else {
//                   var new_post = $j(post.html);
//                   new_post.data("post-id", post.id);
//                   // var comment_id=$j("");
//                   list.prepend(new_post);
//               }
//           }
//       });
// }
// dealing with the hustle problem 
$j(document).ready(function() {
  // Add event-handlers
  // $j("#post-btn").click(addPost);
  // $j("#item-field").keypress(function (e) { if (e.which == 13) addItem(); } );
  // $j("#todo-list").click(deleteItem);

  // Set up to-do list with initial DB items and DOM data
  console.log("Run populateList...");
  populateList(); //get all the objects in the database
  console.log("populateList done.");
  // $j("#item-field").focus();
  // Periodically refresh to-do list
  // window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $j.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
