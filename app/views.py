# -*- coding:utf-8 -*-
"""
Author: Tianxiao Hu
Last Modified: 2017.5.8
Email: hutianxiao_fdu@126.com
Project for Introduction to Database Systems(COMP130010.03)@Fudan University
"""
import urllib
import hashlib
import sqlite3
import traceback
from app import app
from datetime import datetime
from flask import render_template, jsonify, request, g
from config import SQLALCHEMY_DATABASE_LOC, PAGINATION_PER_PAGE

### actions about db before and after request ###

@app.before_request
def before_request():
	g.conn = sqlite3.connect(SQLALCHEMY_DATABASE_LOC)
	g.cursor = g.conn.cursor()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'cursor'):
		g.cursor.close()
	if hasattr(g, 'conn'):
		g.conn.close()

### return html templates ###

@app.route('/')
@app.route('/front_page')
def index():
	return render_template('front_page.htm')

@app.route('/signup')
def signup():
	return render_template('signup.htm')

@app.route('/home_page')
def home_page():
	return render_template('home_page.htm')

@app.route('/your_profile')
def your_profile():
	return render_template('your_profile.htm')

@app.route('/change_avatar')
def change_avatar():
	return render_template('change_avatar.htm')

@app.route('/view_history')
def view_history():
	return render_template('view_history.htm')

@app.route('/signin')
def signin():
	return render_template('signin.htm')

@app.route('/search_results')
def search_results():
	return render_template('search_results.htm')

@app.route('/restaurant_profile')
def restaurant_profile():
	return render_template('restaurant_profile.htm')

@app.route('/restaurant_home_page')
def restaurant_home_page():
	return render_template('restaurant_home_page.htm')

@app.route('/owner_home_page')
def owner_home_page():
	return render_template('owner_home_page.htm')

@app.route('/restaurant_dish_management')
def restaurant_dish_management():
	return render_template('restaurant_dish_management.htm')

@app.route('/restaurant_order_history')
def restaurant_order_history():
	return render_template('restaurant_order_history.htm')

### functions defined for app routes ###

def md5_encrypt(str):
	"""
	:param str: string to encrypt
	:return: encrypted string
	"""
	m = hashlib.md5(str)
	return m.hexdigest()

def get_user_no():
	"""
	create a unique id for a new user
	:return: string
	"""
	total_user_num = len(g.cursor.execute("SELECT * FROM customer").fetchall()) + 1
	return '0' * (3 - len(str(total_user_num))) + str(total_user_num)

def get_restaurant_no():
	# restaurant_id start from '001'
	"""
	create a unique id for a new restaurant
	:return: string
	"""
	total_restaurant_num = len(g.cursor.execute("SELECT * FROM restaurant").fetchall()) + 1
	return '0' * (3 - len(str(total_restaurant_num))) + str(total_restaurant_num)

def get_customer_order_no():
	"""
	create a unique id for a new customer_order
	:return: string
	"""
	max_customer_order_num = g.cursor.execute('SELECT MAX(order_id) FROM customer_order').fetchall()[0][0]
	if not max_customer_order_num:
		max_customer_order_num = 0
	customer_order_id = int(max_customer_order_num) + 1
	return '0' * (3 - len(str(customer_order_id))) + str(customer_order_id)

def get_dish_order_no():
	"""
	create a unique id for a new dish_order
	:return: string
	"""
	max_dish_order_num = g.cursor.execute('SELECT MAX(dish_order_id) FROM dish_order').fetchall()[0][0]
	if not max_dish_order_num:
		max_dish_order_num = 0
	dish_order_id = int(max_dish_order_num) + 1
	return '0' * (4 - len(str(dish_order_id))) + str(dish_order_id)

def get_dish_no(restaurant_id):
	"""
	create a unique id for a new dish
	:return: string
	"""
	total_dish_num = len(g.cursor.execute("SELECT * FROM dish, restaurant "
	                                      "WHERE dish.restaurant_id = restaurant.restaurant_id "
	                                      "AND restaurant.restaurant_id = '%s'"
	                                      % restaurant_id).fetchall()) + 1
	return restaurant_id + '-' + '0' * (2 - len(str(total_dish_num))) + str(total_dish_num)

def jsonify_restaurant(restaurant):
	key_words = ("restaurant_id", "owner_nickname", "owner_password", "restaurant_name",
	             "restaurant_address", "delivery_fee", "base_deliver_price", "time_span",
	             "open_time", "total_month_sale", "restaurant_description")
	return dict(zip(key_words, restaurant))

def jsonify_customer(customer):
	key_words = ("customer_id", "customer_nickname", "customer_password", "customer_mobile_number",
				 "customer_address", "customer_description", "customer_appellation", "customer_avatar")
	return dict(zip(key_words, customer))

def jsonify_dish(dish):
	key_words = ("dish_id", "dish_name", "restaurant_id", "dish_price", "dish_month_sale")
	return dict(zip(key_words, dish))

