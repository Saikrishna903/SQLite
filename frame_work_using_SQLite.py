#Frame work program using sqlite3 library
import sqlite3
menu_cfg_file_name = "menu.cfg"
file_not_found_error_message = "File not found or error in opening the file"
try:
	with open(menu_cfg_file_name) as menu_file_object:
		menu = menu_file_object.read()
	menu_file_object.close()
except FileNotFoundError:
	print(file_not_found_error_message)
try:
	with open("messages.cfg") as messages_file_object:
		messages = messages_file_object.read()
		messages = eval(messages)
	messages_file_object.close()
except FileNotFoundError:
	print(file_not_found_error_message)
connection = sqlite3.connect("framework.db")
field_names_with_data_type = connection.execute("PRAGMA table_info(my_table)")
message_index_number = 0
field_names = []
for field_name in field_names_with_data_type:
	if field_name[1] != 'Status':
		field_names.append(field_name[1])

def create_record():
	field_values = []
	field_values.append('A')
	for field_name in field_names:
		print(field_name + ": " , end = "")
		field_value = input()
		field_values.append(field_value)
	field_values_tuple = tuple(field_values)
	insert_query = "INSERT INTO my_table VALUES" + str(field_values_tuple)
	connection.execute(insert_query)
	connection.commit()
	print(messages[message_index_number])

def print_records():
	cursor_object = connection.execute("SELECT * FROM my_table WHERE Status = 'A'")
	records =  cursor_object.fetchall()
	for record in records:
		print_field_values(record)

def print_field_values(record):
	index_number = 1
	for field_name in field_names:
		print(field_name + ": " , end = "")
		print(record[index_number])
		index_number += 1
	print('-' * 30)

def search_record():
	key_value = get_key_value()
	if get_record_present_status(key_value):
		cursor_object = connection.execute("SELECT * FROM my_table WHERE Status = 'A' AND " + str(field_names[0]) + " = " + str(key_value))
		record =  cursor_object.fetchone()
		print_field_values(record)
	else:
		print(messages[len(messages) - 1])	


def get_key_value():
	return input("Enter " + field_names[0] + ": ")

def get_record_present_status(key_value):
	record_found_status = False
	query = "SELECT * FROM my_table WHERE Status = 'A' AND " + str(field_names[0]) + " = " + str(key_value)
	cursor_object = connection.execute(query)
	record = cursor_object.fetchone()
	if not record:
		return False
	else:
		return True

def update_record():
	try:
		updatable_fields_object = open("updatablefields.cfg")
		updatable_fields = []
		for update_field in updatable_fields_object.read():
			update_field = int(update_field)
			updatable_fields.append(update_field)
		updatable_fields_object.close()
	except FileNotFoundError:
		print(file_not_found_error_message)
	key_value = get_key_value()
	if get_record_present_status(key_value) == True:
		index_number = 0
		print("Do you want to update: ")
		while index_number < len(updatable_fields):
			print(str((index_number + 1)) + "." + field_names[updatable_fields[index_number] - 1])
			index_number += 1
		try:
			update_option = input("Enter your option: ")
			update_option = int(update_option)
		except Exception: 
			print("INVALID OPTION")
		field_name = field_names[updatable_fields[update_option - 1] - 1]
		new_field_value = input("Enter new " + field_name + ": ")
		new_field_value = "\"" + new_field_value + "\""
		update_query = "UPDATE my_table SET " + str(field_name) + " = " + str(new_field_value) + " WHERE " + str(field_names[0]) + " = " + str(key_value)
		connection.execute(update_query)
		connection.commit()
		message_index_number += 1
		print(messages[message_index_number])
	else:
		print(messages[len(messages) - 1])

def delete_record():
	key_value = get_key_value()
	delete_query = "UPDATE my_table SET Status = 'D' WHERE " + str(field_names[0]) + " = " + str(key_value)
	delete_record_status = connection.execute(delete_query)
	connection.commit()
	if delete_record_status.rowcount:
		message_index_number += 1
		print(messages[message_index_number])
	else:
		print(messages[len(messages) - 1])

functions_list = [create_record, print_records, search_record, update_record, delete_record, exit]
while(True):
	print(menu)
	try:
		user_choice = input("Enter your choice to perform: ")
		user_choice = int(user_choice)
		if user_choice == 6:
			print("Do you really want to exit y or n?")
			exit_choice = input("Enter your exit choice: ")
			if exit_choice == 'Y' or exit_choice == 'y':
				print("Entered exit as your choice")
				connection.close()
				exit()
			else: 
				continue
		elif user_choice > 0 and user_choice < 6:
			functions_list[user_choice - 1]()
	except Exception:
		print("INVALID CHOICE")