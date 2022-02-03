from mysql.connector import connect, Error

from db_config import DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME

try:
    connection = connect(host=DB_HOSTNAME, user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    sql = open('db/create_tables.sql', 'r')
    cursor.execute(sql.read(), multi=True)
except Error as e:
    print(e)