def jsonify_dish_with_restaurant_name(dish_with_restaurant):
	key_words = ("dish_id", "dish_name", "restaurant_id", "dish_price", "dish_month_sale",
	             "restaurant_name")
	return dict(zip(key_words, dish_with_restaurant))

### Customer: signup/signin ###

@app.route('/user_signup_submit', methods = ['GET', 'POST'])
def user_signup_submit():
	"""
	create a new user in database
	mobile_number must be unique， password and nickname is required
	:return: json
	{"customer_id": customer_id, "customer_nickname": customer_nickname,
	 "customer_mobile_number": customer_mobile_number}
	"""
	customer_mobile_number = request.args.get("customer_mobile_number")
	customer_nickname = request.args.get("customer_nickname")
	customer_password = request.args.get("customer_password")
	customer_password = md5_encrypt(customer_password)
	customer_id = get_user_no()
	try:
		user_exist = g.cursor.execute("SELECT * FROM customer WHERE customer_mobile_number = '%s'"
		                              % (customer_mobile_number)).fetchall()
		if user_exist:
			return jsonify({"ERROR": "This mobile has been registered, you can sign in now."})
		g.cursor.execute("INSERT INTO customer VALUES ('%s', '%s', '%s', '%s', NULL, NULL, NULL, '1')"
						 % (customer_id,  customer_nickname, customer_password, customer_mobile_number))
		g.conn.commit()
		return jsonify({"customer_id": customer_id, "customer_nickname": customer_nickname,
		                "customer_mobile_number": customer_mobile_number})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Registration failed! Please try again..."})

@app.route('/user_signin_submit', methods = ['GET', 'POST'])
def user_signin_submit():
	"""
	comapre password provided by customer and password stored in database
	if equal: return user's profile
	else return ERROR
	:return: json
	{"customer_id", customer_id, "customer_nickname", customer_nickname,
	 "customer_password", customer_password, "customer_mobile_number": customer_mobile_number,
	 "customer_address": customer_address, "customer_description": customer_description, 
	 "customer_appellation": customer_appellation, "customer_avatar": customer_avatar }
	"""
	customer_mobile_number = request.args.get("customer_mobile_number")
	customer_password = request.args.get("customer_password")
	customer_password = md5_encrypt(customer_password)
	try:
		result = g.cursor.execute("SELECT * FROM customer WHERE customer_mobile_number = '%s'"
		                          % (customer_mobile_number)).fetchall()
		if result:
			db_password = result[0][2]
			if customer_password == db_password:
				return jsonify(jsonify_customer(result[0]))
			else:
				return jsonify({"ERROR": "Wrong username or password."})
		else:
			return jsonify({"ERROR": "User not exist."})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Sign in failed, please try again later."})

### Customers: profile and avatar ###

@app.route('/initialize_homepage', methods = ['GET','POST'])
def initialize_homepage():
	"""
	initialize customer's homepage, including user profile
	:return: json
	{"customer_id", customer_id, "customer_nickname", customer_nickname,
	 "customer_password", customer_password, "customer_mobile_number": customer_mobile_number,
	 "customer_address": customer_address, "customer_description": customer_description, 
	 "customer_appellation": customer_appellation, "customer_avatar": customer_avatar }
	"""
	customer_id = request.args.get("customer_id")
	try:
		res = g.cursor.execute("SELECT * FROM customer WHERE customer_id = '%s'" % (customer_id)).fetchall()
		if res:
			return jsonify(jsonify_customer(res[0]))
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Initialized failed, please try again later.."})

@app.route('/upload_your_profile', methods = ['GET','POST'])
def upload_your_profile():
	"""
	change customer profile including nickname, address, description, appellation 
	:return: succeed or ERROR
	"""
	customer_id = request.args.get("customer_id")
	customer_nickname = request.args.get("customer_nickname")
	customer_address = request.args.get("customer_address")
	customer_description = request.args.get("customer_description")
	customer_appellation = request.args.get("customer_appellation")
	try:
		g.cursor.execute("UPDATE customer SET customer_nickname = '%s', customer_address = '%s', "
		                 "customer_description = '%s', customer_appellation = '%s'"
		                 "WHERE customer_id = '%s'" %(customer_nickname, customer_address, customer_description,
		                                              customer_appellation, customer_id))
		g.conn.commit()
		updated_profile = g.cursor.execute("SELECT * FROM customer WHERE customer_id = '%s'"
		                                   % (customer_id)).fetchall()
		return jsonify(jsonify_customer(updated_profile[0]))
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Update profile failed, please try again later.."})

