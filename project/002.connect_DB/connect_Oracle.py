# -*- coding: utf-8 -*-

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

def save_to_file(df, file_name):
    """
    DataFrame의 데이터를 텍스트 파일로 저장하는 함수
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for index, row in df.iterrows():
            file.write(row[0] + '\n')  # 각 행을 파일에 기록

def print_or_save(df, file_name=None):
    """
    DataFrame을 출력하거나, 파일로 저장할 수 있도록 선택하는 함수
    """
    if file_name:
        # 파일로 저장
        save_to_file(df, file_name)
        print(f"결과가 '{file_name}' 파일로 저장되었습니다.")
    else:
        # 표준 출력 (모든 컬럼과 모든 행 출력)
        print(df.to_string(index=False))  # 인덱스 없이 전체 DataFrame 출력

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
            # 파일 저장 여부 확인
            save_option = input("결과를 파일로 저장하시겠습니까? (y/n): ").strip().lower()
            if save_option == 'y':
                file_name = input("파일 이름을 입력하세요 (예: result.txt): ")
                print_or_save(df_result, file_name)
            else:
                print_or_save(df_result)  # 파일 저장 안 함, 표준 출력
        else:
            print("쿼리 실행 중 오류가 발생했습니다.")
    conn.close()
else:
    print("DB 연결에 실패했습니다.")
