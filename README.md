# Discord Say Bot 

A simple Python script that sends a message to a Discord channel using a bot token and a JSON payload file.

## What It Does

This script reads a message definition from a local JSON file (`message.json`) and posts it to a specified Discord channel via the Discord REST API. It supports everything the Discord message API supports plain text, embeds, components (buttons, select menus), attachments, and more since the entire payload is defined in the JSON file.

## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- The [`requests`](https://pypi.org/project/requests/) library

Install dependencies with:

```bash
pip install requests
```

## Setup
**Steps to Reproduce**
### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, give it a name, and create it.
3. Go to the **Bot** tab and click **Add Bot**.
4. Copy the **Bot Token** you'll need it.
5. Under **Privileged Gateway Intents**, enable any intents you need (not required for simply sending messages).

### 2. Invite the Bot to Your Server

1. In the Developer Portal, go to **OAuth2 → URL Generator**.
2. Select the `bot` scope.

4. Under **Bot Permissions**, select at minimum:
   - `Administrator` (all permissions, very risky, use at your own risk)
   - `Manage Channels` (necessary if the bot will send a message to a locked or read-only channels)
   - `Manage Messages` (not important, but you can add it anyway - maybe risky as it allows to delete messages) 
   - `Send Messages`
   - `Embed Links` (if you plan to send embeds)
   - `Attach Files` (if you plan to send attachments)
5. Copy the generated URL, open it in your browser, and add the bot to your server.

### 3. Get the Target Channel ID

1. In Discord, enable **Developer Mode** (User Settings → Advanced → Developer Mode).
2. Right-click the channel you want to send messages to and select **Copy Channel ID**.

### 4. Configure the Script

Open the `sendjson.py` and replace the placeholders:

> [!WARNING]  
> Never share your bot token or commit it to a public repository. Anyone with the token can control your bot.

### 5. Create `message.json`

The script reads the entire Discord message payload from `message.json`. The contents of that file are sent as-is to the API.

**Simple text example:**

```json
{
  "content": "Hello, world!"
}
```

**Embed example:**

```json
{
  "content": "Cool isn't it?",
  "embeds": [
    {
      "title": "My Embed",
      "description": "This is an embed sent by the bot.",
      "color": 5814783
    }
  ]
}
```

**Message with a button component:**

```json
{
  "content": "Follow the discord guidelines!",
  "components": [
    {
      "type": 1,
      "components": [
        {
          "type": 2,
          "style": 5,
          "label": "Visit Discord Guidelines",
          "url": "https://discord.com/guidelines"
        }
      ]
    }
  ]
}
```

For the full schema, see the [Discord Message API documentation](https://discord.com/developers/docs/resources/message).

## Usage

Once configured, simply run:

```bash
python sendjson.py
```

Expected output on success:

```
Message sent successfully!
```

On failure, the script prints the HTTP status code and the error response body from Discord.

## How It Works

1. Loads `message.json` into a Python dictionary.
2. Sends a `POST` request to `https://discord.com/api/v10/channels/{CHANNEL_ID}/messages` using your bot token for authentication.
3. Checks the response, a `200` or `201` status means the message was delivered.

## Troubleshooting

| Status Code | Meaning | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or missing bot token | Double-check `BOT_TOKEN` |
| `403 Forbidden` | Bot lacks permission in that channel | Give the bot `Send Messages` permission |
| `404 Not Found` | Wrong channel ID | Verify `CHANNEL_ID` |
| `400 Bad Request` | Malformed JSON payload | Validate `message.json` against the API docs |
| `429 Too Many Requests` | Rate limited | Wait and retry; Discord will tell you how long |

## Notes

- The script posts a **new** message every time it runs. It does not edit or delete messages. (might come in future)
- To send the same message repeatedly, just run the script again.
- To change the message, edit `message.json` no code changes required.