@app.route('/change_password', methods = ['GET','POST'])
def change_password():
	"""
	change password for customer, updated password is encrypted in database
	:return: succeed or ERROR
	"""
	customer_id = request.args.get("customer_id")
	old_password = request.args.get("old_password")
	old_password = md5_encrypt(old_password)
	new_password = request.args.get("new_password")
	new_password = md5_encrypt(new_password)
	try:
		old_password_db = g.cursor.execute("SELECT customer_password FROM customer WHERE customer_id = '%s'"
						 					% (customer_id)).fetchall()[0][0]
		if old_password == old_password_db:
			g.cursor.execute("UPDATE customer SET customer_password = '%s' WHERE customer_id = '%s'"
		                 	% (new_password, customer_id))
			g.conn.commit()
			return jsonify({"Succeed!": "Change password Succeed!"})
		else:
			return jsonify({"ERROR": "Please input correct old password!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Change password failed, please try again later.."})

@app.route('/customer_change_avatar', methods=['GET', 'POST'])
def customer_change_avatar():
	"""
	change avatar for customer, there are 9 available avatars in all
	marked from '1' to '9' in database
	:return: succeed or ERROR
	"""
	customer_id = request.args.get("customer_id")
	customer_avatar = request.args.get("customer_avatar")
	try:
		g.cursor.execute("UPDATE customer SET customer_avatar = '%s' WHERE customer_id = '%s'"
		                 % (customer_avatar, customer_id))
		g.conn.commit()
		return jsonify({"Succeed!": "Change avatar Succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Change avatar failed, please try again later.."})

### Customers: search restaurant/dish ###

@app.route('/search_restaurant_results', methods = ['GET', 'POST'])
def search_restaurant_results():
	"""
	customer_id: login required
	return restaurants whose name including search_key and the dishes
	if results more than PAGINATION_PER_PAGE, will return the related page
	:return: json
	{"customer_id": customer_id, 
	"result_list":[{"restaurant_id": restaurant_id, "owner_nickname": owner_nickname, 
					"owner_password": owner_password, "restaurant_name": restaurant_name,
	 				"restaurant_address": restaurant_address, "delivery_fee": delivery_fee, 
	 				"base_deliver_price": base_deliver_price, "time_span": time_span,
	 				"open_time": open_time, "total_month_sale": total_month_sale, 
	 				"restaurant_description": restaurant_description},
	 				{}, {}...]
	 "total_result": total_result, 
	 "total_page": total_page}
	"""
	customer_id = request.args.get("customer_id")
	page = int(request.args.get("page")) - 1
	search_value = request.args.get("search_value")
	search_value = urllib.unquote(str(search_value))
	try:
		result = g.cursor.execute("SELECT * FROM restaurant WHERE restaurant_name LIKE '%%%s%%'"
		                          % (search_value)).fetchall()
		total_result = len(result)
		total_page = total_result / PAGINATION_PER_PAGE + 1
		restaurant_result = []
		selected_result = result[page * PAGINATION_PER_PAGE: (page+1) * PAGINATION_PER_PAGE]
		for res in selected_result:
			restaurant_result.append(jsonify_restaurant(res))
		return jsonify({"customer_id": customer_id, "result_list":restaurant_result,
		                "total_result": total_result, "total_page": total_page})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Search failed, please try again later..."})

@app.route('/search_dish_results', methods = ['GET', 'POST'])
def search_dish_results():
	"""
	customer_id: login required
	return dishes whose name including search_key and the corresponding restaurant
	if results more than PAGINATION_PER_PAGE, will return the related page
	:return: json
	{"customer_id": customer_id, 
	"result_list":[{"dish_id": dish_id, "dish_name": dish_name, "restaurant_id": restaurant_id, 
					"dish_price": dish_price, "dish_month_sale": dish_month_sale,
					"restaurant_name": restaurant_name},
					{}, {}...]
	 "total_result": total_result, 
	 "total_page": total_page}
	"""
	customer_id = request.args.get("customer_id")
	page = int(request.args.get("page")) - 1
	search_value = request.args.get("search_value")
	search_value = urllib.unquote(str(search_value))
	try:
		result = g.cursor.execute("SELECT dish_id, dish_name, dish.restaurant_id, dish_price, dish_month_sale, "
		                          "restaurant_name FROM dish, restaurant WHERE dish_name LIKE '%%%s%%' "
		                          "AND dish.restaurant_id = restaurant.restaurant_id AND NOT deleted"
		                          % (search_value)).fetchall()
		total_result = len(result)
		total_page = total_result / PAGINATION_PER_PAGE + 1
		dish_result = []
		selected_result = result[page * PAGINATION_PER_PAGE: (page+1) * PAGINATION_PER_PAGE]
		for res in selected_result:
			dish_result.append(jsonify_dish_with_restaurant_name(res))
		return jsonify({"customer_id": customer_id, "result_list":dish_result,
		                "total_result": total_result, "total_page": total_page})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Search failed, please try again later..."})

