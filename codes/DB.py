import os

import dotenv
import mysql.connector


def Erase_All_Data(cnx: mysql.connector) -> None:
    print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        CAUTION !!!!!!!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This command erase ALL data in DB.

If you want to do, input 'Yes'.

""")
    if input(">> ") == "Yes":
        cursor = cnx.cursor()
        cursor.execute("SHOW TABLES")
        try:
            for table in cursor.fetchall():
                cursor.execute("drop table IF EXISTS "+table[0])
                print("Erase table of "+table[0])
            cursor.execute("SHOW TABLES")
            print(cursor.fetchall())
        except IndexError:
            print("No Data")
        print("ALL data is erased.")
    else:
        print("No data was erased.")


class CreateTable:
    cnx = mysql.connector

    def __init__(self, cnx: mysql.connector):
        self.cnx = cnx

    def channel(self) -> None:
        cursor = self.cnx.cursor()
        try:
            channel_query = '''CREATE TABLE channel (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                channel_id VARCHAR(50) NOT NULL,
                channel_name VARCHAR(50) NOT NULL,
                topic VARCHAR(500) NOT NULL,
                purpose VARCHAR(500) NOT NULL
            );
            '''
            cursor.execute(channel_query)
            print("Create table of channel")
        except Exception as e:
            print(f"CreateTable 'channel' Error Occurred: {e}")

    def user(self):
        cursor = self.cnx.cursor()
        try:
            user_query = '''CREATE TABLE user (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                user_name VARCHAR(50) NOT NULL,
                user_real_name VARCHAR(50) NOT NULL,
                user_profile_img VARCHAR(500) NOT NULL
            );
            '''
            cursor.execute(user_query)
            print("Create table of user")
        except Exception as e:
            print(f"CreateTable 'user' Error Occurred: {e}")

    def Conversation(self, channel_dict: dict) -> None:
        cursor = self.cnx.cursor()
        print("Conversationのテーブル作成開始")
        for channel_id in channel_dict.keys():
            try:
                conversation_query = '''CREATE TABLE '''+channel_id+'''_conversation (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    ts INT NOT NULL,
                    user_id VARCHAR(50) NOT NULL,
                    text VARCHAR(1000) NOT NULL,
                    reply_count INT NOT NULL
                );
                '''
                cursor.execute(conversation_query)
                print("Create 'conversation' table of channel '"+channel_id+"'")
            except Exception as e:
                print(f"CreateTable 'Conversation' Error Occurred: {e}")

    def Reply(self, channel_dict: dict) -> None:
        cursor = self.cnx.cursor()
        print("Replyのテーブル作成開始")
        for channel_id in channel_dict.keys():
            try:
                reply_query = '''CREATE TABLE '''+channel_id+'''_reply (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    conversation_ts INT NOT NULL,
                    reply_ts INT NOT NULL,
                    user_id VARCHAR(50) NOT NULL,
                    text VARCHAR(1000) NOT NULL
                );
                '''
                cursor.execute(reply_query)
                print("Create 'reply' table of channel '"+channel_id+"'")
            except Exception as e:
                print(f"CreateTable 'reply' Error Occurred: {e}")

class Insert:
    cnx = mysql.connector
    
    def __init__(self, cnx: mysql.connector):
        self.cnx = cnx

def CreateTableTest(cnx: mysql.connector) -> None:
    cursor = cnx.cursor()
    # try:
    #     # cursor.execute("DROP TABLE IF EXISTS channel")
    #     sql = '''
    #         CREATE TABLE channel (
    #             id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #             channel_id VARCHAR(50) NOT NULL,
    #             name VARCHAR(50) NOT NULL,
    #             topic VARCHAR(500) NOT NULL,
    #             purpose VARCHAR(500) NOT NULL
    #         );
    #         '''
    #     cursor.execute(sql)
    # except Exception as e:
    #     print(f"Error Occurred: {e}")
    # cursor.execute("SHOW TABLES")
    # print((cursor.fetchall())[0])


def ConnectTest():
    cnx = None
    # try:
    #     cnx = mysql.connector.connect(
    #         user=os.environ.get("DB_USER"),
    #         password=os.environ.get("DB_PASSWORD"),
    #         host=os.environ.get("DB_HOST"),
    #         database=os.environ.get("DB_NAME")
    #     )
    #     if cnx.is_connected:
    #         print('Connected!')

    # except Exception as e:
    #     print(f"Error Occurred: {e}")

    # Erase_All_Data(cnx=cnx)

    # if cnx is not None and cnx.is_connected():
    #     cnx.close()


def Connect() -> mysql.connector:
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
        print(f"DB Connection Error Occurred: {e}")

    return cnx


def EndConnect(cnx: mysql.connector) -> None:
    if cnx is not None and cnx.is_connected():
        cnx.close()


def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    ConnectTest()
    return 0


if __name__ == '__main__':
    main()
