$.extend({
    el: function(el, props){
        var $el = $(document.createElement(el));
        $el.attr(props);
        return $el;
    }
});
 //Constants
 var usernameElmn = document.querySelector("#username");
 if (usernameElmn!=null){
    const username = usernameElmn.text;
 }
// Detect and create new tweet
$("#new_tweet_btn").on("click", ()=>{postTweet();});


//Add Tweet event handler
document.addEventListener('DOMContentLoaded', (event) => {
    getAllTweets();    
});

function onLoadPage(){
    console.log("Hi");
    $("#new_tweet_btn").click(function(){console.log("Clicked!");});
    // getAllTweets();
    

}
const csrftoken = getCookie('csrftoken');
function getAllTweets(){
    var form_control = document.querySelector(".form-group");
    var content = form_control.elements[0].value;
    getTweetPage(1)
    return false;
}
var current_page_count = 1
function getTweetPage(number){
    $.ajax({
        url: '/api/v1/tweets/',
        method: "GET",
        headers: {
            "Accept": "application/json",
            "X-CSRFToken": csrftoken,
        },
        data: {
            'page':number,
        },
        success: function(result){
            current_page_count = result[2];
            if (result["message"] != "User not found"){
                addTweetDOM(result[0], result[1]);
            }
            
        }, 
        failure: function(){

        }
    })
}

function setAttributes(el, attrs){
    for (var key in attrs){
        el.setAttribute(key, attrs[key])
    }
}

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


function postTweet(){
    var tweet_string = document.querySelector('textarea').value;
    if (tweet_string != ""){

        // With ajax
        $.ajax({
            url: "/api/v1/tweets/",
            method: "POST",
            headers: {
                    "Accept": "application/json",
                    "X-CSRFToken": csrftoken,
            },
            data: {
                'data': tweet_string.toString(),
            },
            success: function(data){
                // console.log("success");
                //Add tweet to the top of the tweets container
            //   console.log(data);
                var date = new Date(Date.now());
                var container =  $(".tweets-container");
                var display_tweet = $.el("div", {"class": "display-tweet"});
                var icon = $.el("span", {"class": "far fa-user fa-2x tweet-icon"});
                var tweet_content = $.el("div", {"class": "tweet-content"})
                                    .append($.el("div", {"class": "d-flex align-items-center bd-highlight mb-3 subheader-flex"})
                                        .append($.el("h6", {"style": "margin: 0px; padding:0px"}).text("You"))
                                        .append($.el("nobr", {}).append($.el("p", {"class": "no-borders tweet-date"}).html(data["data"]["datetime"]))));                                        
                   
                var tweet_txt = $.el("p", {}).text(tweet_string);
                tweet_content.append(tweet_txt);
                var icon_sec = $.el("div",{"class":"d-flex icons-section"})
                                .append($.el("i", {"class": "fas fa-heart"}))
                                .append($.el("p",{}).html("0"));
                //Coalesce everything into a single unit
                display_tweet.append(icon, tweet_content, icon_sec);
                display_tweet.hide().prependTo(".tweets-container").fadeIn(1000);
                $(".display-tweet").last().fadeOut()
                $(".tweets-container")
                $("textarea").val("");
                // console.log(display_tweet);
                                        
                // getAllTweets();
            },
            failure: function(data){
                console.log("failure");
                // console.log(data);
            },
        })
    }else{
        alert("Empty tweet not allowed")
    }
    
}