@app.route('/search_restaurant_results_by_price', methods = ['GET','POST'])
def search_restaurant_results_by_price():
	"""
	customer_id: login required
	return restaurants whose name including search_key and the dishes ASCEND BY base_deliver_price
	if results more than PAGINATION_PER_PAGE, will return the related page
	:return: json
	{"customer_id": customer_id, 
	"result_list":[{"restaurant_id": restaurant_id, "owner_nickname": owner_nickname, 
					"owner_password": owner_password, "restaurant_name": restaurant_name,
					"restaurant_address": restaurant_address, "delivery_fee": delivery_fee, 
					"base_deliver_price": base_deliver_price, "time_span": time_span,
					"open_time": open_time, "total_month_sale": total_month_sale, 
					"restaurant_description": restaurant_description},
					{}, {}...]
	 "total_result": total_result, 
	 "total_page": total_page}
	"""
	customer_id = request.args.get("customer_id")
	page = int(request.args.get("page")) - 1
	search_value = request.args.get("search_value")
	search_value = urllib.unquote(str(search_value))
	try:
		result = g.cursor.execute("SELECT * FROM restaurant WHERE restaurant_name LIKE '%%%s%%' "
		                          "ORDER BY base_deliver_price" % (search_value)).fetchall()
		total_result = len(result)
		total_page = total_result / PAGINATION_PER_PAGE + 1
		restaurant_result = []
		selected_result = result[page * PAGINATION_PER_PAGE: (page + 1) * PAGINATION_PER_PAGE]
		for res in selected_result:
			restaurant_result.append(jsonify_restaurant(res))
		return jsonify({"customer_id": customer_id, "result_list": restaurant_result,
		                "total_result": total_result, "total_page": total_page})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Search failed, please try again later..."})

@app.route('/search_restaurant_results_by_sale', methods = ['GET','POST'])
def search_restaurant_results_by_sale():
	"""
	customer_id: login required
	return restaurants whose name including search_key and the dishes DESCEND BY total_month_sale
	if results more than PAGINATION_PER_PAGE, will return the related page
	:return: json
	{"customer_id": customer_id, 
	"result_list":[{"restaurant_id": restaurant_id, "owner_nickname": owner_nickname, 
					"owner_password": owner_password, "restaurant_name": restaurant_name,
					"restaurant_address": restaurant_address, "delivery_fee": delivery_fee, 
					"base_deliver_price": base_deliver_price, "time_span": time_span,
					"open_time": open_time, "total_month_sale": total_month_sale, 
					"restaurant_description": restaurant_description},
					{}, {}...]
	 "total_result": total_result, 
	 "total_page": total_page}
	"""
	customer_id = request.args.get("customer_id")
	page = int(request.args.get("page")) - 1
	search_value = request.args.get("search_value")
	search_value = urllib.unquote(str(search_value))
	try:
		result = g.cursor.execute("SELECT * FROM restaurant WHERE restaurant_name LIKE '%%%s%%' "
		                          "ORDER BY total_month_sale DESC" % (search_value)).fetchall()
		total_result = len(result)
		total_page = total_result / PAGINATION_PER_PAGE + 1
		restaurant_result = []
		selected_result = result[page * PAGINATION_PER_PAGE: (page + 1) * PAGINATION_PER_PAGE]
		for res in selected_result:
			restaurant_result.append(jsonify_restaurant(res))
		return jsonify({"customer_id": customer_id, "result_list": restaurant_result,
		                "total_result": total_result, "total_page": total_page})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Search failed, please try again later..."})

@app.route('/search_dish_results_by_price', methods = ['GET', 'POST'])
def search_dish_results_by_price():
	"""
	customer_id: login required
	return dishes whose name including search_key and the corresponding restaurant ASCEND BY dish_price
	if results more than PAGINATION_PER_PAGE, will return the related page
	:return: json
	{"customer_id": customer_id, 
	"result_list":[{"dish_id": dish_id, "dish_name": dish_name, "restaurant_id": restaurant_id, 
					"dish_price": dish_price, "dish_month_sale": dish_month_sale,
					"restaurant_name": restaurant_name},
					{}, {}...]
	 "total_result": total_result, 
	 "total_page": total_page}
	"""
	customer_id = request.args.get("customer_id")
	page = int(request.args.get("page")) - 1
	search_value = request.args.get("search_value")
	search_value = urllib.unquote(str(search_value))
	try:
		result = g.cursor.execute("SELECT dish_id, dish_name, dish.restaurant_id, dish_price, dish_month_sale, "
		                          "restaurant_name FROM dish, restaurant WHERE dish_name LIKE '%%%s%%' "
		                          "AND dish.restaurant_id = restaurant.restaurant_id AND NOT deleted "
		                          "ORDER BY dish_price" % (search_value)).fetchall()
		total_result = len(result)
		total_page = total_result / PAGINATION_PER_PAGE + 1
		dish_result = []
		selected_result = result[page * PAGINATION_PER_PAGE: (page+1) * PAGINATION_PER_PAGE]
		for res in selected_result:
			dish_result.append(jsonify_dish_with_restaurant_name(res))
		return jsonify({"customer_id": customer_id, "result_list":dish_result,
		                "total_result": total_result, "total_page": total_page})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Search failed, please try again later..."})

