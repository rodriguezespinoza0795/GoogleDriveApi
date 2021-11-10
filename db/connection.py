import sqlalchemy as sql

def get_connection():
    user = 'root'
    password = ''
    host = '127.0.0.1:3306'
    database = 'test'
    conn_string = 'mysql+pymysql://{}:{}@{}/{}'.format(user, password, host, database)
    sql_conn = sql.create_engine(conn_string)
    return sql_conn

def conn_close(sql_conn):
    connection = sql_conn.raw_connection()
    connection.close()