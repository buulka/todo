import sqlite3
from _sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to sqlite successful")
    except Error as e:
        print(f"1The error  '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"2The error '{e}' occurred")


def add_user(connection, user_name):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (name) VALUES(?)", user_name)
        connection.commit()

    except Error as e:
        print(f"4The error '{e}' occurred")
    cursor.execute("SELECT id FROM users;")
    id_result = cursor.fetchone()
    print(id_result)


def add_task(connection, task_name, task):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO tasks (name, task) VALUES(?, ?)", (task_name, task))
        connection.commit()
    except Error as e:
        print(f"5The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"3The error '{e}' occurred")


def select_users_tasks(connection):
    select_posts = '''
    SELECT
        users.id,
        users.name,
        tasks.name,
        tasks.task
    FROM
        tasks
        INNER JOIN users ON users.id = tasks.user_id
    '''

    user_tasks = execute_read_query(connection, select_posts)
    return user_tasks


def main():
    connection = create_connection("C:\\todo\\main")
    cursor = connection.cursor()

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """
    execute_query(connection, create_users_table)

    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        task TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """
    execute_query(connection, create_tasks_table)

    print("0 - end session \n1 - add a user and a task \n2 - select all users")
    select = 1

    while select != 0:
        # try:
        select = int(input("Your choice: "))

        if select == 1:
            name = input("Insert username: ")
            add_user(connection, name)
            task_name = input("task name: ")
            task = input("task: ")
            add_task(connection, task_name, task)

        elif select == 2:
            for users in select_users_tasks(connection):
                print(users)
        elif select == 0:
            print("Your session ended")
            break
        else:
            print("There is no such command")
        #
        # except:
        #     print("There is no such command")
    else:
        print("Your session ended")

    cursor.close()
    connection.close()


main()
