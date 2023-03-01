import requests
import json
import dotenv
import os

dotenv.load_dotenv()

requests.post(os.environ.get("WEB_HOOK_URL"), data=json.dumps ({
   # message
   "text": "これはテストだよ\n<https://google.com|google>もびっくり",
   "username": "テスト用bot",
   "icon_emoji": ":pien:",  
   "channel": "#bot_try"
}))