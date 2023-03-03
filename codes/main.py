import os

import dotenv
import SlackAPI


def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    
    SlackAPI.SendMessage("SlackBotのスクリプトが開始されました。")
    
    ChannelInfo = SlackAPI.GetChannelInfo()
    UserInfo = SlackAPI.GetUserInfo()
    ConversationInfo = SlackAPI.GetAllConversationInfo(list(ChannelInfo.keys()))
    print(SlackAPI.GetAllReplyInfo(list(ChannelInfo.keys()), ConversationInfo))
    
    SlackAPI.SendMessage("SlackBotのスクリプトが正常終了しました。")
    return 0


if __name__ == '__main__':
    main()