function addTweetDOM(tweets, liked_pk){
    var container = document.querySelector(".tweets-container");
    $(container).fadeOut().empty();
    var frag = document.createDocumentFragment();
    var i = 0;
    for (i; i<tweets.length; i++){
        // Big container where to put everything
        var tweet_cont = document.createElement('div');
        setAttributes(tweet_cont, {"class":"display-tweet"})

        // Username photo
        var user_photo = document.createElement('span');
        user_photo.setAttribute("class", "far fa-user fa-2x tweet-icon")
        // console.log(tweets[i]);
        // Username text and tweet content
        var name_date_container = document.createElement("div");
        name_date_container.setAttribute("class", "d-flex align-items-center bd-highlight mb-3 subheader-flex");
        var tweet_main = document.createElement('div');
        tweet_main.setAttribute("class", "tweet-content");

        var user_div = document.createElement('h6');
        var anchor = document.createElement('a');
        var nobr = document.createElement("nobr")
        anchor.setAttribute("class", "anchor"); anchor.setAttribute("href", 'profile_page/999'.replace(999, tweets[i].username));
        user_div.setAttribute("class", "no-borders tweet-user");
        user_div.textContent = tweets[i].username;
        anchor.appendChild(user_div);
        var date = document.createElement('p');
        date.setAttribute("class", "no-borders tweet-date"); 
        var date_mil = tweets[i].datetime;
        date.textContent = date_mil;
        // console.log(username);
        var edit_btn = $.el("button", {"class": "btn btn-secondary btn-edit", "type": "button"}).html("...");
        var pk = $.el("p",{"class": "pk"});
        pk.text(tweets[i].pk);

        name_date_container.appendChild(anchor);
        name_date_container.appendChild(date);
        name_date_container.appendChild(pk.get(0));
        if(username === tweets[i].username){
            name_date_container.appendChild(pk.get(0));
            name_date_container.appendChild(edit_btn.get(0));
        }
        
        var tweet_txt = document.createElement('p');
        tweet_txt.textContent = tweets[i].content;
        tweet_main.appendChild(name_date_container);
        tweet_main.appendChild(tweet_txt);
        
        // Icon container
        var icon_cont = document.createElement('div');
        icon_cont.setAttribute("class", "d-flex icons-section");
        var icon = $.el("i", {"class": "fas fa-heart"})
        if (liked_pk.includes(tweets[i].pk)){
            icon.css("color", "red");
        }
        var counter_txt = document.createElement("div");
        counter_txt.setAttribute("id","like-counter")
        counter_txt.innerHTML = tweets[i].likes.toString();
        
        icon_cont.appendChild(icon.get(0));
        icon_cont.appendChild(counter_txt)

        // Add all to tweet container
        tweet_cont.appendChild(user_photo)
        tweet_cont.appendChild(tweet_main);
        tweet_cont.appendChild(icon_cont);

        // Add to document fragment
        frag.appendChild(tweet_cont);

        // Append to DOM
        // container.innerHTML = "";
        $(container).fadeIn().append(tweet_cont);
        // container.appendChild(tweet_cont);
        // console.log(liked_pk);
        icon.on("click", function(event){
            const pk = $(event.target.parentNode.parentNode).children().find("p")[1];
            // console.log(parseInt(pk.textContent));
            if(liked_pk.includes(parseInt(pk.textContent))){
                console.log("Dislike Post");
                $.ajax({
                    url: '/api/v1/like/',
                    method: 'DELETE',
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": csrftoken,
                    },
                    data: {
                        "pk": pk.textContent,
                    },
                    success: function(data){
                        console.log($(event.target.parentNode.parentNode))
                        $(event.target.parentNode.parentNode).children().find("i").css("color", "black");
                        var counterElment = $(event.target.parentNode.parentNode).children().find("#like-counter")
                        current_counter = parseInt($(event.target.parentNode.parentNode).children().find("#like-counter").html());
                        counterElment.html(current_counter-1);
                        const idx = liked_pk.indexOf(parseInt(pk.textContent));
                        if (idx > -1){
                            liked_pk.splice(idx, 1);
                        }
                        console.log("Like deleted");
                        console.log(liked_pk);

                    }, 
                    failure: function(data){
    
                    }
                })
            }else if(!liked_pk.includes(parseInt(pk.textContent))){
                $.ajax({
                    url: '/api/v1/like/',
                    method: 'POST',
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": csrftoken,
                    },
                    data: {
                        "pk": pk.textContent,
                    },
                    success: function(data){
                        $(event.target.parentNode.parentNode).children().find("i").css("color", "red");
                        var counterElment = $(event.target.parentNode.parentNode).children().find("#like-counter")
                        current_counter = parseInt($(event.target.parentNode.parentNode).children().find("#like-counter").html());
                        counterElment.html(current_counter+1);
                        // const idx = liked_pk.indexOf(parseInt(pk.textContent));
                        liked_pk.push(parseInt(pk.textContent));
                        console.log("Liked post successfully");
                        console.log(liked_pk)
                        // console.log(current_counter);
                    }, 
                    failure: function(data){
    
                    }
                })
            }
            
        });
        edit_btn.on("click", function(event){
            if(event.target.innerHTML ==="..."){
                event.target.innerHTML = "Save";
                // console.log($(this).parent()[0].childNodes[2].textContent);
                const content_elmnt = $(this).parent().parent()[0].childNodes[1];
                const editable_content = $.el("textarea",{}).text(content_elmnt.textContent);
                console.log(content_elmnt.parentNode);
                content_elmnt.parentNode.replaceChild(editable_content.get(0), content_elmnt);
            }else{                
                event.target.innerHTML = "...";
                const content_elmnt = $(this).parent().parent()[0].childNodes[1];
                const non_editable_content = $.el("p",{}).text(content_elmnt.value);
                console.log(content_elmnt.parentNode);
                content_elmnt.parentNode.replaceChild(non_editable_content.get(0), content_elmnt);
                if(content_elmnt.value != content_elmnt.innerHTML){

                $.ajax(
                    {
                        url: "/api/v1/tweets/",
                        method: "POST",
                        headers: {
                                "Accept": "application/json",
                                "X-CSRFToken": csrftoken,
                        },
                        data: {
                            'data': content_elmnt.value.toString(),
                            'pk': $(this).parent()[0].childNodes[2].textContent,
                        },
                        success: function(data){

                        },
                        failure: function(data){

                        }
                    }
                );
                }
                
            }
            
        });
        
    }
}

//Pagination Logic 
$($(".page-item")[1]).addClass("active");
//Create pagination component given number of pages
function pagLinkCreation(){

}

//Handle clicks on pagination components
$(".page-item").on("click", function(event){
    // $(".page-item").removeClass("active");
    // var container = document.querySelector(".tweets-container");
    if($(".page-item.active").length===0){
        var current_page = 1;
        $($(".page-item")[1]).addClass("active");
    }else{
        var current_page_int = parseInt($(".page-item.active").children()[0].text);
    }
    
    if(event.target.innerHTML === 'Previous'){
        if (current_page_int>1){
            $(".page-item.active").removeClass("active");
            $($(".page-item")[current_page_int-1]).addClass("active");
            getTweetPage(current_page_int-1);        
        }else{
        }
    }else if(event.target.innerHTML === 'Next'){
        if (current_page_int<current_page_count){
            $(".page-item.active").removeClass("active");
            $($(".page-item")[current_page_int+1]).addClass("active");
            getTweetPage(current_page_int+1);        
        }else{
        }
    }else{
        $(".page-item.active").removeClass("active");
        // $($(".page-item")[current_page_int-1]).addClass("active");
        var item = $(event.target.parentNode);
        if (item.hasClass("active")){
            item.removeClass("active");
        }else{
            item.addClass("active");
        }
        getTweetPage(parseInt(event.target.innerHTML));
    }    
});

function convertToReadableDate(date){
    var newDate = new Date(date);
}


//Logic to edit post

