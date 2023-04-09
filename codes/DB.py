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
                channel_id VARCHAR(50) NOT NULL UNIQUE,
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
                user_id VARCHAR(30) NOT NULL UNIQUE,
                user_name VARCHAR(50) NOT NULL,
                user_real_name VARCHAR(60) NOT NULL,
                user_profile_img VARCHAR(300) NOT NULL
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
                conversation_query = '''CREATE TABLE IF NOT EXISTS '''+channel_id+'''_conversation (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    ts DOUBLE NOT NULL UNIQUE,
                    user_id VARCHAR(50) NOT NULL,
                    text TEXT(2000) NOT NULL,
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
                reply_query = '''CREATE TABLE IF NOT EXISTS '''+channel_id+'''_reply (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    conversation_ts DOUBLE NOT NULL,
                    reply_ts DOUBLE NOT NULL UNIQUE,
                    user_id VARCHAR(50) NOT NULL,
                    text TEXT(2000) NOT NULL
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

    def channel(self, channel_dict: dict) -> None:
        cursor = self.cnx.cursor()
        insert_channel = ("INSERT IGNORE INTO channel "
                          "(channel_id, channel_name, topic, purpose) "
                          "VALUES (%s, %s, %s, %s)")
        for channel_id in channel_dict.keys():
            channel_name = channel_dict[channel_id]["name"]
            channel_topic = channel_dict[channel_id]["topic"]
            channel_purpose = channel_dict[channel_id]["purpose"]
            data_channel = (channel_id, channel_name,
                            channel_topic, channel_purpose)
            cursor.execute(insert_channel, data_channel)
        self.cnx.commit()

    def user(self, user_dict: dict) -> None:
        cursor = self.cnx.cursor()
        insert_user = ("INSERT IGNORE INTO user "
                       "(user_id, user_name, user_real_name, user_profile_img) "
                       "VALUES (%s, %s, %s, %s)")
        for user_id in user_dict.keys():
            user_name = user_dict[user_id]["name"]
            user_real_name = user_dict[user_id]["real_name"]
            user_profile_img = user_dict[user_id]["profile_img"]
            data_user = (user_id, user_name, user_real_name, user_profile_img)
            cursor.execute(insert_user, data_user)
        self.cnx.commit()

    def conversation(self, conversation_dict: dict) -> None:
        cursor = self.cnx.cursor()
        for channel_conversation in conversation_dict.keys():
            table_conversation = channel_conversation+"_conversation"
            # insert_conversation =(table_conversation+
            #                     " (ts, user_id, text, reply_count)"
            #                     " VALUES (%f, %s, %s, %d)")
            for ts in conversation_dict[channel_conversation].keys():
                user_id = conversation_dict[channel_conversation][ts]["user"]
                # text = conversation_dict[channel_conversation][ts]["text"]
                # text_list = conversation_dict[channel_conversation][ts]["text"].splitlines()
                # text = ("\n".join(text_list)).replace("", "")
                text = (conversation_dict[channel_conversation][ts]["text"]).replace(
                    "'", '"')
                reply_count = int(
                    conversation_dict[channel_conversation][ts]["reply_count"])
                query_conversation = """INSERT IGNORE INTO %s\
 (ts, user_id, text, reply_count)\
 VALUES (%f, '%s', '%s', %d)""" % (table_conversation, float(ts), user_id, text, reply_count)
                print(query_conversation)
                # data_conversation = (table_conversation, ts_float, user_id, text, reply_count)
                cursor.execute(query_conversation)
                # cursor.execute(insert_conversation,data_conversation)
        self.cnx.commit()
    
    def reply(self, reply_dict: dict) -> None:
        cursor = self.cnx.cursor()
        for channel_reply in reply_dict.keys():
            table_reply = channel_reply+"_reply"
            for ts_ToConversation in reply_dict[channel_reply].keys():
                for ts in reply_dict[channel_reply][ts_ToConversation].keys():
                    user_id = reply_dict[channel_reply][ts_ToConversation][ts]["user"]
                    # text = conversation_dict[channel_conversation][ts]["text"]
                    # text_list = conversation_dict[channel_conversation][ts]["text"].splitlines()
                    # text = ("\n".join(text_list)).replace("", "")
                    text = (reply_dict[channel_reply][ts_ToConversation][ts]["text"]).replace(
                        "'", '"')
                    query_reply = """INSERT IGNORE INTO %s\
 (conversation_ts, reply_ts, user_id, text)\
 VALUES (%f, %f, '%s', '%s')""" % (table_reply, float(ts_ToConversation), float(ts), user_id, text)
                    print(query_reply)
                    # data_conversation = (table_conversation, ts_float, user_id, text, reply_count)
                    cursor.execute(query_reply)
                    # cursor.execute(insert_conversation,data_conversation)
        self.cnx.commit()


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
