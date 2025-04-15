import psycopg2
import csv


conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "12345678",
                        port = 5432)


cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telephone VARCHAR(20) NOT NULL)
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
    id = int(input("Enter id of a contact you want to change: "))
    print("What do you want to change? ")
    print("1. Contact's name")
    print("2. Contact's phone number")
    choice = int(input("Your choice: "))
    
    if choice == 1:
        new_name = input("Enter new name: ")
        cur.execute("""UPDATE phonebook
                    SET name = %s
                    WHERE id = %s""", (new_name, id))
        conn.commit()
    elif choice == 2:
        new_num = input("Enter new phone number: ")
        cur.execute("""UPDATE phonebook
                    SET telephone = %s
                    WHERE id = %s""", (new_num, id))
        
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
        cur.execute("""SELECT * FROM phonebook WHERE name = %s ;""", (num, ))

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


print("Choose what do you want to do with the table:")
print("1. Insert some data")
print("2. Change contact")
print("3. Filter data by name or phone number")
print("4. Delete contact")
command = int(input("Your choice: "))

if command == 1:
    print("Choose the method you want to insert data with:")
    print("1. By the CSV-file")
    print("2. By the console")
    choice = int(input("Your choice: "))

    if choice == 1:
        filename = input("Enter CSV-file name: ")
        upload_csv(filename)
        
    elif choice == 2:
        enter_manually()

elif command == 2:
    update_table()

elif command == 3:
    query_data()

elif command == 4:
    delete_data()


print_rows()
