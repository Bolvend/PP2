import psycopg2
import csv
import re
from typing import List, Tuple

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    host="localhost",
    password="12345678",
    port=5432
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telephone VARCHAR(20) NOT NULL
    )
""")
conn.commit()

cur.execute("""
    CREATE OR REPLACE FUNCTION get_all_phonebook()
    RETURNS TABLE(id INTEGER, name VARCHAR, telephone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT p.id, p.name, p.telephone
        FROM phonebook p;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE PROCEDURE insert_user(
        p_name VARCHAR,
        p_telephone VARCHAR
    ) AS $$
    BEGIN
        INSERT INTO phonebook (name, telephone)
        VALUES (p_name, p_telephone);
        COMMIT;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE PROCEDURE update_user_phone(
        p_name VARCHAR,
        p_telephone VARCHAR
    ) AS $$
    BEGIN
        UPDATE phonebook
        SET telephone = p_telephone
        WHERE name = p_name;
        COMMIT;
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE PROCEDURE delete_user(
        p_search_term VARCHAR
    ) AS $$
    BEGIN
        DELETE FROM phonebook
        WHERE name = p_search_term OR telephone = p_search_term;
        COMMIT;
    END;
    $$ LANGUAGE plpgsql;
""")
conn.commit()

def upload_csv(filename):
    try:
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            _ = next(csvreader)
            for row in csvreader:
                id, name, telephone = row
                if (id, name, telephone) != ("id", "name", "telephone"):
                    cur.execute("""INSERT INTO phonebook(id, name, telephone) VALUES (%s, %s, %s)""", (id, name, telephone))
                    conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def enter_manually():
    id = int(input("New contact's ID: "))
    name = input("New contact's name: ")
    telephone = input("New contact's phone number: ")
    cur.execute("INSERT INTO phonebook (id, name, telephone) VALUES (%s, %s, %s)", (id, name, telephone))
    conn.commit()

def update_table():
    nameofcon = input("Enter name of a contact you want to change: ")
    cur.execute("""SELECT * FROM phonebook WHERE name = %s ;""",(nameofcon, ))
    rows = cur.fetchall()
    
    found = False
    for row in rows:
        if nameofcon == row[1]:  
            found = True
            contact_id = row[0]  
            print("What do you want to change? ")
            print("1. Contact's name")
            print("2. Contact's phone number")
            
            try:
                choice = int(input("Your choice: "))
                if choice not in [1, 2]:
                    print("Invalid choice.")
                    return
                
                if choice == 1:
                    new_name = input("Enter new name: ")
                    cur.execute("""UPDATE phonebook
                                SET name = %s
                                WHERE id = %s""", (new_name, contact_id))
                    conn.commit()
                elif choice == 2:
                    new_num = input("Enter new phone number: ")
                    cur.execute("""UPDATE phonebook
                    SET telephone = %s
                    WHERE id = %s""", (new_num, contact_id))
                    conn.commit()
                    print("Phone number updated successfully.")
                
                break
            except ValueError:
                print("Please enter a valid number.")
                return
            except Exception as e:
                print(f"An error occurred: {e}")
                return
    
    if not found:
        print("Contact not found.")

def query_data():
    print("How do you wanna filter your data?")
    print("1. By contact's name")
    print("2. By contact's phone number")
    choice = int(input("Your choice: "))
    if choice == 1:
        name = input("Enter needed name: ")
        cur.execute("""SELECT * FROM phonebook WHERE name = %s ;""",(name, ))
    elif choice == 2:
        num = input("Enter needed phone number: ")
        cur.execute("""SELECT * FROM phonebook WHERE telephone = %s ;""", (num, ))
    else:
        print("Invalid choice.")
        return

    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_data():
    name = input("Enter name of a contact you want to delete: ")
    cur.execute("""DELETE FROM phonebook WHERE name = %s""", (name, ))
    conn.commit()

def print_rows():
    cur.execute("""SELECT * FROM phonebook;""")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def search_by_pattern(pattern: str) -> List[Tuple]:
    """Search phonebook by pattern in name or telephone using Python filtering"""
    cur.execute("SELECT * FROM get_all_phonebook()")
    rows = cur.fetchall()
    pattern = pattern.lower()
    return [
        row for row in rows
        if pattern in row[1].lower() or pattern in row[2].lower()
    ]

def upsert_user(name: str, telephone: str) -> bool:
    """Insert new user or update existing user's phone"""
    
    
    cur.execute("SELECT 1 FROM phonebook WHERE name = %s", (name,))
    exists = cur.fetchone() is not None
    
    if exists:
        cur.execute("CALL update_user_phone(%s, %s)", (name, telephone))
    else:
        cur.execute("CALL insert_user(%s, %s)", (name, telephone))
    conn.commit()
    return True

def insert_multiple_users(names: List[str], telephones: List[str]) -> List[str]:
    """Insert multiple users and return invalid entries"""
    if len(names) != len(telephones):
        return ["Error: Names and telephones lists must have equal length"]
    
    invalid_entries = []
    for name, phone in zip(names, telephones):
        upsert_user(name, phone)
    
    return invalid_entries

def get_paginated_data(limit: int, offset: int) -> List[Tuple]:
    """Get paginated phonebook data using Python"""
    cur.execute("SELECT * FROM get_all_phonebook() ORDER BY id")
    rows = cur.fetchall()
    start = min(offset, len(rows))
    end = min(offset + limit, len(rows))
    return rows[start:end]

def delete_user(search_term: str) -> None:
    """Delete user by name or telephone"""
    cur.execute("CALL delete_user(%s)", (search_term,))
    conn.commit()

def main():
    while True:
        print("\nPhonebook Menu:")
        print("1. Insert data")
        print("2. Search by pattern")
        print("3. Add/Update single user")
        print("4. Add multiple users")
        print("5. View paginated data")
        print("6. Delete user by name or phone")
        print("7. Print all records")
        print("8. Exit")
        
        try:
            choice = int(input("Enter choice (1-8): "))
            
            if choice == 1:
                print("Choose the method to insert data:")
                print("1. By CSV-file")
                print("2. By console")
                insert_choice = int(input("Your choice: "))
                if insert_choice == 1:
                    filename = input("Enter CSV-file name: ")
                    upload_csv(filename)
                elif insert_choice == 2:
                    enter_manually()
                else:
                    print("Invalid choice.")
                    
            elif choice == 2:
                pattern = input("Enter search pattern: ")
                results = search_by_pattern(pattern)
                for row in results:
                    print(row)
                    
            elif choice == 3:
                name = input("Enter name: ")
                telephone = input("Enter telephone: ")
                if upsert_user(name, telephone):
                    print("User added/updated successfully")
                    
            elif choice == 4:
                names = input("Enter names (comma-separated): ").split(",")
                telephones = input("Enter telephones (comma-separated): ").split(",")
                invalid = insert_multiple_users([n.strip() for n in names], [t.strip() for t in telephones])
                if invalid:
                    print("Invalid entries:", invalid)
                else:
                    print("All users added successfully")
                    
            elif choice == 5:
                limit = int(input("Enter limit: "))
                offset = int(input("Enter offset: "))
                results = get_paginated_data(limit, offset)
                for row in results:
                    print(row)
                    
            elif choice == 6:
                search_term = input("Enter name or telephone to delete: ")
                delete_user(search_term)
                print("User deleted successfully")
                
            elif choice == 7:
                print_rows()
                
            elif choice == 8:
                break
                
            else:
                print("Invalid choice")
                
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    finally:
        cur.close()
        conn.close()