@app.route('/search_dish_results_by_sale', methods = ['GET', 'POST'])
def search_dish_results_by_sale():
	"""
	customer_id: login required
	return dishes whose name including search_key and the corresponding restaurant DESCEND BY dish_month_sale
	if results more than PAGINATION_PER_PAGE, will return the related page
	:return: json
	{"customer_id": customer_id, 
	"result_list":[{"dish_id": dish_id, "dish_name": dish_name, "restaurant_id": restaurant_id, 
					"dish_price": dish_price, "dish_month_sale": dish_month_sale,
					"restaurant_name": restaurant_name},
					{}, {}...]
	 "total_result": total_result, 
	 "total_page": total_page}
	"""
	customer_id = request.args.get("customer_id")
	page = int(request.args.get("page")) - 1
	search_value = request.args.get("search_value")
	search_value = urllib.unquote(str(search_value))
	try:
		result = g.cursor.execute("SELECT dish_id, dish_name, dish.restaurant_id, dish_price, dish_month_sale, "
		                          "restaurant_name FROM dish, restaurant WHERE dish_name LIKE '%%%s%%' "
		                          "AND dish.restaurant_id = restaurant.restaurant_id AND NOT deleted "
		                          "ORDER BY dish_month_sale DESC " % (search_value)).fetchall()
		total_result = len(result)
		total_page = total_result / PAGINATION_PER_PAGE + 1
		dish_result = []
		selected_result = result[page * PAGINATION_PER_PAGE: (page+1) * PAGINATION_PER_PAGE]
		for res in selected_result:
			dish_result.append(jsonify_dish_with_restaurant_name(res))
		return jsonify({"customer_id": customer_id, "result_list":dish_result,
		                "total_result": total_result, "total_page": total_page})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Search failed, please try again later..."})

@app.route('/get_restaurant_detail', methods = ['GET', 'POST'])
def get_restaurant_detail():
	"""
	:return: json
	{"restaurant": {"restaurant_id": restaurant_id, "owner_nickname": owner_nickname, 
					"owner_password": owner_password, "restaurant_name": restaurant_name,
	 				"restaurant_address": restaurant_address, "delivery_fee": delivery_fee, 
	 				"base_deliver_price": base_deliver_price, "time_span": time_span,
	 				"open_time": open_time, "total_month_sale": total_month_sale, 
	 				"restaurant_description": restaurant_description}
	 "dishes": [{"dish_id": dish_id, "dish_name": dish_name, "restaurant_id": restaurant_id, 
	 			 "dish_price": dish_price, "dish_month_sale": dish_month_sale}, 
	 			 {}, {}...] }
	"""
	restaurant_id = request.args.get("restaurant_id")
	try:
		restaurant = g.cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = '%s'"
		                              % (restaurant_id)).fetchall()
		if restaurant:
			dish_list = []
			dish_result = g.cursor.execute("SELECT  dish_id, dish_name, dish.restaurant_id, "
			                               "dish_price, dish_month_sale FROM dish, restaurant "
			                               "WHERE dish.restaurant_id = restaurant.restaurant_id "
			                               "AND restaurant.restaurant_id = '%s' AND NOT deleted"
			                               % (restaurant_id)).fetchall()
			for dish in dish_result:
				dish_list.append(jsonify_dish(dish))
			return jsonify({"restaurant": jsonify_restaurant(restaurant[0]), "dish": dish_list})
		else:
			return jsonify({"ERROR": "restaurant doesn't exist!"})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Can't get restaurant details, please try again later..."})

### Customer: create/receive/comment/delete an order ###

@app.route('/submit_order', methods=['GET', 'POST'])
def submit_order():
	"""
	insert into customer_order and dish_order at the same time
	:return: succeed or ERROR
	"""
	dish_counts = request.args.get("dish_counts")
	dish_counts = dict(eval(dish_counts))
	dish_counts = {dish: count for dish, count in dish_counts.items() if count}
	customer_id = request.args.get("customer_id")
	restaurant_id = request.args.get("restaurant_id")
	customer_order_id = get_customer_order_no()
	try:
		g.cursor.execute("INSERT INTO customer_order VALUES('%s', '%s', '%s', '%s', NULL, NULL);"
		                 % (restaurant_id, customer_id, customer_order_id,
		                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		g.cursor.execute("UPDATE restaurant SET total_month_sale = total_month_sale + '%d' "
						 "WHERE restaurant_id = '%s'" % (sum(dish_counts.values()), restaurant_id))
		for order, count in dish_counts.items():
			dish_order_id = get_dish_order_no()
			g.cursor.execute("INSERT INTO dish_order VALUES('%s', '%s', '%s', '%d');"
			                 % (dish_order_id, customer_order_id, order, int(count)))
			g.cursor.execute("UPDATE dish SET dish_month_sale = dish_month_sale + '%d' "
							 "WHERE dish_id = '%s'" % (count, order))
		g.conn.commit()
		return jsonify({"succeed!": "succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR":"Submit order failed, please try again later.."})

@app.route('/receive_order', methods=['GET', 'POST'])
def receive_order():
	"""
	insert receive_time into database
	:return: succeed or ERROR
	"""
	order_id = request.args.get("order_id")
	order_id = '0' * (3 - len(order_id)) + order_id
	try:
		g.cursor.execute("UPDATE customer_order SET receive_time = '%s' WHERE order_id = '%s'"
		                 % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), order_id))
		g.conn.commit()
		return jsonify({"succeed!": "succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Receive order failed, please try again later.."})

