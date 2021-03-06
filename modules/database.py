import sqlite3
from time import time_ns

from orjson import dumps, loads

from modules import environment
from modules.classes import (LogInfo, LogList, SchedulerInfo, TaskList,
                             TaskOutput)


def udumps(data):
    return dumps(data).decode("utf-8")

def connect_to_db(file = environment.DB_FILE):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

def select_all_column(column, table):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT {column} FROM {table};")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [x for i in results for x in i]

def update_row(table, column, new_value, s_column, s_value):
    connection, cursor = connect_to_db()
    cursor.execute(f"""UPDATE {table} SET {column} = ? WHERE {s_column} = "{s_value}";""", (new_value, ))
    connection.commit()
    close_connection(connection, cursor)

def get_table(table):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {table};")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return results

def get_row(table, s_column, s_value):
    connection, cursor = connect_to_db()
    cursor.execute(f"""SELECT * FROM {table} WHERE {s_column} = "{s_value}";""")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return results[0] if results else []

# UPDATE ROWS
def complete_task(task_id, res):
    try:
        update_row(environment.DB_TABLE_TASKS, "status", 1, "task_id", task_id)
        update_row(environment.DB_TABLE_TASKS, "result", udumps(res), "task_id", task_id)
        add_log(time_ns(), f"Updated task {task_id} status to 1")
    except:
        add_log(time_ns(), f"Failed to update task {task_id} status to 1")

def pending_task(task_id, pc):
    try:
        update_row(environment.DB_TABLE_TASKS, "status", 2, "task_id", task_id)
        update_row(environment.DB_TABLE_TASKS, "pc", pc, "task_id", task_id)
        add_log(time_ns(), f"Updated task {task_id} status to 2")
    except:
        add_log(time_ns(), f"Failed to update task {task_id} status to 1")

def free_task(task_id):
    try:
        update_row(environment.DB_TABLE_TASKS, "status", 0, "task_id", task_id)
        update_row(environment.DB_TABLE_TASKS, "pc", "", "task_id", task_id)
        add_log(time_ns(), f"Updated task {task_id} status to 0")
    except:
        add_log(time_ns(), f"Failed to update task {task_id} status to 1")

def change_scheduler_status(pc: str, status: int):
    try:
        update_row(environment.DB_TABLE_SCHEDULER, "status", status, "pc", pc)
        add_log(time_ns(), f"Updated {pc} status to {status}")
    except:
        add_log(time_ns(), f"Failed to update {pc} status to {status}")

# STATUS/INFO
def list_task(identifier = ""):
    connection, cursor = connect_to_db()
    cursor.execute(f"""SELECT * FROM {environment.DB_TABLE_TASKS} WHERE uuid = "{identifier}";""")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return TaskList(tasks=[TaskOutput(task_id=result[0],
                                        status=result[1],
                                        unix_time= result[2],
                                        pc=result[3],
                                        input_values=loads(result[4]),
                                        result=loads(result[5]) if result[5] else [],
                                        uuid=result[6]).dict() for result in results],
                                uuid=identifier)

def status_task(task_id):
    result = get_row(environment.DB_TABLE_TASKS, "task_id", task_id)
    return TaskOutput(task_id=result[0],
                            status=result[1],
                            unix_time= result[2],
                            pc=result[3],
                            input_values=loads(result[4]),
                            result=loads(result[5]) if result[5] else [],
                            uuid=result[6]).dict()

def task_exists(task_id):
    result = get_row(environment.DB_TABLE_TASKS, "task_id", task_id)
    return True if result else False

def status_scheduler(pc):
    result = get_row(environment.DB_TABLE_SCHEDULER, "pc", pc)
    return SchedulerInfo(pc=result[0],
                                    status=result[1],
                                    pc_domain=result[2]).dict()

def scheduler_exists(pc):
    result = get_row(environment.DB_TABLE_SCHEDULER, "pc", pc)
    return True if result else False

def user_info(s_column, s_value):
    result = get_row(environment.DB_TABLE_USERS, s_column, s_value)
    return {"uuid": result[0]}

def user_hash(identifier):
    result = get_row(environment.DB_TABLE_USERS, "uuid", identifier)
    return result[1]

def user_exists(identifier):
    result = get_row(environment.DB_TABLE_USERS, "uuid", identifier)
    return True if result else False

def list_logs(max_logs):
    connection, cursor = connect_to_db()
    cursor.execute(f"""SELECT * FROM {environment.DB_TABLE_LOGS} ORDER BY logid DESC LIMIT {max_logs};""")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return LogList(logs=[LogInfo(unix_time=result[0], text=result[1]) for result in results])

# ADD ROWS
def add_task(task_id, input_values, identifier = ""):
    try:
        connection, cursor = connect_to_db()
        cursor.execute(f"INSERT INTO {environment.DB_TABLE_TASKS} (task_id, unix_time, input_values, uuid) VALUES (?, ?, ?, ?);", (task_id, time_ns(), udumps(input_values), identifier))
        connection.commit()
        close_connection(connection, cursor)
        add_log(time_ns(), f"Added new task {task_id} to the database")
    except:
        add_log(time_ns(), f"Failed to add new task {task_id} to the database")

def add_user(identifier, hashed_password):
    try:
        connection, cursor = connect_to_db()
        cursor.execute(f"INSERT INTO {environment.DB_TABLE_USERS} VALUES (?, ?);", (identifier, hashed_password, ))
        connection.commit()
        close_connection(connection, cursor)
        add_log(time_ns(), f"Added new user {identifier} to the database")
    except:
        add_log(time_ns(), f"Failed to add new user {identifier} to the database")

def add_log(unix_time, text):
    connection, cursor = connect_to_db()
    cursor.execute(f"INSERT INTO {environment.DB_TABLE_LOGS} VALUES (?, ?);", (unix_time, text, ))
    connection.commit()
    close_connection(connection, cursor)

# RANDOMIZERS
def oldest_pending_task():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.DB_TABLE_TASKS} WHERE status = 0 ORDER BY unix_time ASC LIMIT 1;")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None

def random_free_scheduler():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.DB_TABLE_SCHEDULER} WHERE status = 0 ORDER BY RANDOM() LIMIT 1;")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None
