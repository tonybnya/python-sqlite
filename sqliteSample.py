import sqlite3
from sqlite3 import Error

# Sample function to create a connection with an SQLIte database
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('')
        print('----------------------------------------')
        print('-> Connection to SQLite DB successful!')
        print('----------------------------------------')
        print('')
    except Error as e:
        print('')
        print('----------------------------------------')
        print(f"-> The error '{e}' occured!")
        print('----------------------------------------')
        print('')

    return connection

# The connection object created by the function above is used to execute queries
connection = create_connection("./sample.sqlite")

# Sample function to execute queries in SQLite
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('')
        print('----------------------------------------')
        print('-> Query executed successfully!')
        print('----------------------------------------')
        print('')
    except Error as e:
        print('')
        print('----------------------------------------')
        print(f"-> The error '{e}' occured!")
        print('----------------------------------------')
        print('')

# Below, four queries to create different tables in a SQLite database
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
age INTEGER,
gender TEXT,
nationality TEXT
);
"""


create_posts_table = """
CREATE TABLE IF NOT EXISTS posts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


create_comments_table = """
CREATE TABLE IF NOT EXISTS comments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT NOT NULL,
user_id INTEGER NOT NULL,
post_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

create_likes_table = """
CREATE TABLE IF NOT EXISTS likes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
post_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

# Call of the execute_query() function to create these four tables
execute_query(connection, create_users_table)
execute_query(connection, create_posts_table)
execute_query(connection, create_comments_table)
execute_query(connection, create_likes_table)

# Below, four queries to insert records into the tables
create_users = """
INSERT INTO
users (name, age, gender, nationality)
VALUES
('James', 25, 'male', 'USA'),
('Leila', 32, 'female', 'France'),
('Brigitte', 35, 'female', 'England'),
('Mike', 40, 'male', 'Denmark'),
('Elizabeth', 21, 'female', 'Canada');
"""

create_posts = """
INSERT INTO
posts (title, description, user_id)
VALUES
("Happy", "I am feeling very happy today", 1),
("Hot Weather", "The weather is very hot today", 2),
("Help", "I need some help with my work", 2),
("Great News", "I am getting married", 1),
("Interesting Game", "It was a fantastic game of tennis", 5),
("Party", "Anyone uo for a late-night party today", 3);
"""

create_comments = """
INSERT INTO
comments (text, user_id, post_id)
VALUES
('Count me in', 1, 6),
('What sort of help', 5, 3),
('I was rooting for Nadala though', 4, 5),
('Help with your thesis?', 2, 3),
('Many congratulations', 5, 4);
"""

create_likes = """
INSERT INTO
likes (user_id, post_id)
VALUES
(1, 6),
(2, 3),
(1, 5),
(5, 4),
(2, 4),
(4, 2),
(3, 6);
"""

# Call of execute_query() to insert these records created above 
execute_query(connection, create_users)
execute_query(connection, create_posts)
execute_query(connection, create_comments)
execute_query(connection, create_likes)

# Sample function for selecting records into the SQLite database
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e} occured!'")

# Retrieve all the records from the users table
select_users = "SELECT * FROM users"
users = execute_read_query(connection, select_users)

print('')
print('----------------------------------------')
print('-> Below are all the records from users:')
print('')

for user in users:
    print(user)

print('----------------------------------------')

# Retrieve all the records from the posts table
select_posts = "SELECT * FROM posts"
posts = execute_read_query(connection, select_posts)

print('')
print('----------------------------------------')
print('-> Below are all the records from posts:')
print('')

for post in posts:
    print(post)

print('----------------------------------------')
print('')

# Retrieve data from two related tables
select_users_posts = """
SELECT
users.id,
users.name,
posts.description
FROM
posts
INNER JOIN users ON users.id = posts.user_id
"""

users_posts = execute_read_query(connection, select_users_posts)

print('----------------------------------------')
print('-> Retrieve data from users & posts:')
print('')

for users_post in users_posts:
    print(users_post)

print('----------------------------------------')
print('')

# Retrieve data from three related tables
select_posts_comments_users = """
SELECT
posts.description as post,
text as comment,
name
FROM
posts
INNER JOIN comments ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id
"""

posts_comments_users = execute_read_query(connection, select_posts_comments_users)

print('----------------------------------------')
print('-> Data from posts, comments & users:')
print('')

for posts_comments_user in posts_comments_users:
    print(posts_comments_user)

print('----------------------------------------')
print('')