@app.route('/comment_order', methods=['GET', 'POST'])
def comment_order():
	"""
	insert comment into database
	:return: succeed or ERROR
	"""
	order_id = request.args.get("order_id")
	order_id = '0' * (3 - len(order_id)) + order_id
	comment = request.args.get("comment")
	try:
		g.cursor.execute("UPDATE customer_order SET comment = '%s' WHERE order_id = '%s'"
		                 % (comment, order_id))
		g.conn.commit()
		return jsonify({"succeed!": "succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Comment order failed, please try again later.."})

@app.route('/delete_order', methods=['GET', 'POST'])
def delete_order():
	"""
	delete order from database
	will delete customer_order and dish_order at the same time in `cascade` mode
	:return: succeed or ERROR
	"""
	order_id = request.args.get("order_id")
	try:
		# in sqlite3, PRAGMA foreign_keys = OFF is default
		g.cursor.execute("PRAGMA foreign_keys = ON")
		g.cursor.execute("DELETE FROM customer_order WHERE order_id = '%s'" % (order_id))
		g.conn.commit()
		return jsonify({"succeed!": "succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Delete order failed, please try again later.."})

### Customer: view order history ###

@app.route('/get_user_history', methods= ['GET', 'POST'])
def get_user_history():
	"""
	:return: json
	[{"restaurant_id":restaurant_id, "order_id": order_id, "create_time": create_time, 
	  "receive_time":receive_time, "restaurant_name":restaurant_name,
	  "order_total_price":order_total_price, 
	  "comment": comment,
	  "dishes":[{"dish_price": dish_price, "dish_amount": dish_amount, "dish_name":dish_name}, {}, {}..]
	 },
	 {}, {}, ...]
	"""
	customer_id = request.args.get("customer_id")
	try:
		customer_order = g.cursor.execute("SELECT customer_order.restaurant_id, customer_order.order_id, "
		                                  "customer_order.create_time, customer_order.receive_time, customer_order.comment "
		                                  "FROM customer_order WHERE customer_id = '%s'" % (customer_id)).fetchall()
		if customer_order:
			order_list = []
			for order in customer_order:
				keywords = ["restaurant_id", "order_id", "create_time", "receive_time", "comment"]
				order_dict = dict(zip(keywords, order))
				restaurant_name = g.cursor.execute("SELECT restaurant_name FROM restaurant "
				                                   "WHERE restaurant_id = '%s'" % (order[0])).fetchall()
				order_dict["restaurant_name"] = restaurant_name[0][0]
				dish_details = g.cursor.execute("SELECT dish.dish_name, dish.dish_price, dish_order.count "
				                                "FROM dish, dish_order, customer_order "
				                                "WHERE customer_order.order_id = dish_order.order_id "
				                                "AND dish_order.dish_id = dish.dish_id "
				                                "AND customer_order.order_id = '%s'"
				                                % (order_dict["order_id"])).fetchall()
				order_total_price = sum(map(lambda x: x[1] * x[2], dish_details))
				order_dict["order_total_price"] = order_total_price
				dish_list = []
				for dish in dish_details:
					dish_list.append(dict(zip(("dish_name", "dish_price", "dish_amount"), dish)))
				order_dict["dishes"] = dish_list
				order_list.append(order_dict)
			return jsonify({"result":order_list})
		else:
			return jsonify({"ERROR": "No orders! Don't you want to eat some?"})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Get user history failed, please try again later.."})

### Restaurant: signup/signin ###

@app.route('/restaurant_signup_submit', methods = ['GET', 'POST'])
def restaurant_signup_submit():
	"""
	create a new restaurant in database
	owner_nickname must be unique， password and restaurant_name is required
	:return: json
	{"restaurant_id": restaurant_id, "owner_nickname": owner_nickname,
	 "restaurant_name": restaurant_name}
	"""
	owner_nickname = request.args.get("owner_nickname")
	restaurant_name = request.args.get("restaurant_name")
	owner_password = request.args.get("owner_password")
	owner_password = md5_encrypt(owner_password)
	restaurant_id = get_restaurant_no()
	try:
		user_exist = g.cursor.execute("SELECT * FROM restaurant WHERE owner_nickname = '%s'"
		                              % (owner_nickname)).fetchall()
		if user_exist:
			return jsonify({"ERROR": "This nickname has been registered, you can sign in now."})
		g.cursor.execute("INSERT INTO restaurant VALUES ('%s', '%s', '%s', '%s', NULL, NULL, "
		                 "NULL, NULL, NULL, 0, NULL)"
						 % (restaurant_id, owner_nickname, owner_password, restaurant_name))
		g.conn.commit()
		return jsonify({"restaurant_id": restaurant_id, "owner_nickname": owner_nickname,
		                "restaurant_name": restaurant_name})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Registration failed! Please try again..."})

