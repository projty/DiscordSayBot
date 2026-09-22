import requests
import json

# configuration 
CHANNEL_ID = "1234356789123456799"   # replace with your channel ID where you want the message to be sent
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" # replace with your bot token

# Don't make modifications in the code beneath this, unless you know what you are doing 

JSON_FILE = "message.json"
url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
} 

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200 or response.status_code == 201:
    print("Message sent successfully!")
else:
    print(f"Failed to send message ({response.status_code})")
    print(response.text)
    
# Discord Say Bot 1.0.8
