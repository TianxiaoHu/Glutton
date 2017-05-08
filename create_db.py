# -*- coding:utf-8 -*-
"""
Author: Tianxiao Hu
Last Modified: 2017.5.5
Email: hutianxiao_fdu@126.com
Project for Introduction to Database Systems(COMP130010.03)@Fudan University
"""
import  sqlite3
from config import SQLALCHEMY_DATABASE_LOC

def main():
	# connect to database
	conn = sqlite3.connect(SQLALCHEMY_DATABASE_LOC)
	cursor = conn.cursor()

	print 'Create table...'

	cursor.execute("""
CREATE TABLE restaurant(
restaurant_id CHAR(3) NOT NULL,
owner_nickname CHAR(20) NOT NULL UNIQUE,
owner_password CHAR(40) NOT NULL,
restaurant_name CHAR(50) NOT NULL,
restaurant_address CHAR(100),
delivery_price DECIMAL(5,2),
base_deliver_price DECIMAL(5,2),
time_span SMALLINT,
open_time  CHAR(20),
total_month_sale INTEGER,
restaurant_description CHAR(200),
PRIMARY KEY(restaurant_id)
);
""")

	cursor.execute("""
CREATE TABLE customer(
customer_id CHAR(3) NOT NULL,
customer_nickname CHAR(20) NOT NULL,
customer_password CHAR(40) NOT NULL,
customer_mobile_number CHAR(20) UNIQUE,
customer_address CHAR(100),
customer_description CHAR(100),
customer_appellation CHAR(20),
customer_avatar CHAR(20) NOT NULL,
PRIMARY KEY(customer_id)
);
""")

	cursor.execute("""CREATE TABLE dish(
dish_id CHAR(6) NOT NULL,
dish_name CHAR(30) NOT NULL,
restaurant_id CHAR(3) NOT NULL,
dish_price DECIMAL(5,2) NOT NULL,
dish_month_sale SMALLINT,
deleted BOOL,
PRIMARY KEY(dish_id),
FOREIGN KEY(restaurant_id)REFERENCES restaurant(restaurant_id)
);
""")

	cursor.execute("""CREATE TABLE customer_order(
restaurant_id CHAR(3) NOT NULL,
customer_id CHAR(3) NOT NULL,
order_id CHAR(3) NOT NULL,
create_time DATETIME NOT NULL,
receive_time DATETIME,
comment CHAR(100),
PRIMARY KEY(order_id),
FOREIGN KEY(restaurant_id)REFERENCES restaurant(restaurant_id),
FOREIGN KEY(customer_id)REFERENCES customer(customer_id)
);
""")

	cursor.execute("""CREATE TABLE dish_order(
dish_order_id CHAR(4) NOT NULL,
order_id CHAR(4) NOT NULL,
dish_id CHAR(6) NOT NULL,
count SMALLINT NOT NULL ,
PRIMARY KEY(dish_order_id),
FOREIGN KEY(order_id)REFERENCES customer_order(order_id) ON DELETE CASCADE,
FOREIGN KEY(dish_id)REFERENCES dish(dish_id)
);
""")

	conn.commit()

	# insert some restaurants and dishes
	f = open('insert.sql')

	line = f.readline()
	while line:
		cursor.execute(line)
		print line
		line = f.readline()
	conn.commit()

	cursor.close()
	conn.close()

if __name__ == '__main__':
	main()