@app.route('/restaurant_signin_submit', methods = ['GET', 'POST'])
def restaurant_signin_submit():
	"""
	comapre password provided by restaurant owner and password stored in database
	if equal: return restaurant's detail
	else return ERROR
	:return: json
	{"restaurant_id": restaurant_id, "owner_nickname": owner_nickname, 
	 "owner_password": owner_password, "restaurant_name": restaurant_name,
	 "restaurant_address": restaurant_address, "delivery_fee": delivery_fee, 
	 "base_deliver_price": base_deliver_price, "time_span": time_span,
	 "open_time": open_time, "total_month_sale": total_month_sale, 
	 "restaurant_description": restaurant_description }
	"""
	owner_nickname = request.args.get("owner_nickname")
	owner_password = request.args.get("owner_password")
	owner_password = md5_encrypt(owner_password)
	try:
		result = g.cursor.execute("SELECT * FROM restaurant WHERE owner_nickname = '%s'" % (owner_nickname)).fetchall()
		if result:
			db_password = result[0][2]
			if owner_password == db_password:
				return jsonify(jsonify_restaurant(result[0]))
			else:
				return jsonify({"ERROR": "Wrong owner_nickname or password."})
		else:
			return jsonify({"ERROR": "Restaurant not exist."})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Sign in failed, please try again later."})

### Restaurant: profile ###

@app.route('/upload_restaurant_profile', methods=['GET', 'POST'])
def upload_restaurant_profile():
	"""
	change restaurant details including name, address, delivery_price, base_deliver_price, 
	open_time and description
	:return: succeed or ERROR
	"""
	restaurant_id = request.args.get("restaurant_id")
	restaurant_name = request.args.get("restaurant_name")
	restaurant_address = request.args.get("restaurant_address")
	delivery_price = request.args.get("delivery_price")
	base_deliver_price = request.args.get("base_deliver_price")
	open_time = request.args.get("open_time")
	restaurant_description = request.args.get("restaurant_description")
	try:
		g.cursor.execute("UPDATE restaurant SET restaurant_name = '%s', restaurant_address = '%s', "
		                 "delivery_price = '%s', base_deliver_price = '%s', open_time = '%s', "
		                 "restaurant_description = '%s' WHERE restaurant_id = '%s'"
		                 % (restaurant_name, restaurant_address, delivery_price, base_deliver_price, open_time,
		                    restaurant_description, restaurant_id))
		g.conn.commit()
		updated_profile = g.cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = '%s'"
		                                   % (restaurant_id)).fetchall()
		return jsonify(jsonify_restaurant(updated_profile[0]))
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Update profile failed, please try again later.."})

@app.route('/change_restaurant_password', methods=['GET', 'POST'])
def change_restaurant_password():
	"""
	change password for restaurant owner, updated password is encrypted in database
    :return: succeed or ERROR
    """
	restaurant_id = request.args.get("restaurant_id")
	old_password = request.args.get("old_password")
	old_password = md5_encrypt(old_password)
	new_password = request.args.get("new_password")
	new_password = md5_encrypt(new_password)
	try:
		old_password_db = g.cursor.execute("SELECT owner_password FROM restaurant WHERE restaurant_id = '%s'"
										   % (restaurant_id)).fetchall()[0][0]
		if old_password == old_password_db:
			g.cursor.execute("UPDATE restaurant SET owner_password = '%s' WHERE restaurant_id = '%s'"
							 % (new_password, restaurant_id))
			g.conn.commit()
			return jsonify({"Succeed!": "Change password Succeed!"})
		else:
			return jsonify({"ERROR": "Please input correct old password!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Change password failed, please try again later.."})

### Restaurant: dish management ###

