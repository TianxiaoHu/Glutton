// restaurant_order_history.js
					    // <a id="commit_receive" href="#faceboxdiv" rel="facebox" onclick="received_order(this,' + order_id + ')" class="btn btn-block btn-outline f4 plans-card-btn">Received the Dishes</a>\

$(document).ready(function(){
	var url = location.search;
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        var url_vals = {};
        var str_splits = str.split("&");
        for (var i = 0; i < str_splits.length; i++) {
        	url_vals[str_splits[i].split("=")[0]] = str_splits[i].split("=")[1];
        }
        var restaurant_id = url_vals["restaurant_id"];

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
            window.location.href="search_results?who=business&search_value="+search_value+'&customer_id='+restaurant_id;
        });

        $("#search_block_in_search_results").keydown(function() {
             if (event.keyCode == "13") {
                 $('#navi_search_home_page').click();
             }
         });

        $("#search_home_page").click(function(){
            search_value = $("input[name='q']").val();
            window.location.href="search_results?who=business&search_value="+search_value+'&customer_id='+restaurant_id;
        });

        console.log("restaurant_id"+restaurant_id);
        $.getJSON("/get_restaurant_history",{"restaurant_id":restaurant_id}, function(data){
        	console.log("get data:"+JSON.stringify(data));
            if (data.ERROR) {
                swal(data.ERROR);
                return;
            }
        	result = data.result;
        	var str= '<table>\
                        <tbody>\
                            <tr>';
        	var order_total_price = 0;
        	$.each(result, function(i, item){
        		var restaurant_name = item.customer_nickname;
        		var comment = item.comment;
        		var create_time = item.create_time;
                var receive_time = item.receive_time;
                if (receive_time == null) {
                    receive_time = '尚未收货';
                }
                console.log("restaurant_name:"+restaurant_name);
        		var order_id = item.order_id;
                console.log("order_id"+item.order_id);
        		var order_total_price = item.order_total_price;
                console.log("order_total_price"+order_total_price);
        		var dishes = item.dishes;
        		var dish_list = '<ul class="list-style-none lh-condensed">';
        		$.each(dishes, function(j, dish_item){
                    dish_amount = dish_item.dish_amount;
        			var dish_name = dish_item.dish_name;
        			var dish_price = dish_item.dish_price;
					dish_list += '<li class="mb-1">'+ dish_name+'：<span class="default-currency">¥'+dish_price+' &nbsp'+dish_amount+'份</span></li>';
        		});
        		dish_list += '</ul>';
        		if (i%3 == 0) {
        			if (i != 0) {
        				str += '</tr><tr>';
        			}
					// str += '<div class="plans-cards pt-3 my-3">';
				}
        		str += '\
                <td>\
					 <div class="plans-card text-center bg-white border rounded-2">\
					    <a class="d-block mb-0 py-2 px-3 border-bottom text-blue no-underline">\
					      <h2 class="alt-h3">'+restaurant_name+'</h2>\
					    </a>\
					  <div class="plans-card-text p-3">\
					    <h3 class="alt-h2 text-normal mb-0 lh-condensed">\
					      <span class="default-currency">Total:¥'+order_total_price+'</span>\
					    </h3>\
					    <p class="mb-4 alt-text-small text-gray>\
					      order id: <span id="order_id">下单：'+create_time+'</span><br/><span id="order_id">收货：'+receive_time+'</span>\
					    </p>\
					    <h4 class="alt-h4 lh-condensed mb-1">Includes:</h4>\
					    <ul class="list-style-none lh-condensed">\
					    '+dish_list+'\
					  </div>';
				if (comment == null) {
        			console.log("comment is null");
        			str += '<a class="btn btn-block btn-outline f4 plans-card-btn disabled">View Comment</a>\
						</div>\
               		</td>';
        		} else { 
                    console.log("commet is:"+comment);
					str +=  '<span id="comment" style="display:none;">'+comment+'</span><a id="commit_receive" onclick="view_comment(this)" class="btn btn-block btn-outline f4 plans-card-btn">View Comment</a>\
						</div>\
                	</td>';
            	}
                
                // console.log("final str is: "+str);
        	});
            str += '</tr></tbody></table>';
            $("#main_body").html(str);
        });
    }
    $("a").css("cursor","pointer");
});

var comment_order_id = '0';

var view_comment = function(obj){
    if ($(obj).hasClass("disabled")) {
        swal("customer haven't commented yet!");
        return;
        // how to stop the facebox?
    } else {
        var com = $(obj).prev("span:first").html();
    	swal("comment:"+com);
    }
};




