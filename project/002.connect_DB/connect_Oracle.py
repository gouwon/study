#-*- coding: utf-8 -*-

## python -m venv ./venv
## source ./venv/Scripts/activate
## pip install cx_Oracle==8.3.0
## pip install pandas==2.2.2

import cx_Oracle as orcl
import pandas as pd

def dbConnection(username, password, host, port, service_name):
    """
    Oracle DB에 연결하는 함수
    """
    try:
        # dsn = orcl.makedsn(host, port, service_name)
        # conn = orcl.connect(username, password, dsn)
        conn = orcl.connect(username, password, service_name)
        return conn
    except orcl.DatabaseError as e:
        print(f"Error connecting to Oracle: {e}")
        return None

def execute_query(conn, query):
    """
    입력받은 쿼리를 실행하고 결과를 pandas DataFrame으로 반환하는 함수
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        cursor.close()
        return df
    except orcl.DatabaseError as e:
        print(f"Error executing query: {e}")
        return None

# 사용자 정보 입력
username = "test"
password = "test"
host = "localhost"
port = 1521
service_name = "ORCLCDB"

# DB 연결
conn = dbConnection(username, password, host, port, service_name)
if conn:
    while True:
        user_query = input("쿼리를 입력하세요 (종료하려면 'exit' 입력): ")
        if user_query.lower() == "exit":
            break
        df_result = execute_query(conn, user_query)
        if df_result is not None:
            print(df_result)
        else:
            print("쿼리 실행 중 오류가 발생했습니다.")
    conn.close()
else:
    print("DB 연결에 실패했습니다.")
