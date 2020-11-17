#Frame work program using sqlite3 library
import sqlite3
menu_cfg_file_name = "menu.cfg"
data_base_name_with_table_name_cfg_file_name = "DB_name_with_table_name.cfg"
updatable_fields_cfg_file_name = "updatablefields.cfg"
record_not_found_error_message = "NO RECORD FOUND"
file_not_found_error_message = "File not found or error in opening the file"
try:
	with open(menu_cfg_file_name) as menu_file_object:
		menu = menu_file_object.read()
	menu_file_object.close()
except FileNotFoundError:
	print(file_not_found_error_message)
try:
	with open(data_base_name_with_table_name_cfg_file_name) as data_base_object:
		data_base_name_with_table_name = data_base_object.read()
		data_base_name_with_table_name = eval(data_base_name_with_table_name)
	data_base_object.close()
except FileNotFoundError:
	print(file_not_found_error_message)
connection = sqlite3.connect(data_base_name_with_table_name[0])
field_names_with_data_type = connection.execute("PRAGMA table_info(" + data_base_name_with_table_name[1] + ")")
field_names = []
for field_name in field_names_with_data_type:
	if field_name[1] != 'Status':
		field_names.append(field_name[1])

def execute_query(query):
	cousor_object = connection.execute(query)
	connection.commit()
	if cousor_object.rowcount:
		return True
	else:
		print(record_not_found_error_message)

def create_record():
	field_values = []
	field_values.append('A')
	for field_name in field_names:
		print(field_name + ": " , end = "")
		field_value = input()
		field_values.append(field_value)
	field_values_tuple = tuple(field_values)
	insert_query = "INSERT INTO " + data_base_name_with_table_name[1] + " VALUES" + str(field_values_tuple)
	execute_query(insert_query)
	print("Details are saved successfully.")

def print_records():
	cousor_object = connection.execute("SELECT * FROM " + data_base_name_with_table_name[1] + " WHERE Status = 'A'")
	records =  cousor_object.fetchall()
	for record in records:
		print_field_values(record)

def print_field_values(record):
	index_number = 1
	for field_name in field_names:
		print(field_name + ": " , end = "")
		print(record[index_number])
		index_number += 1
	print('-' * 25)

def search_record():
	key_value = get_key_value()
	cousor_object = connection.execute("SELECT * FROM " + data_base_name_with_table_name[1] + " WHERE Status = 'A' AND " + str(field_names[0]) + " = " + str(key_value))
	record =  cousor_object.fetchone()
	print_field_values(record)

def get_key_value():
	return input("Enter " + field_names[0] + ": ")

def update_record():
	try:
		updatable_fields_object = open(updatable_fields_cfg_file_name)
		updatable_fields = []
		for update_field in updatable_fields_object.read():
			update_field = int(update_field)
			updatable_fields.append(update_field)
		updatable_fields_object.close()
	except FileNotFoundError:
		print(file_not_found_error_message)
	key_value = get_key_value()
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
	update_query = "UPDATE " + data_base_name_with_table_name[1] + " SET " + str(field_name) + " = " + str(new_field_value) + " WHERE Status = 'A' AND " + str(field_names[0]) + " = " + str(key_value)
	update_status = execute_query(update_query)
	if update_status == True:
		print("Update successful.")

def delete_record():
	key_value = get_key_value()
	delete_query = "UPDATE " + data_base_name_with_table_name[1] + " SET Status = 'D' WHERE " + str(field_names[0]) + " = " + str(key_value)
	delete_status = execute_query(delete_query)
	if delete_status == True:
		print("Delete successful.")

connection.close()
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
				exit()
			else: 
				continue
		elif user_choice > 0 and user_choice < 6:
			functions_list[user_choice - 1]()
	except Exception:
		print("INVALID CHOICE")