const username = $("#username")[0].textContent;
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.extend({
    el: function(el, props){
        var $el = $(document.createElement(el));
        $el.attr(props);
        return $el;
    }
});
const csrftoken = getCookie('csrftoken');

$("#btn-follow").click(function(){
    console.log("Clicked");
    var follow_status =  $("#btn-follow").html();
    if (follow_status === "Follow"){
        follow_api("Follow");
    }else{
        follow_api("Unfollow");
    }
    

});

function follow_api(follow_req){
    if (follow_req==="Follow"){
        var method = "POST";
    }else{
        var method = "DELETE";
    }
    console.log(method);
    $.ajax({
        url: "/api/v1/follow/",
        method: method,
        headers: {
            "Accept": "application/json",
            "X-CSRFToken": csrftoken,
        },
        data: {
            "follower_username":$("#profile_username")[0].textContent,
        },
        success: function(data){
            if(method==="POST"){
                $("#btn-follow").removeClass("btn-outline-primary").addClass("btn-primary").html("Unfollow");
            }else if(method==="DELETE"){
                $("#btn-follow").removeClass("btn-primary").addClass("btn-outline-primary").html("Follow");
            }
        }, 
        failure: function(data){
            
        },
        error:function(data){
            console.log("Implement this shit first");
        },
    })
}