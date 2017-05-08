// front_page.js,

$(document).ready(function(){
    var url = location.search;
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        var who = str.split("&")[0].split("=")[1];
        if (who == 'business') {
	    	$("a#jump_to_signin").html('Sign in to Business');
	    	$("a#jump_to_signin").attr("href",'signin?who=business');
	    	$("a#jump_to_signup").text('Sign up to Business');
	    	$("a#jump_to_signup").attr("href",'signup?who=business');
	    	$("h1#main_title").html("<strong>Open up your restaurant</strong>");
	    	$("a#navi.selected").attr("class","js-selected-navigation-item nav-item");
    		$("a[name='Business']").attr("class",'js-selected-navigation-item nav-item selected');
        }
    }
    $("a").css("cursor","pointer");
})

$("a#navi").bind("click",function(){
    if ($(this).html() == 'Business'){
        window.location.href = 'front_page?who=business';
    }
    if ($(this).html() == 'Customer') {
        window.location.href = 'front_page';
    }
    if ($(this).html() == 'My Order' || $(this).html() == 'Home Page') {
        swal("sign in first!");
    }
})