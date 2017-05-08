// change_avatar.js


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
        
        console.log("customer_id:"+customer_id);
        $("a#avatar").bind("click",function(){
        	var name = $(this).prop("name");
        	console.log("name:"+name);
        	$.getJSON("customer_change_avatar",{"customer_id":customer_id,"customer_avatar":name},function(data){
        		if(data.ERROR){
        			swal(data.ERROR);
        		} else {
        			// swal("change avatar succeed!");
                    window.location.href="your_profile?customer_id="+customer_id;
        		}
        	});
        });
    } else {
    	swal("log in first!");
    }
    $("a").css("cursor","pointer");
});