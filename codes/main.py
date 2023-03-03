import os

import dotenv
import SlackAPI


def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    
    SlackAPI.SendMessage("ログを取得するのスクリプトが開始されたよ")
    
    ChannelInfo = SlackAPI.GetChannelInfo()
    UserInfo = SlackAPI.GetUserInfo()
    ConversationInfo = SlackAPI.GetAllConversationInfo(list(ChannelInfo.keys()))
    print(SlackAPI.GetAllReplyInfo(list(ChannelInfo.keys()), ConversationInfo))
    
    SlackAPI.SendMessage("ログを取得するのスクリプトが正常に終わったよ")
    return 0


if __name__ == '__main__':
    main()