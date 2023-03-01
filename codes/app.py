import requests
import json
import dotenv
import os

# 辞書型のチャンネルデータを取得


def GetChannelInfo() -> dict:
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": "Bearer " +
               str(os.environ.get("SLACK_BOT_TOKEN"))}
    # チャンネル一覧の取得
    response = requests.get(url, headers=headers)
    channel_data = response.json()

    # #インデントをつけてさらに見やすい形式に変換
    # channel_json = json.dumps(channel_data, indent=2, ensure_ascii=False)

    # 辞書型のチャンネルデータを生成
    channel_dict = dict()
    for i in channel_data["channels"]:
        channel_dict[i["id"]] = {"name": i["name"],
                                 "topic": i["topic"]["value"],
                                 "purpose": i["purpose"]["value"]}

    return channel_dict


def GetUserInfo() -> dict:
    url = "https://slack.com/api/users.list"
    headers = {"Authorization": "Bearer " +
               str(os.environ.get("SLACK_BOT_TOKEN"))}
    # チャンネル一覧の取得
    response = requests.get(url, headers=headers)
    user_data = response.json()

    # print(json.dumps(user_data, indent=2, ensure_ascii=False))

    # 辞書型のユーザーデータを生成
    user_dict = dict()
    for i in user_data["members"]:
        # 名称未設定の人の分をスキップ
        try:
            real_name = i["real_name"]
        except KeyError:
            real_name = ""

        # 画像を取得できない人の分をスキップ
        # 他の画像を探すようにしたいね
        try:
            profile_img = i["profile"]["image_72"]
        except KeyError:
            profile_img = ""

        user_dict[i["id"]] = {"name": i["name"],
                              "real_name": real_name,
                              "profile_img": profile_img}

    return user_dict


def GetConversationInfo(channel_id: str) -> dict:
    # channel_id = "C049P5T2F7H"
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": "Bearer "+str(os.environ.get("SLACK_BOT_TOKEN"))}
    payload = {"channel": channel_id}
    
    # , "cursor":""
    # メッセージ一覧の取得
    response = requests.get(url, headers=headers, params=payload)
    conversation_data = response.json()
    # print(json.dumps(conversation_data, indent=2, ensure_ascii=False))
    
    conversation_dict = dict()
    for i in conversation_data["messages"]:
        # try:
        #     files=i["files"]
        # except KeyError:
        #     files=""
        
        # if files != "":
        #     files_name = i["files"]["name"]
        #     files_url = i["files"]["url_private"]
        # else:
        #     files_name =""
        #     files_url = ""
        conversation_dict[i["ts"]] = {"user": i["user"], \
                                    "text": i["text"], }\
                                    # "files_name": files_name, \
                                    # "files_url": files_url}

    return conversation_dict


def main():
    # 環境変数の読み取り
    dotenv.load_dotenv()
    # GetChannelInfo()
    # GetUserInfo()
    GetConversationInfo("C049P5T2F7H")


if __name__ == '__main__':
    main()
