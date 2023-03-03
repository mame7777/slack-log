import os

import dotenv
import mysql.connector

def Erase_All_Data(cnx: mysql.connector):
    print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        CAUTION !!!!!!!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This command erase ALL data in DB.

If you want to do, input 'Yes'.

""")
    if input(">>") == "Yes":
        cursor = cnx.cursor()
        cursor.execute("SHOW TABLES")
        try:
            for table in cursor.fetchall()[0]:
                cursor.execute("drop table IF EXISTS"+table)
            cursor.execute("SHOW TABLES")
            print(cursor.fetchall())
        except IndexError:
            print("No Data")
        print("ALL data is erased.")
    else:
        print("No data was erased.")

def CreateTableTest(cnx: mysql.connector):
    cursor = cnx.cursor()
    try:
        # cursor.execute("DROP TABLE IF EXISTS channel")
        sql = '''
            CREATE TABLE channel (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                channel_id VARCHAR(50) NOT NULL,
                name VARCHAR(50) NOT NULL,
                topic VARCHAR(500) NOT NULL,
                purpose VARCHAR(500) NOT NULL
            );
            '''
        cursor.execute(sql)
    except Exception as e:
        print(f"Error Occurred: {e}")
        
    cursor.execute("SHOW TABLES")
    print((cursor.fetchall())[0][0])


def ConnectTest():
    cnx = None
    try:
        cnx = mysql.connector.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME")
        )
        if cnx.is_connected:
            print('Connected!')
        
    except Exception as e:
        print(f"Error Occurred: {e}")

    CreateTableTest(cnx=cnx)
    
    if cnx is not None and cnx.is_connected():
        cnx.close()


def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    ConnectTest()
    return 0


if __name__ == '__main__':
    main()
