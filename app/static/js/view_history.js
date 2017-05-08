// view_history.js

// way to test:
// http://127.0.0.1:5000/view_history?customer_id=001


$(document).ready(function(){
	var url = location.search;
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        var url_vals = {};
        var str_splits = str.split("&");
        for (var i = 0; i < str_splits.length; i++) {
        	url_vals[str_splits[i].split("=")[0]] = str_splits[i].split("=")[1];
        }
        var customer_id = url_vals["customer_id"];

        $("a#navi_home_page").bind("click",function(){
            window.location.href="home_page?customer_id="+customer_id;
        });

        $("a#navi_my_profile").bind("click",function(){
            window.location.href="your_profile?customer_id="+customer_id;
        });

        $("a#navi_my_orders").bind("click",function(){
            window.location.href="view_history?customer_id="+customer_id;
        });

        $("#navi_search_home_page").click(function(){
            search_value = $("input[name='q_navi']").val();
            window.location.href="search_results?who=customer&search_value="+search_value+'&customer_id='+customer_id;
        });

        $("#search_block_in_search_results").keydown(function() {
             if (event.keyCode == "13") {
                 $('#navi_search_home_page').click();
             }
        });
        
        console.log("customer_id"+customer_id);
        $.getJSON("/get_user_history",{"customer_id":customer_id}, function(data){
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
                console.log("item is:"+JSON.stringify(item));
        		var restaurant_name = item.restaurant_name;
        		var order_id = item.order_id;
        		var order_total_price = item.order_total_price;
        		var dishes = item.dishes;
                var create_time = item.create_time;
                var comment = item.comment;
                if (comment == null) {
                    comment = '暂无评论';
                }
                var receive_time = item.receive_time;
                if (receive_time == null) {
                    receive_time = '暂未收货';
                }
                console.log("receive_time:"+receive_time);
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
				}
                console.log("order_id in str:"+order_id);
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
                           <span id="order_id">下单:'+create_time+'</span><br/>\
					       <span id="order_id">收货:'+receive_time+'</span>\
					    </p>\
					    <h4 class="alt-h4 lh-condensed mb-1">Includes:</h4>\
					    <ul class="list-style-none lh-condensed">\
					    '+dish_list+'<br/><h4 class="alt-h4 lh-condensed mb-1">Comment:</h4>'+comment+'\
					  </div>';

                if (receive_time != '暂未收货' && comment != '暂无评论') {      //received and commented
                    console.log("receive_time is null");
                    str += '<a class="btn btn-block btn-outline f4 plans-card-btn disabled">Received the Dishes</a>';

                } else if (receive_time != '暂未收货' && comment == '暂无评论') {    //received but not comment
                    str +=  '<a id="commit_receive" href="#faceboxdiv" name="'+order_id+'" rel="facebox" onclick="change_id(this)" class="btn btn-block btn-outline f4 plans-card-btn">Comment</a>';
                } else {    // have not received
                    str +=  '<a id="commit_receive" href="#faceboxdiv" name="'+order_id+'" rel="facebox" onclick="received_order(this)" class="btn btn-block btn-outline f4 plans-card-btn">Received the Dishes</a>';
                } str += '<a name="'+order_id+'" onclick="delete_order(this)" class="btn btn-danger btn-sm f4">Delete Order</a>\
                         </div>\
                     </td>';
        	});
            str += '</tr></tbody></table>';
            $("#main_body").html(str);
        });
    }
    $("a").css("cursor","pointer");
});

var comment_order_id = '0';

var delete_order = function(obj) {
    swal({
          title: 'Are you sure?',
          text: 'are you sure to delete this order?',
          type: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Yes, delete it!',
          cancelButtonText: 'No, keep it',
    },function(isConfirm) {
        if (isConfirm === true) {
            var orderid = $(obj).prop("name");
            $.getJSON("delete_order",{"order_id":orderid},function(data){
                if(data.ERROR) {
                    swal(data.ERROR);
                } else {
                    window.location.href = location.search;
                }
            })
        } else {}
    });    
}

var received_order = function(obj){
    if ($(obj).hasClass("disabled")) {
        return;
    } else {
        var received_order_id = $(obj).prop("name");
        console.log("order_id"+received_order_id);
        $.getJSON("/receive_order",{"order_id":received_order_id,"received":true},function(data){
            if (data.ERROR){
                swal(data.ERROR);
            }else {
                console.log("order_id:"+received_order_id+";received");
                $(obj).addClass("disabled");
                comment_order_id = received_order_id;
            }
        })
    }
};

var dish_comment = '';

var set_comment = function(obj) {
    dish_comment = obj.value;
}

var submit_comment = function() {
    console.log("comment"+dish_comment+"order_id"+comment_order_id);
    $.getJSON("/comment_order",{"comment":dish_comment,"order_id":comment_order_id},function(data){
        console.log("get response"+data);
        if (data.ERROR){
            swal(data.ERROR);
            return;
        } else {
            console.log("comment_order_id:"+comment_order_id+";dish_comment:"+dish_comment+";submitted");
            window.location.href = location.search;
        }
    });
}


var change_id = function(obj) {
    comment_order_id = $(obj).prop("name");
}



