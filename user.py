import sqlite3
import csv

# download and install git
# create account in github
# git config --global user.name "Ramesh Pradhan"
# git config --global user.email "MY_NAME@example.com"
# go to project folder
# git init
# git add .
# git commit -m "Your commit message"
# git push origin

"""Simple CLI project."""
def create_connection():
    try:
        con = sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print(e)


def create_table(conn):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255),
            email CHAR(255) NOT NULL,
            web text
        );
    """
    cur = conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User table was created successfully.")


def read_csv():
    users = []
    with open("sample_users.csv", "r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))

    return users[1:]


def insert_users(con, users):
    user_add_query = """
        INSERT INTO users
        (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cur = con.cursor()
    cur.executemany(user_add_query, users)
    con.commit()
    print(f"{len(users)} users were imported successfully.")


def select_users(con, no_of_records=0):
    cur = con.cursor()
    if no_of_records:
        users = cur.execute("SELECT * FROM users LIMIT ?;", (no_of_records,))
    else:
        users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)


def select_user_by_id(con, user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users where id = ?;", (user_id,))
    for user in users:
        print(user)


def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("All users were deleted successfully")


INPUT_STRING = """
Enter the option: 
    1. CREATE TABLE
    2. DUMP users from csv INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users from TABLE
    5. QUERY user by id from TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE user by id
    9. UPDATE user
    10. Press any key to EXIT
"""


def delete_user_by_id(con, user_id):
    cur = con.cursor()
    cur.execute("DELETE FROM users where id = ?", (user_id,))
    con.commit()
    print(f"User with id [{user_id}] was successfully deleted.")


COLUMNS = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web",
)


def update_user_by_id(con, user_id, column_name, column_value):
    update_query = f"UPDATE users set {column_name}=? where id = ?;"
    cur = con.cursor()
    cur.execute(update_query, (column_value, user_id))
    con.commit()
    print(
        f"[{column_name}] was updated with value [{column_value}] of user with id [{user_id}]"
    )


def main():
    con = create_connection()
    user_input = input(INPUT_STRING)
    if user_input == "1":
        create_table(con)

    elif user_input == "2":
        users = read_csv()
        insert_users(con, users)

    elif user_input == "3":
        user_data = []
        for column in COLUMNS:
            column_value = input(f"Enter {column}: ")
            user_data.append(column_value)
        insert_users(con, [tuple(user_data)])

    elif user_input == "4":
        select_users(con)

    elif user_input == "5":
        user_id = input("Enter the id of user: ")
        select_user_by_id(con, user_id)

    elif user_input == "6":
        no_of_records = input("How many users you want to fetch? ")
        if no_of_records.isnumeric():
            select_users(con, int(no_of_records))

    elif user_input == "7":
        delete_users(con)

    elif user_input == "8":
        user_id = input("Enter the id of user: ")
        delete_user_by_id(con, user_id)

    elif user_input == "9":
        user_id = input("Enter id of user: ")
        if user_id.isnumeric():
            column_name = input(
                f"Enter the column you want to edit. Please make sure column is with in {COLUMNS}: "
            )
            if column_name in COLUMNS:
                column_value = input(f"Enter the value of {column_name}: ")
                update_user_by_id(con, user_id, column_name, column_value)

    else:
        exit()


main()
