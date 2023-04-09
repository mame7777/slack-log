print('Hello world!')

# import os

# import dotenv
# import mysql.connector

# def Erase_All_Data(cnx: mysql.connector) -> None:
#     print("""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#         CAUTION !!!!!!!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This command erase ALL data in DB.

# If you want to do, input 'Yes'.

# """)
#     if input(">> ") == "Yes":
#         cursor = cnx.cursor()
#         cursor.execute("SHOW TABLES")
#         try:
#             for table in cursor.fetchall():
#                 if str(table[0]).endswith('_reply'):
#                     cursor.execute("drop table IF EXISTS "+table[0])
#                     print("Erase table of "+table[0])
#             cursor.execute("SHOW TABLES")
#             print(cursor.fetchall())
#         except IndexError:
#             print("No Data")
#         print("ALL data is erased.")
#     else:
#         print("No data was erased.")
        
# def Connect() -> mysql.connector:
#     cnx = None
#     try:
#         cnx = mysql.connector.connect(
#             user=os.environ.get("DB_USER"),
#             password=os.environ.get("DB_PASSWORD"),
#             host=os.environ.get("DB_HOST"),
#             database=os.environ.get("DB_NAME")
#         )
#         if cnx.is_connected:
#             print('Connected!')

#     except Exception as e:
#         print(f"DB Connection Error Occurred: {e}")

#     return cnx


# def EndConnect(cnx: mysql.connector) -> None:
#     if cnx is not None and cnx.is_connected():
#         cnx.close()


# def main() -> int:
#     # 環境変数の読み取り
#     dotenv.load_dotenv()
#     cnx=Connect()
#     Erase_All_Data(cnx=cnx)
#     EndConnect(cnx=cnx)
#     return 0


# if __name__ == '__main__':
#     main()