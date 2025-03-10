import sqlite3
import re

def read_data(full_name, aadhaar_number, identifier_type=None, identifier_value=None):
    conn = sqlite3.connect('surveys.db')
    cursor = conn.cursor()
    
    try:
        table_name = create_safe_table_name(full_name, aadhaar_number)
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"Error: Table {table_name} does not exist.")
            return None
        
        if identifier_type is None:
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            return records
        elif identifier_type == 'id':
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (identifier_value,))
            record = cursor.fetchone()
            return record
        elif identifier_type == 'survey_no':
            cursor.execute(f"SELECT * FROM {table_name} WHERE survey_no = ?", (identifier_value,))
            record = cursor.fetchone()
            return record
        else:
            print("Error: Invalid identifier_type. Use 'id' or 'survey_no'.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def create_safe_table_name(full_name, aadhaar_number):
    
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', full_name).lower()
    # unique_id = aadhaar_number.replace('-', '')[:4]
    unique_id = "1234"
    
    return f"user_{safe_name}_{unique_id}"

# Function to create a new user table (no record insertion)
def create_user(full_name, aadhaar_number):
    conn = sqlite3.connect('surveys.db')
    cursor = conn.cursor()
    
    try:
        table_name = create_safe_table_name(full_name, aadhaar_number)
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_no INTEGER UNIQUE,
                full_name TEXT NOT NULL,
                aadhaar_number TEXT,
                email TEXT,
                phone_number TEXT,
                date_of_birth TEXT,
                owner_name TEXT NOT NULL,
                area_sqft REAL,
                city_district TEXT,
                pin_code TEXT,
                state TEXT,
                registration_date TEXT,
                status TEXT,
                address TEXT,
                last_updated TEXT
            )
        ''')
        conn.commit()
        print(f"User table {table_name} created successfully.")
    except Exception as e:
        print(f"An error occurred while creating table {table_name}: {e}")
    finally:
        conn.close()

# Function to add a new record to an existing user's table
def add_record(user_data):
    conn = sqlite3.connect('surveys.db')
    cursor = conn.cursor()
    
    try:
        table_name = create_safe_table_name(user_data['full_name'], user_data['aadhaar_number'])
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"Error: Table {table_name} does not exist. Create user first.")
            return
        
        cursor.execute(f'''
            INSERT INTO {table_name} (
                survey_no, full_name, aadhaar_number, email, phone_number, date_of_birth,
                owner_name, area_sqft, city_district, pin_code, state, registration_date,
                status, address, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['survey_no'], user_data['full_name'], user_data['aadhaar_number'],
            user_data['email'], user_data['phone_number'], user_data['date_of_birth'],
            user_data['owner_name'], user_data['area_sqft'], user_data['city_district'],
            user_data['pin_code'], user_data['state'], user_data['registration_date'],
            user_data['status'], user_data['address'], user_data['last_updated']
        ))
        conn.commit()
        print(f"Record added to {table_name} successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error adding record: {e} (Possible duplicate survey_no)")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        conn.close()

