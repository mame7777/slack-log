import requests
import json
import dotenv
import os

# 辞書型のチャンネルデータを取得
def GetChannelInfo() -> dict:
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": "Bearer "+str(os.environ.get("SLACK_BOT_TOKEN"))}
    
    # チャンネル一覧の取得
    response = requests.get(url, headers=headers)
    channel_data = response.json()
    
    # #インデントをつけてさらに見やすい形式に変換
    # channel_json = json.dumps(channel_data, indent=2, ensure_ascii=False)
    
    # 辞書型のチャンネルデータを生成
    channeldict = dict()
    for i in channel_data["channels"]:
        channeldict[i["name"]] = {"id": i["id"], \
                                "topic": i["topic"]["value"], \
                                "purpose": i["purpose"]["value"]}

    return channeldict

def main():
    # 環境変数の読み取り
    dotenv.load_dotenv()
    result=GetChannelInfo()

if __name__=='__main__':
    main()
