from os import getenv

DB_FILE = getenv("db_file")
DB_TABLE_TASKS = getenv("db_table_tasks")
DB_TABLE_SCHEDULER = getenv("db_table_scheduler")
DB_TABLE_USERS = getenv("db_table_users")
AUTH_SECRET = getenv("auth_secret")
WS_URL = getenv("ws_url")