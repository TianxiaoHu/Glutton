// restaurant_home_page.js

var viewing_dish_id=0;
var restaurant_id="";
$(document).ready(function(){
    var dish_counts = {};
    var url = location.search;

    if (url.indexOf("?") != -1) {
        var str = url.substr(1);        
        var splits = str.split("&");
        var route = {}
        for (var i = 0; i < splits.length; i++){
            route[splits[i].split("=")[0]] = splits[i].split("=")[1];
        }
        
        restaurant_id = route['restaurant_id'];

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
        
        $.getJSON("/get_restaurant_detail",{"customer_id":"-","restaurant_id":restaurant_id},function(data){
            console.log("get data!!!~~~~~"+JSON.stringify(data));
            $("ul#dish_info").html('');
            var str = '';
            var restaurant_info = eval(data.restaurant);
            console.log(JSON.stringify(restaurant_info));
            var delivery_price = restaurant_info.delivery_fee;
            if (delivery_price == null) {
                delivery_price = '暂无';
            }
            $("span#month_total_sale").html(delivery_price);
            var base_deliver_price = restaurant_info.base_deliver_price;
            if (base_deliver_price == null) {
                base_deliver_price = '暂无';
            }
            $("span#delivery_span").html(base_deliver_price);
            var restaurant_name = restaurant_info.restaurant_name;
            $("span#restaurant_name").html(restaurant_name);
            var open_time = restaurant_info.open_time;
            if (open_time == null) {
                open_time = '暂无';
            }
            $("span#open_time_restaurant").html(open_time);
            var restaurant_address = restaurant_info.restaurant_address;
            var restaurant_description = restaurant_info.restaurant_description;
            if (restaurant_address == null) {
                restaurant_address = '暂无';
            }
            if (restaurant_description == null) {
                restaurant_description = '暂无';
            }
            $("span#restaurant_id").html("地址："+restaurant_address+"; 描述："+restaurant_description);
            var dishes = data.dish;
            var dish_num = dishes.length;

            $.each(dishes, function(i,item){
                var dish_id = item.dish_id;
                var dish_name = item.dish_name;
                var month_sale = item.dish_month_sale;
                var dish_price = item.dish_price;
                dish_counts[dish_id] = 0;
                str += '\
                <li class="repo-list-item" style="width:90%">\
              <h3 class="mb-1">\
              	<span id="dish_id" style="display:none;">'+dish_id+'</span>\
                <a href="#faceboxdiv" rel="facebox" id="dish_name">'+dish_name+'\
                </a>\
              </h3>\
              <div>\
                  <div class="d-inline-block col-9 text-gray pr-4">\
                      <div class="f6 text-gray mt-2">\
                            <span class="repo-language-color ml-0" style="background-color:#e34c26;"></span>\
                          <span class="mr-3" itemprop="programmingLanguage">\
                            价格: '+dish_price+'¥\
                          </span>\
                          <a class="muted-link mr-3">\
                            <svg aria-label="star" class="octicon octicon-star" height="16" role="img" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z"></path></svg>\
                            月销量: '+month_sale+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                          </a>\
                      </div>\
                  </div>\
                <div class="col-3 float-right">   \
                  <div width="155" height="30">\
              	  <span id="dish_id" style="display:none;">'+dish_id+'</span>\
                  <a id="dish_name" href="#faceboxdiv" rel="facebox" class="btn btn-sm btn-primary" id="cut_dish" style="width:59.28px; text-align:center">Edit</a>\
              	  <span id="dish_id" style="display:none;">'+dish_id+'</span>\
                	<a class="btn btn-danger btn-sm btn-primary" id="delete_dish">Delete</a>\
                  </div>\
                </div>\
              </div>\
            </li>';
            });

            $("ul#dish_info").html(str);
            $("a#dish_name").bind("click",function(){
            	viewing_dish_id = $(this).prev("span#dish_id:first").html();
            });

            $("a#delete_dish").bind("click",function(){
            	var delete_dish_id = $(this).prev("span#dish_id:first").html();
            	// swal('are you sure to delete dish:'+delete_dish_id+"?");

                swal({
                      title: 'Are you sure?',
                      text: 'are you sure to delete dish:'+delete_dish_id+"?",
                      type: 'warning',
                      showCancelButton: true,
                      confirmButtonText: 'Yes, delete it!',
                      cancelButtonText: 'No, keep it',
                },function(isConfirm) {
                    if (isConfirm === true) {
                    	$.getJSON("/delete_dish",{"dish_id":delete_dish_id},function(data){
                    		if (data.ERROR){
                    			swal(data.ERROR);
                    		} else {
                                window.location.href=location.search;
                    		}
                    	});
                    } else {}
                });
            });

        });

    }
    $("a").css("cursor","pointer");
}); 




var dish_name = $("input#dish_name").text();
var dish_price = $("input#dish_price").val();

var set_dish_name = function(obj) {
	dish_name = obj.value;
}

var set_dish_price = function(obj) {
	dish_price = obj.value;
}

var submit_change_dish = function() {
	console.log("clicked");
	console.log("dish_name"+dish_name+dish_price+"viewing_dish_id"+viewing_dish_id);
	$.getJSON("/change_dish",{"dish_id":viewing_dish_id,"dish_name":dish_name,"dish_price":dish_price},function(data){
		console.log("get response"+data);
		if (data.ERROR){
			swal(data.ERROR);
		} else {
			window.location.href = location.search;
		}
	});
}

var new_dish_name = $("input#add_dish_name").val();
var new_dish_price = $("input#add_dish_price").val();

var create_dish_name = function(obj) {
    new_dish_name = obj.value;
}

var create_dish_price = function(obj) {
    new_dish_price = obj.value;
}

var add_dish_submit = function() {
    console.log("new_dish_price:"+new_dish_price);
    console.log("new_dish_name:"+new_dish_name);
    console.log("restaurant_id:"+restaurant_id);
    $.getJSON("/add_dish",
        {"dish_name":new_dish_name,
        "restaurant_id":restaurant_id,
        "dish_price":new_dish_price},function(data){
        if (data.ERROR){
            swal(data.ERROR);
        } else {
            window.location.href = location.search;
        }
    })
}












