// signup.js
// return jsonify({"status": 0, 
// "customer_id": customer_id,  
// "customer_nickname": customer_nickname, 
// "customer_mobile_number": customer_mobile_number, 
// "customer_address": customer_address, 
// "customer_discription": customer_discription, 
// "customer_gender": customer_gender, 
// "customer_appellation": customer_appellation})

var who = 'customer';
var signin = function() {
    var password = $("input[name='password']").val();
    var mobile = $("input[name='login']").val();
    var route = "user_signin_submit";
    if (who == 'business'){
        route = "restaurant_signin_submit";
    }
    var input_dict = {}
    if (who == 'business'){
        input_dict["owner_nickname"] = mobile;
        input_dict["owner_password"] = password;
    } else {
        input_dict["customer_password"] = password;
        input_dict["customer_mobile_number"] = mobile;
    }
    $.getJSON(route,input_dict,function(data){
        if (data.ERROR) {
            swal(data.ERROR);
        } else {
            if (who == 'business') {
                window.location.href="owner_home_page?customer_id="+data.restaurant_id+
                "&owner_nickname="+data.owner_nickname+
                "&restaurant_name="+data.restaurant_name+
                "&who="+who;
            } else {
            window.location.href="home_page?customer_id="+data.customer_id+
                "&customer_nickname="+data.customer_nickname+
                '&customer_mobile_number='+data.customer_mobile_number+
                "&customer_nickname="+data.customer_nickname+
                "&who="+who;
            }
        }
    });
}

$("input[name='password']").keydown(function() {
    if (event.keyCode == "13") {
        signin();
    }
});


$(document).ready(function(){
    var url = location.search;
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        who = str.split("&")[0].split("=")[1];
        if (who=='business'){
            $("label#first_label").html("Input your nickname");
            $("h1").children("strong").html('Sign in as owner');
        } else {
            
        }
        $("span#picture_nickname").html(nickname);
        $("span#USER_ID").html(customer_id);
    }
    $("a").css("cursor","pointer");
})