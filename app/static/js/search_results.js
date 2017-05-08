// search_results.js

var restaurant = "Restaurants";
var dishes = "Dishes";
var current_div = restaurant;
var initialized = false;
var page_num = 0;
var search_value = "";
var who = '';
var customer_id = "";
var search = function(page,current_div,search_content, key){
	console.log("search_value"+search_content);
	console.log("who"+who);
	var route_to_search = '';
	var input_dict  = {"search_value":search_content,"page":page,"customer_id":customer_id};
	if (current_div == restaurant){
		if (key == 0) {
			route_to_search = "search_restaurant_results";
		} else if (key == 1) {
			route_to_search = "search_restaurant_results_by_price";
		} else {
			route_to_search = "search_restaurant_results_by_sale";
		}
	} else {
		if (key == 0){
			route_to_search = "search_dish_results";
		} else if (key == 1) {
			route_to_search = "search_dish_results_by_price";
		} else {
			route_to_search = "search_dish_results_by_sale";
		}
	}
	$.getJSON(route_to_search,input_dict,function(data){

		if (data.ERROR) {
			swal(data.ERROR);
		}

		$("span#total_result_len").text(data.total_result);
		$("span#current_div").text(current_div);
		if (page_num != data.total_page || page == 0) {
			page_num = data.total_page;
			var str = '<span class="previous_page disabled" onclick="previous_page()">Previous</span>';
			for (var i = 1; i <= 5; i++) {
				if ( i <= page_num ) {
					if (i==1) {
			 			str += '<a id="page_n" class="current">' + (i).toString() + '</a>'
			 		} else {
			 			str += '<a id="page_n" class="">' + (i).toString() + '</a>'	
			 		}
			 	} else {
			 		break;
		 		}
		 	}
			$("div.pagination").text('');
			if (page_num < 8){
			$("div.pagination").append(str+'<span class="next_page" rel="next" onclick="next_page()">Next</span>');
			} else {
				$("div.pagination").append(str+'<span class="gap">…</span>'+'<span class="next_page" rel="next" onclick="next_page()">Next</span>');
			}
			$("a#page_n").bind("click",function(){toPage($(this).html(),this);});
		} 
		if (data.total_page == 0 || data.total_page == '1'){
			$("span.next_page").attr("class","next_page disabled");
		}
		

		$("input#search_block_in_search_results").attr("value",decodeURIComponent(search_value));
		$("div#tofill").text('');
		if(current_div == restaurant){
			$("#search_by_price_content").html("By base delivery fee");
			$("#results_overview").html('');
			$.each(data.result_list, function(i,eachData){
				eval(eachData);
				var name = eachData.restaurant_name;
				var address = eachData.restaurant_address;
				if (address == null) {
					address = '暂无';
				}
				var restaurant_id = eachData.restaurant_id;
				var description = eachData.restaurant_description;
				if (description == null) {
					description = '暂无';
				}
				var base_delivery_price = eachData.base_deliver_price;
				if (base_delivery_price == null) {
					base_delivery_price = '暂无';
				}
				var str = '\
						<div class="repo-list-item d-flex flex-justify-start py-4 public source">\
						<div class="col-8 pr-3">\
						<h3>\
						<a href="restaurant_home_page?who='+who+'&restaurant_name='+name+'&restaurant_id='+restaurant_id+'&customer_id='+customer_id+'" class="v-align-middle">'+name+'</a>\
						</h3>\
						<p class="d-inline-block text-gray mb-2 pr-4">描述：'+description+'；（起送费：'+base_delivery_price+'¥）\
						</p>\
						<p class="f6 text-gray mb-0 mt-2">地址：'+address+'</p>\
						</div>\
						<div class="d-table-cell col-2 text-gray pt-2">\
						<span class="repo-language-color ml-0" style="background-color:#f1e05a;"></span>\
						营业时间: '+eachData.open_time+'\
						</div>\
						<div class="col-2 pt-1 pr-3 pt-2">\
						<a class="muted-link">\
						<svg aria-label="star" class="octicon octicon-star" height="16" role="img" version="1.1" viewBox="0 0 14 16" width="14">\
						<path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z">hehe</path>\
						</svg>月销量:<br/>&nbsp;&nbsp;&nbsp;'+eachData.total_month_sale+'&nbsp;&nbsp;&nbsp;&nbsp;\
						</a>\
						</div>\
						</div>\
						';
				console.log("name:"+name);
				$("div#tofill").append(str);

				var results_str = '<li>\
						            <span class="bar" style="width: 19%;"></span>\
						            <a href="restaurant_home_page?who='+who+'&restaurant_name='+name+'&restaurant_id='+restaurant_id+'&customer_id='+customer_id+'" class="filter-item"><span class="count"></span>'+name+'</a>\
						        </li>';
				$("#results_overview").append(results_str);


			});
		} else {
			$("#search_by_price").html("By Price");
			$("#results_overview").html('');
			$.each(data.result_list, function(i,eachData){
			eval(eachData);
			var dish_name = eachData.dish_name;
			var dish_price = eachData.dish_price;
			var restaurant_name = eachData.restaurant_name;
			var dish_month_sale = eachData.dish_month_sale;
			if (dish_month_sale == null) {
				dish_month_sale = '暂无';
			}
			var dish_id = eachData.dish_id;
			var restaurant_id = eachData.restaurant_id;
			var str = '\
					<div class="repo-list-item d-flex flex-justify-start py-4 public source">\
					<div class="col-8 pr-3">\
					<h3>\
					<a class="v-align-middle" href="restaurant_home_page?who='+who+'&restaurant_name='+restaurant_name+'&restaurant_id='+restaurant_id+'&customer_id='+customer_id+'">'+restaurant_name+'</a>/\
					<a href="restaurant_home_page?who='+who+'&restaurant_name='+restaurant_name+'&restaurant_id='+restaurant_id+'&customer_id='+customer_id+'" class="v-align-middle">'+dish_name+'</a>\
					</h3>\
					</div>\
					<div class="d-table-cell col-2 text-gray pt-2">\
					<span class="repo-language-color ml-0" style="background-color:#f1e05a;"></span>价格: '+dish_price+'¥\
					</div>\
					<div class="col-3 pt-1 pr-3 pt-2">\
					<a class="muted-link">\
					<svg aria-label="star" class="octicon octicon-star" height="16" role="img" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z"></path></svg>月销量: '+dish_month_sale+'\
					</a>\
					</div>\
					</div>\
					';
			$("div#tofill").append(str);

			var results_str = '<li>\
						            <span class="bar" style="width: 19%;"></span>\
						            <a href="restaurant_home_page?who='+who+'&restaurant_name='+restaurant_name+'&restaurant_id='+restaurant_id+'&customer_id='+customer_id+'" class="filter-item">\
						              <span class="count">'+dish_price+'¥</span>'+dish_name+'\
						            </a>\
						        </li>';
			$("#results_overview").append(results_str);

		});
		}
	});
}



