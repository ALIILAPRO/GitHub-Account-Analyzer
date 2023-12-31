import os
import requests
import sqlite3
from github import Github
from datetime import datetime

def CreateDB(name):
	connection = sqlite3.connect(name)
	cursor = connection.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id TEXT DEFAULT NULL,
		name TEXT DEFAULT NULL,
		username TEXT DEFAULT NULL,
		user_type TEXT DEFAULT NULL,
		created_at TEXT DEFAULT NULL,
		bio TEXT DEFAULT NULL,
		location TEXT DEFAULT NULL,
		blog TEXT DEFAULT NULL,
		email TEXT DEFAULT NULL,
		avatar_url TEXT DEFAULT NULL
	);""")
	connection.commit()
	connection.close()
		
def CreateFolder(name):
	if not os.path.isdir(name):
		try:
			os.mkdir(name)
		except Exception as error:
			print(error)

# Enter your token
access_token = ""
g = Github(access_token)

def get_user_choice():
	while True:
		choice = input("Enter '1' to get followers or '2' to get following: ")
		if choice == '1' or choice == '2':
			return choice
		else:
			print("Invalid choice. Please enter '1' or '2'.")

userinput = input("Enter the Username of Github: ")

if os.path.isdir(f"./{userinput}"):
	print("Folder with the username already exists.")
	create_new = input("Do you want to create a new folder? (y=yes /n=no /c=yes with custom name): ").lower()
	if create_new == 'n':
		followers_folder = f"./{userinput}/followers"
		following_folder = f"./{userinput}/following"
		folder = f"./{userinput}"
		type_db = 'update'
	elif create_new == 'y':
		now = datetime.now().strftime("%Y%m%d%H%M%S")
		new_folder_name = f"{userinput}_{now}"
		folder = f"./{new_folder_name}"
		followers_folder = f"./{new_folder_name}/followers"
		following_folder = f"./{new_folder_name}/following"
		type_db = 'create'
	elif create_new == 'c':
		new_folder_name = input("Enter new folder name: ")
		folder = f"./{new_folder_name}"
		followers_folder = f"./{new_folder_name}/followers"
		following_folder = f"./{new_folder_name}/following"
		type_db = 'create'
else:
	folder = f"./{userinput}"
	followers_folder = f"./{userinput}/followers"
	following_folder = f"./{userinput}/following"
	type_db = 'new'

CreateFolder(folder)

user = g.get_user(userinput)

user_choice = get_user_choice()

if user_choice == '1':
	followers = user.get_followers()
	print("Getting followers...")
	CreateFolder(followers_folder)
	folder = f"./{followers_folder}/Profile Picture"
	CreateFolder(folder)
	db_name = (f"{followers_folder}/followers.db")
else:
	followers = user.get_following()
	print("Getting following...")
	CreateFolder(following_folder)
	folder = f"./{following_folder}/Profile Picture"
	CreateFolder(folder)
	db_name = (f"{following_folder}/following.db")
	
CreateDB(db_name)

connection = sqlite3.connect(db_name)
cursor = connection.cursor()

print("In progress...")

for follower in followers:
	user_id = follower.id
	name = follower.name
	username = follower.login
	user_type = follower.type
	created_at = follower.created_at
	bio = follower.bio
	location = follower.location
	blog = follower.blog
	email = follower.email
	avatar_url = follower.avatar_url

	if type_db == 'update':
		cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
		result = cursor.fetchone()
		if not result:
			cursor.execute('INSERT INTO users (user_id, name, username, user_type, created_at, bio, location, blog, email, avatar_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				   (user_id, name, username, user_type, created_at, bio, location, blog, email, avatar_url))
			connection.commit()

			response = requests.get(avatar_url)
			with open(os.path.join(folder, f'{username}.png'), 'wb') as file:
				file.write(response.content)

	elif type_db == 'create':
		cursor.execute('INSERT INTO users (user_id, name, username, user_type, created_at, bio, location, blog, email, avatar_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				(user_id, name, username, user_type, created_at, bio, location, blog, email, avatar_url))
		connection.commit()

		response = requests.get(avatar_url)
		with open(os.path.join(folder, f'{username}.png'), 'wb') as file:
			file.write(response.content)

	elif type_db == 'new':
		cursor.execute('INSERT INTO users (user_id, name, username, user_type, created_at, bio, location, blog, email, avatar_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				(user_id, name, username, user_type, created_at, bio, location, blog, email, avatar_url))
		connection.commit()

		response = requests.get(avatar_url)
		with open(os.path.join(folder, f'{username}.png'), 'wb') as file:
			file.write(response.content)

connection.close()
print("Done.")