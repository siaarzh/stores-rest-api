import psycopg2
from config import config

'''
small comment for commit
NOTE: Disconnect PyCharm connection before running this script
'''

params = config()
connection = psycopg2.connect(**params)

cursor = connection.cursor()

delete_table = 'DROP TABLE IF EXISTS users'
cursor.execute(delete_table)

delete_table = 'DROP TABLE IF EXISTS items'
cursor.execute(delete_table)

print("dropped table")

# Create users
create_table = "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, " \
               "username VARCHAR (50) UNIQUE," \
               " password VARCHAR (8) NOT NULL)"
cursor.execute(create_table)
print("created table users")

user = ('serzhan', 'password')
insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
cursor.execute(insert_query, user)
print("inserted {} into table".format(user[1]))

users = [
    ('rolf', 'asdf'),
    ('john', 'zxcv')
]
cursor.executemany(insert_query, users)
for user in users:
    print("inserted {} into table".format(user[1]))

select_query = 'SELECT * FROM users'
username = "serzhan"
cursor.execute(select_query)
row = cursor.fetchone()

while row is not None:
    print("\nFetched : \n{}\n".format(row))
    row = cursor.fetchone()

# Create items
create_table = "CREATE TABLE IF NOT EXISTS items (name VARCHAR (50) PRIMARY KEY," \
               " price REAL)"
cursor.execute(create_table)
print("created table items")

item = ('table', 12.99)
insert_query = "INSERT INTO items (name, price) VALUES (%s, %s)"
cursor.execute(insert_query, item)
print("inserted {} into table".format(item[0]))

connection.commit()  # saves data
print('commit achieved')
connection.close()  # closes connection resources
print("connection closed")
