import sqlite3
import sys

connection = sqlite3.connect('tracker.db')
cursor = connection.cursor()


# creates table unless one exists
try:
    cursor.execute("CREATE TABLE tracker (name TEXT, sub STRING, number INTEGER)")
except Exception as e:
    pass


# Makes sure name id is unique when created
def user_is_unique(name):
    rows = cursor.execute("SELECT name, sub, number FROM tracker").fetchall()

    for user in rows:
        if user[0] == name:
            return False
    return True


# create new data record to table
def insert_db():
    name = input("Name >>")

    if user_is_unique(str(name)):
        sub = input("Sub >>")
        number = input("Number >>")

        if name != "" and sub != "" and number != "":
            cursor.execute(f"INSERT INTO tracker VALUES ('{name}', '{sub}', '{number}')")
            connection.commit()
            print(name + " has been added to the database!")

        else:
            print("One of the fields are empty! Please try again")
            insert_db()
    else:
        print("Name is already in the database!")


def edit_db():
    name = input("Type the name of the text you would like to edit >>")
    field = input("Which field would you like to edit: Name, Sub, Number? >>")
    updated_field = input("What would you like to update it to? >>")

    try:
        cursor.execute(f"UPDATE tracker SET {field} = ? WHERE name = ?", (updated_field, name))
        connection.commit()
        print(f"Successfully updated {updated_field}!")
    except Exception as e:
        print(e)


def number_db():
    name = input("Type the name of the text you would like to edit >>")
    value = 0
    options = input("""
        ----------------------
        Type '0' to exit
        Type '1' to + 1
        Type '2' to - 1
        Type '3' to + 5
        Type '4' to - 5
        ----------------------
        >>""")

    if options == "1":
        value += 1
    if options == "2":
        value -= -1
    if options == "3":
        value += 5
    if options == "4":
        value -= 5
    try:
        cursor.execute(f"UPDATE tracker SET number = number + ? WHERE name = ?", (value, name))
        connection.commit()
        rows = cursor.execute("SELECT number FROM tracker WHERE name = ?", (name,), ).fetchall()

        num = rows[0][0]

        print(f"Number changed to {num}")
    except Exception as e:
        print(e)


def display_db():
    target_name = input("Type the name of the record you want to view >>")
    rows = cursor.execute("SELECT name, sub, number FROM tracker WHERE name = ?", (target_name,), ).fetchall()

    name = rows[0][0]
    sub = rows[0][1]  # rows [(name, sub, number)]
    number = rows[0][2]

    print(f"{name}, {sub}, {number}")


def delete_db():
    name = input("Type the name of the record you want to delete >>")
    if name != "":
        cursor.execute("DELETE FROM tracker WHERE name = ?", (name,))
        connection.commit()
        print(f"Successfully deleted {name}")


def display_all_db():
    rows = cursor.execute("SELECT name, sub, number FROM tracker ORDER BY name ASC").fetchall()

    print("Data: ")
    for user in rows:
        print(f" {user[0]} - {user[1]} - {user[2]}")


def exit_db():
    cursor.close()
    connection.close()
    sys.exit()


def select_options():
    options = input("""
    ----------------------
    Type '0' to exit
    Type '1' to insert new data
    Type '2' to delete data
    Type '3' to edit data
    Type '4' to display all data
    Type '5' to display data
    Type '6' to change number data
    ----------------------
    >>""")

    if options == "0":
        exit_db()
    if options == "1":
        insert_db()
    if options == "2":
        delete_db()
    if options == "3":
        edit_db()
    if options == "4":
        display_all_db()
    if options == "5":
        display_db()
    if options == "6":
        number_db()


# loop
while True:
    select_options()
