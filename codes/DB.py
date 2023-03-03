import os

import dotenv
import mysql.connector


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
            print('ok!')

    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()


def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    ConnectTest()
    return 0


if __name__ == '__main__':
    main()