var toPage = function(page, obj) {
	console.log("console");
	if (page!=1) {
		$("span.previous_page").attr("class","previous_page");
	} else {
		$("span.previous_page").attr("class","previous_page disabled");
	} 
	if (page!=page_num) {
		$("span.next_page").attr("class","next_page");
	} else {
		$("span.next_page").attr("class","next_page disabled");
	}
	console.log("page:"+page);
	$("a.current").attr("class",'');
	$(obj).attr("class","current");
	search(parseInt(page), current_div, search_value, 0);
}


var getDishes = function() {
	$("a#getDishes").attr("class","underline-nav-item selected");
	$("a#getRestaurants").attr("class","underline-nav-item");
	$("span#best_match").html("Best Match");
	current_div = dishes;
	search(1, current_div, search_value, 0);
}

var getRestaurants = function() {
	$("span#best_match").html("Best Match");
	$("a#getDishes").attr("class","underline-nav-item");
	$("a#getRestaurants").attr("class","underline-nav-item selected");
	current_div = restaurant;
	search(1, current_div, search_value, 0);
}

var next_page = function() {
	if ($("span.next_page").hasClass("disabled")) {
		return
	} else {
		var page = $("a#page_n.current").html();
		obj = $("a#page_n.current").next();
		if (obj.html() == '…') {
			var start_page = parseInt(page)+1;
			var str = '<span class="previous_page" onclick="previous_page()">Previous</span>'+'<span class="gap">…</span>';
			for (var i = 0; i < 8; i++) {
				if ( start_page + i <= page_num ) {
					if (i==0) {
			 			str += '<a id="page_n" class="current">' + (start_page + i).toString() + '</a>'
			 		} else {
			 			str += '<a id="page_n" class="">' + (start_page + i).toString() + '</a>'	
			 		}
			 	} else {
			 		break;
			 	}
			}
			$("div.pagination").text('');
			$("div.pagination").append(str+'<span class="gap">…</span>'+'<span class="next_page" rel="next" onclick="next_page()">Next</span>');
			$("a#page_n").bind("click",function(){toPage($(this).html(),this);});
			toPage(parseInt(page)+1, $("div.pagination").children("a#page_n:first"));
		} else {
			toPage(parseInt(page)+1, obj);
		}
	}
}

var previous_page = function() {
	if ($("span.previous_page").hasClass("disabled")) {
		return
	} else {
		var page = $("a#page_n.current").html();
		obj = $("a#page_n.current").prev();
		if (obj.html() == '…') {
			var start_page = parseInt(page)-1;
			var str = '';
			for (var i = 0; i < 8; i++) {
				if ( start_page - i > 0 ) {
					if (i==0) {
			 			str = '<a id="page_n" class="current">' + (start_page - i).toString() + '</a>' + str;
			 		} else {
			 			str = '<a id="page_n" class="">' + (start_page - i).toString() + '</a>'	+ str;
			 		}
			 	} else {
			 		break;
			 	}
			}
			$("div.pagination").text('');
			$("div.pagination").append('<span class="previous_page" onclick="previous_page()">Previous</span>'+'<span class="gap">…</span>'+str + '<span class="gap">…</span>'+'<span class="next_page" rel="next" onclick="next_page()">Next</span>' );
			$("a#page_n").bind("click",function(){toPage($(this).html(),this);});
			toPage(parseInt(page)+1, $("div.pagination").children("a#page_n:last"));
		} else {
			toPage(parseInt(page) - 1, obj);
		}
	}
}

$(document).ready(function(){
	var url = location.search;
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        var url_vars = {}
        var str_split = str.split("&");
        for (var i = 0; i < str_split.length; i++) {
        	url_vars[str_split[i].split("=")[0]] = str_split[i].split("=")[1];
        }
        customer_id = url_vars["customer_id"];
        search_value = url_vars["search_value"];

        $("#search_origin").bind("click",function(){
    		search(1,current_div, search_value, 0);
        });

        $("#search_by_price").bind("click",function(){
    		search(1,current_div, search_value, 1);
        });

        $("#search_by_sale").bind("click",function(){
    		search(1,current_div, search_value, 2);
        });

        who = url_vars["who"];
        if (who == 'customer') {
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
        } else {
        	var restaurant_id = customer_id;
        	$("#navi_dishes").attr("style","display:block;");
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
        }
    	search(1,"Restaurants", search_value, 0);
        
    }
	$("a#page_n").bind("click",function(){toPage($(this).html(),this);});
    $("a").css("cursor","pointer");
});




















