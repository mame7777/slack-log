import requests
import json
import dotenv
import os
import time

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
        # 画像を取得できない人の分をスキップ
        # 他の画像を探すようにしたいね
        profile_img = i.get("profile", "")

        user_dict[i["id"]] = {"name": i["name"],
                              "real_name": i.get("real_name", ""),
                              "profile_img": profile_img.get("image_72", "")}

    return user_dict


def GetConversationInfo(channel_id: str) -> dict:
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": "Bearer " +
               str(os.environ.get("SLACK_BOT_TOKEN"))}
    payload = {"channel": channel_id}

    # メッセージ一覧の取得
    response = requests.get(url, headers=headers, params=payload)
    conversation_data = response.json()
    print(json.dumps(conversation_data, indent=2, ensure_ascii=False))

    conversation_dict = dict()

    if conversation_data["ok"]:
        while True:
            for i in conversation_data["messages"]:
                conversation_dict[i["ts"]] = {
                    "user": i["user"], "text": i["text"], "reply_count": i.get("reply_count", "0")}

            if conversation_data["has_more"]:
                # APIレートの調整
                time.sleep(1.35)
                payload = {"channel": channel_id,
                           "cursor": conversation_data["response_metadata"]["next_cursor"]}
                response = requests.get(url, headers=headers, params=payload)
                conversation_data = response.json()
            else:
                break

    return conversation_dict


def GetAllConversationInfo(channnel_list: list) -> dict:
    ALLconversation_dict = dict()
    for channel_id in channnel_list:
        ALLconversation_dict[channel_id] = GetConversationInfo(channel_id)
        # APIレートの調整
        time.sleep(1.35)

        # if channel_id == "C1GQGJURK":
        #     break

    return ALLconversation_dict


def GetReplysInfo(channel_id: str, history_ts_list: list) -> dict:
    reply_dict = dict()
    for history_ts in history_ts_list:
        url = "https://slack.com/api/conversations.replies"
        headers = {"Authorization": "Bearer " +
                   str(os.environ.get("SLACK_BOT_TOKEN"))}
        payload = {"channel": channel_id, "ts": history_ts}

        # メッセージ一覧の取得
        response = requests.get(url, headers=headers, params=payload)
        reply_data = response.json()
        print(json.dumps(reply_data, indent=2, ensure_ascii=False))

        if reply_data["ok"]:
            reply_dict_temp = dict()
            while True:
                for i in reply_data["messages"]:
                    reply_dict_temp[i["ts"]] = {
                        "user": i["user"], "text": i["text"]}

                if reply_data["has_more"]:
                    # APIレートの調整
                    time.sleep(1.35)
                    payload = {"channel": channel_id, "ts": history_ts,
                               "cursor": reply_data["response_metadata"]["next_cursor"]}
                    response = requests.get(
                        url, headers=headers, params=payload)
                    reply_data = response.json()
                else:
                    break
            reply_dict[history_ts] = {"reply_dict": reply_dict_temp}

        # APIレートの調整
        time.sleep(1.35)

    return reply_dict


def GetAllReplyInfo(channnel_list: list, ALLconversation_dict: dict) -> dict:
    ALLReply_dict = dict()
    for channel_id in channnel_list:
        conversation_dict = ALLconversation_dict[channel_id]

        ts_HasReply_list = list()
        for ts_in_loop in conversation_dict.keys():
            if int(conversation_dict[ts_in_loop]["reply_count"]) > 0:
                ts_HasReply_list.append(ts_in_loop)

        ALLReply_dict[channel_id] = GetReplysInfo(channel_id, ts_HasReply_list)

        # if channel_id == "C1GQGJURK":
        #     break

    return ALLReply_dict


def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    ChannelInfo = GetChannelInfo()
    UserInfo = GetUserInfo()
    ConversationInfo = GetAllConversationInfo(list(ChannelInfo.keys()))
    print(GetAllReplyInfo(list(ChannelInfo.keys()), ConversationInfo))
    return 0


if __name__ == '__main__':
    main()
