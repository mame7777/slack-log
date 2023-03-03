import os
import time
import datetime

import DB
import dotenv
import SlackAPI


def init_main():
    ChannelInfo = SlackAPI.GetChannelInfo()
    UserInfo = SlackAPI.GetUserInfo()
    ConversationInfo = SlackAPI.GetAllConversationInfo(list(ChannelInfo.keys()))
    ReplyInfo = SlackAPI.GetAllReplyInfo(list(ChannelInfo.keys()), ConversationInfo)
    
    cnx = DB.Connect()
    DB_CT = DB.CreateTable(cnx=cnx)
    # DB.Erase_All_Data(cnx)
    DB_CT.channel()
    DB_CT.user()
    DB_CT.Conversation(channel_dict=ChannelInfo)
    DB_CT.Reply(channel_dict=ChannelInfo)
    
    DB_I = DB.Insert(cnx=cnx)
    DB_I.channel(channel_dict=ChannelInfo)
    DB_I.user(user_dict=UserInfo)
    DB_I.conversation(conversation_dict=ConversationInfo)
    DB_I.reply(reply_dict=ReplyInfo)
    
    DB.EndConnect(cnx)

def main() -> int:
    # 環境変数の読み取り
    dotenv.load_dotenv()
    
    start_time = time.perf_counter()
    
    SlackAPI.SendMessage("ログを取得するのスクリプトが開始されたよ")
    init_main()
    
    # ChannelInfo = SlackAPI.GetChannelInfo()
    # UserInfo = SlackAPI.GetUserInfo()
    # ConversationInfo = SlackAPI.GetAllConversationInfo(list(ChannelInfo.keys()))
    # print(SlackAPI.GetAllReplyInfo(list(ChannelInfo.keys()), ConversationInfo))
    
    time.sleep(1)
    
    end_time = time.perf_counter()
    delta_time = end_time - start_time
    print(datetime.timedelta(seconds=delta_time))
    
    message = "ログを取得するのスクリプトが正常に終わったよ\n経過時間(hh:mm:ss)は >> " + str(datetime.timedelta(seconds=delta_time))
    SlackAPI.SendMessage(message)
    return 0


if __name__ == '__main__':
    main()