# Function to delete a record from a user's table
def delete_record(full_name, aadhaar_number, identifier_type='id', identifier_value=None):
    conn = sqlite3.connect('surveys.db')
    cursor = conn.cursor()
    
    try:
        table_name = create_safe_table_name(full_name, aadhaar_number)
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"Error: Table {table_name} does not exist.")
            return
        
        if identifier_type == 'id':
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (identifier_value,))
        elif identifier_type == 'survey_no':
            cursor.execute(f"DELETE FROM {table_name} WHERE survey_no = ?", (identifier_value,))
        else:
            print("Error: Invalid identifier_type. Use 'id' or 'survey_no'.")
            return
        
        if cursor.rowcount == 0:
            print(f"No record found with {identifier_type} = {identifier_value} in {table_name}.")
        else:
            conn.commit()
            print(f"Record deleted from {table_name} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Function to update a record in a user's table
def update_record(user_data, identifier_type='id', identifier_value=None):
    conn = sqlite3.connect('surveys.db')
    cursor = conn.cursor()
    
    try:
        table_name = create_safe_table_name(user_data['full_name'], user_data['aadhaar_number'])
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            print(f"Error: Table {table_name} does not exist.")
            return
        
        if identifier_type == 'id':
            cursor.execute(f'''
                UPDATE {table_name} SET 
                    survey_no = ?, full_name = ?, aadhaar_number = ?, email = ?, phone_number = ?, 
                    date_of_birth = ?, owner_name = ?, area_sqft = ?, city_district = ?, pin_code = ?, 
                    state = ?, registration_date = ?, status = ?, address = ?, last_updated = ?
                WHERE id = ?
            ''', (
                user_data['survey_no'], user_data['full_name'], user_data['aadhaar_number'],
                user_data['email'], user_data['phone_number'], user_data['date_of_birth'],
                user_data['owner_name'], user_data['area_sqft'], user_data['city_district'],
                user_data['pin_code'], user_data['state'], user_data['registration_date'],
                user_data['status'], user_data['address'], user_data['last_updated'],
                identifier_value
            ))
        elif identifier_type == 'survey_no':
            cursor.execute(f'''
                UPDATE {table_name} SET 
                    full_name = ?, aadhaar_number = ?, email = ?, phone_number = ?, 
                    date_of_birth = ?, owner_name = ?, area_sqft = ?, city_district = ?, pin_code = ?, 
                    state = ?, registration_date = ?, status = ?, address = ?, last_updated = ?
                WHERE survey_no = ?
            ''', (
                user_data['full_name'], user_data['aadhaar_number'],
                user_data['email'], user_data['phone_number'], user_data['date_of_birth'],
                user_data['owner_name'], user_data['area_sqft'], user_data['city_district'],
                user_data['pin_code'], user_data['state'], user_data['registration_date'],
                user_data['status'], user_data['address'], user_data['last_updated'],
                identifier_value
            ))
        else:
            print("Error: Invalid identifier_type. Use 'id' or 'survey_no'.")
            return
        
        if cursor.rowcount == 0:
            print(f"No record found with {identifier_type} = {identifier_value} in {table_name}.")
        else:
            conn.commit()
            print(f"Record updated in {table_name} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Example usage
# if __name__ == "__main__":
    # Create users (only tables, no records)
    # create_user('Adarsh', '1234')
    # create_user('Bob Johnson', '5678-1234-9012')

    # # Add records
    # user1_data = {
    #     'full_name': 'Adarsh',
    #     'aadhaar_number': '1234',
    #     'email': 'adarsh@email.com',
    #     'phone_number': '123-456-7890',
    #     'date_of_birth': '1990-01-01',
    #     'owner_name': 'Adarsh',
    #     'survey_no': 1,
    #     'area_sqft': 1000.0,
    #     'city_district': 'Delhi',
    #     'pin_code': '110001',
    #     'state': 'Delhi',
    #     'registration_date': '2025-03-01',
    #     'status': 'In Progress',
    #     'address': '123 Main St',
    #     'last_updated': '2025-03-01'
    # }
    # add_record(user1_data)

    # user2_data = {
    #     'full_name': 'Bob Johnson',
    #     'aadhaar_number': '5678-1234-9012',
    #     'email': 'bob.johnson@email.com',
    #     'phone_number': '111-222-3333',
    #     'date_of_birth': '1988-11-10',
    #     'owner_name': 'Bob Johnson',
    #     'survey_no': 3,
    #     'area_sqft': 1500.75,
    #     'city_district': 'Chicago',
    #     'pin_code': '60601',
    #     'state': 'Illinois',
    #     'registration_date': '2025-03-01',
    #     'status': 'Pending',
    #     'address': '789 Pine Rd',
    #     'last_updated': '2025-03-01'
    # }
    # add_record(user2_data)

    # # Update a record (e.g., update Adarsh's record with id=1)
    # updated_record = {
    #     'full_name': 'Adarsh',
    #     'aadhaar_number': '1234',
    #     'email': 'adarsh.updated@email.com',
    #     'phone_number': '123-456-7890',
    #     'date_of_birth': '1990-01-01',
    #     'owner_name': 'Adarsh',
    #     'survey_no': 1,
    #     'area_sqft': 1000.0,
    #     'city_district': 'Delhi',
    #     'pin_code': '110001',
    #     'state': 'Delhi',
    #     'registration_date': '2025-03-01',
    #     'status': 'Completed',
    #     'address': '123 Main St',
    #     'last_updated': '2025-03-10'
    # }
    # update_record(updated_record, 'id', 1)

    # # Delete a record (e.g., delete Bob Johnson's record with survey_no=3)
    # delete_record('Bob Johnson', '5678-1234-9012', 'survey_no', 3)

    # # Display all records
    # print("\nFinal User Tables Data:")
    # for full_name, aadhaar_number in [('Adarsh', '1234'), ('Bob Johnson', '5678-1234-9012')]:
    #     table_name = create_safe_table_name(full_name, aadhaar_number)
    #     cursor = sqlite3.connect('surveys.db').cursor()
    #     cursor.execute(f'SELECT * FROM {table_name}')
    #     print(f"\nTable: {table_name}")
    #     for row in cursor.fetchall():
    #         print(row)
    #     cursor.close()

    # Close the connection (if you want to close a global connection, but here it's per-function)
    # conn.close() # Uncomment if using a global connection, but not needed with per-function connections