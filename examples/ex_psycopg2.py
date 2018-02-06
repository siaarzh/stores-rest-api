'''
This file follows the Udemy API with Flask and Python course:
section: 5
video: 65
'''

import psycopg2

connection = psycopg2.connect("dbname=flask_tutorial user=postgres password=password")

cursor = connection.cursor()

delete_table = 'DROP TABLE IF EXISTS "users";'
cursor.execute(delete_table)
print("dropped table")

create_table = "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, username VARCHAR (50) UNIQUE, password VARCHAR (8) NOT NULL)"
cursor.execute(create_table)
print("created table")


user = (1, 'serzhan', 'password')
insert_query = "INSERT INTO users VALUES (%s, %s, %s)"
cursor.execute(insert_query, user)
print("inserted {} into table".format(user[1]))


users = [
	(2, 'rolf', 'asdf'),
	(3, 'john', 'zxcv')
]
cursor.executemany(insert_query, users)
for user in users:
	print("inserted {} into table".format(user[1]))

select_query = 'SELECT * FROM "users"'
cursor.execute(select_query)
row = cursor.fetchone

while row is not None:
	print(row)
	row = cursor.fetchone()

connection.commit() # saves data
print('commit achieved')
connection.close() # closes connection resources
print("connection closed")