@app.route('/add_dish', methods = ['GET', 'POST'])
def add_dish():
	"""
	add a dish to database: dish_name, dish_price is required
	dish name can't be repeated in a restaurant
	:return: succeed or ERROR
	"""
	dish_name = request.args.get("dish_name")
	restaurant_id = request.args.get("restaurant_id")
	dish_price = request.args.get("dish_price")
	try:
		if not dish_price.replace('.', '').isdigit():
			return jsonify({"ERROR": "Please input valid price!"})
		dish_names = g.cursor.execute("SELECT dish_name FROM dish WHERE restaurant_id = '%s' "
									  "AND NOT deleted" % (restaurant_id)).fetchall()
		dish_names = [x[0] for x in dish_names]
		if dish_name in dish_names:
			return jsonify({"ERROR": "Dish name duplicated, select a new one!"})
		dish_id = get_dish_no(restaurant_id)
		g.cursor.execute("INSERT INTO dish VALUES('%s','%s', '%s', '%f', '%d', '%d');"
		                 % (dish_id, dish_name, restaurant_id, float(dish_price), 0, 0))
		g.conn.commit()
		return jsonify({"succeed!": "succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "New dish created failed, please try again later"})

@app.route('/change_dish', methods=['GET', 'POST'])
def change_dish():
	"""
	change dish price or name
	:return: succeed or ERROR
	"""
	dish_id = request.args.get("dish_id")
	dish_price = request.args.get("dish_price")
	dish_name = request.args.get("dish_name")
	try:
		if not dish_price.replace('.', '').isdigit():
			return jsonify({"ERROR": "Please input valid price!"})
		restaurant_id = dish_id[:3]
		dish_names = g.cursor.execute("SELECT dish_name FROM dish WHERE restaurant_id = '%s'"
									  % (restaurant_id)).fetchall()
		dish_names = [x[0] for x in dish_names]
		old_dish_name = g.cursor.execute("SELECT dish_name FROM dish WHERE dish_id = '%s' "
										 "AND NOT deleted" % (dish_id)).fetchall()[0][0]
		if dish_name != old_dish_name and dish_name in dish_names:
			return jsonify({"ERROR": "Dish name duplicated, select a new one!"})
		g.cursor.execute("UPDATE dish SET dish_price = '%f', dish_name = '%s'  WHERE dish_id = '%s'"
		                 % (float(dish_price), dish_name, dish_id))
		g.conn.commit()
		updated_dish = g.cursor.execute("SELECT * FROM dish WHERE dish_id = '%s'" % (dish_id)).fetchall()
		return jsonify(jsonify_dish(updated_dish[0]))
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Update dish failed, please try again later.."})

@app.route('/delete_dish', methods=['GET', 'POST'])
def delete_dish():
	"""
	"delete" a dish from database: set the deleted BOOL to True
	deleted dishes will neither show up in restaurant homepage nor be searched,
	but orders including the deleted dish will not be deleted
	:return: succeed or ERROR
	"""
	dish_id = request.args.get("dish_id")
	try:
		g.cursor.execute("UPDATE dish SET deleted = 1 WHERE dish_id = '%s'" % (dish_id))
		g.conn.commit()
		return jsonify({"succeed!": "succeed!"})
	except Exception as e:
		g.conn.rollback()
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Dish delete failed, please try again later.."})

### Restaurant: view order history ###

@app.route('/get_restaurant_history', methods=['GET', 'POST'])
def get_restaurant_history():
	"""
	:return: json
	[{"customer_nickname":customer_nickname, "create_time":create_time, "receive_time":receive_time,
	 "comment":comment, "order_total_price":order_total_price, 
	 "dishes":[{"dish_price": dish_price, "dish_amount": dish_amount, "dish_name":dish_name}, {}, {}..]
	 },
	 {}, {}, ...]
	"""
	restaurant_id = request.args.get("restaurant_id")
	try:
		restaurant_order = g.cursor.execute("SELECT customer_order.customer_id, customer_order.order_id, "
		                                    "customer_order.create_time, customer_order.receive_time, "
		                                    "customer_order.comment "
		                                    "FROM customer_order WHERE restaurant_id = '%s'"
		                                    % (restaurant_id)).fetchall()
		if restaurant_order:
			order_list = []
			for order in restaurant_order:
				keywords = ["customer_nickname", "order_id", "create_time", "receive_time", "comment"]
				order_dict = dict(zip(keywords, order))
				customer_nickname = g.cursor.execute("SELECT customer_nickname FROM customer "
				                                     "WHERE customer_id = '%s'" % (order[0])).fetchall()
				order_dict["customer_nickname"] = customer_nickname[0][0]
				dish_details = g.cursor.execute("SELECT dish.dish_name, dish.dish_price, dish_order.count "
				                                "FROM dish, dish_order, customer_order "
				                                "WHERE customer_order.order_id = dish_order.order_id "
				                                "AND dish_order.dish_id = dish.dish_id "
				                                "AND customer_order.order_id = '%s'"
				                                % (order_dict["order_id"])).fetchall()
				order_total_price = sum(map(lambda x: x[1] * x[2], dish_details))
				order_dict["order_total_price"] = order_total_price
				dish_list = []
				for dish in dish_details:
					dish_list.append(dict(zip(("dish_name", "dish_price", "dish_amount"), dish)))
				order_dict["dishes"] = dish_list
				order_list.append(order_dict)
			return jsonify({"result":order_list})
		else:
			return jsonify({"ERROR": "No orders! Your business is so poor.."})
	except Exception as e:
		print traceback.format_exc(e)
		return jsonify({"ERROR": "Get restaurant history failed, please try again later.."})
