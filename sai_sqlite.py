#Python program to use sqlite3 library
import sqlite3
import sys
from printy import printy
import subprocess
print("SQLite version 3.33.0 2020-08-14 13:23:32")
print("Enter \".help\" for usage hints.")
if len(sys.argv) == 2:
	DB_name = sys.argv[1]
else:
	print("Connected to a ", end = "")
	printy("transient in-memory database", "r", end = "")
	print(".")
	print("Use \".open FILENAME\" to reopen on a persistent database.")
	DB_name = "temp.db"
connection = sqlite3.connect(DB_name)
while True:
	query = input("sqlite3> ")
	if query[0] != '.':
		try:
			cursor_object = connection.execute(query)
			connection.commit()
			query_output = cursor_object.fetchall()
		except:
			while True:
				user_input = input("   ...> ")
				if user_input == ";":
					print("Error: near \"" + query + "\": syntax error")
					break
				else:
					continue
		if query_output != []:
			for record in query_output:
				count = len(record)
				for index in range(count):
					print(record[index], end = "")
					if index != count - 1:
						print("|", end = "")
				print()
	else:
		if query == '.quit':
			connection.close()
			exit()
		elif query[:5] == '.open':
			connection.close()
			DB_name = query[6:]
			connection = sqlite3.connect(DB_name)
		else:
			subprocess.run(['sqlite3', DB_name, query])