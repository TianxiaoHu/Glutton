// owner_home_page.js
var search_value = "";


$(document).ready(function(){
    var url = location.search;
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        var url_var = str.split("&");
        var url_vars = {}
        for (var i = 0; i < url_var.length; i++) {
            url_vars[url_var[i].split("=")[0]] = url_var[i].split("=")[1];
        }
        
        console.log($("span#picture_nickname").html());
        $("span#picture_nickname").html(url_vars["owner_nickname"]);
        console.log($("span#picture_nickname").html());
        console.log(JSON.stringify(url_vars));
        var customer_id = url_vars["customer_id"];
        var restaurant_id = customer_id;

        $("a#navi_home_page").bind("click",function(){
            window.location.href="owner_home_page?customer_id="+restaurant_id;
        });

        $("a#navi_my_profile").bind("click",function(){
            window.location.href="restaurant_profile?restaurant_id="+restaurant_id;
        });

        $("a#navi_my_dishes").bind("click",function(){
            window.location.href="restaurant_dish_management?restaurant_id="+restaurant_id;
        });

        $("a#navi_my_orders").bind("click",function(){
            window.location.href="restaurant_order_history?restaurant_id="+restaurant_id;
        });

        $("#navi_search_home_page").click(function(){
            search_value = $("input[name='q_navi']").val();
            window.location.href="search_results?who=business&search_value="+search_value+'&customer_id='+url_vars["customer_id"];
        });

        $("#search_block_in_search_results").keydown(function() {
             if (event.keyCode == "13") {
                 $('#navi_search_home_page').click();
             }
        });

        $("#main_search_input").keydown(function() {
             if (event.keyCode == "13") {
                 $('#search_home_page').click();
             }
        });

        $("#search_home_page").click(function(){
            search_value = $("input[name='q']").val();
            window.location.href="search_results?who=business&search_value="+search_value+'&customer_id='+url_vars["customer_id"];
        });

        $("a#jump_to_profile").bind("click",function() {
            window.location.href = "restaurant_profile?restaurant_id="+customer_id;
        });

        $.getJSON("/get_restaurant_detail",{"customer_id":"-","restaurant_id":customer_id},function(data){
            console.log("get data!!!~~~~~"+JSON.stringify(data));
            $("ul#dish_info").html('');
            var str = '';
            var restaurant_info = eval(data.restaurant);
            console.log(JSON.stringify(restaurant_info));
            var restaurant_description = restaurant_info.restaurant_description;
            var delivery_price = restaurant_info.delivery_fee;
            var base_deliver_price = restaurant_info.base_deliver_price;
            var restaurant_name = restaurant_info.restaurant_name;
            var open_time = restaurant_info.open_time;
            var time_span = restaurant_info.time_span;
            var total_month_sale = restaurant_info.total_month_sale;
            var restaurant_address = restaurant_info.restaurant_address;
            if (restaurant_address == null) {
                restaurant_address = '暂无';
            }
            var dishes = data.dish;
            var dish_num = dishes.length;

            $("span#picture_nickname").html(restaurant_name);
            $("span#USER_ID").html(restaurant_address);
            
            $.each(dishes, function(i,item){
                var dish_id = item.dish_id;
                var dish_name = item.dish_name;
                var month_sale = item.dish_month_sale;
                var dish_price = item.dish_price;
                str += '\
                    <a href="restaurant_dish_management?restaurant_id='+customer_id+'" class="exploregrid-item exploregrid-item-mini px-3 py-4">\
                          <h4 class="exploregrid-item-title">\
                            <span class="text-bold">'+dish_name+'</span>\
                          </h4>\
                          <span class="repo-language-color pinned-repo-meta" style="background-color:#DA5B0B;"></span>价格：<span id="dish_price">\
                          '+dish_price+'¥</span><span style="width: 300px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>\
                          <svg aria-label="star" class="octicon octicon-star" height="16" role="img" version="1.1" viewBox="0 0 14 16" width="14">\
                          <path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z"/></svg>\
                          月销量：<span id="month_sale">'+month_sale+'</span>\
                    </a>';
            });
            if (str!=""){
                $("div#owner_dishes").html(str);
            }
        });
    } else {
        swal("Sign in first!");
    }
    $("a").css("cursor","pointer");
});


