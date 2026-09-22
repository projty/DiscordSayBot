# Discord Say Bot

A simple Python script that sends, edits, or deletes a Discord message using either a bot token or a webhook URL, with the full payload defined in a local JSON file.

# Not working?
- Click [here](https://projty.github.io/DiscordSayBot/) to view the website version

## What It Does

The script reads a Discord message payload from a local JSON file (`message.json` by default) and:

- **Sends** a new message to a channel (via bot or webhook).
- **Edits** an existing message (via bot or webhook).
- **Deletes** an existing message (via bot or webhook).

Because the entire payload comes from the JSON file, everything the Discord message API supports works out of the box: plain text, embeds, components (buttons, select menus), attachments, and more.

## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- The [`requests`](https://pypi.org/project/requests/) library

Install dependencies with:

```bash
pip install requests
```

## Setup

### 1. Create a Discord Bot (only if not using a webhook)

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, give it a name, and create it.
3. Go to the **Bot** tab and click **Add Bot**.
4. Copy the **Bot Token** — you'll need it.
5. Under **Privileged Gateway Intents**, enable any intents you need (not required for simply sending messages).

### 2. Invite the Bot to Your Server

1. In the Developer Portal, go to **OAuth2 → URL Generator**.
2. Select the `bot` scope.
3. Under **Bot Permissions**, select at minimum:
   - `Send Messages`
   - `Embed Links` (if you plan to send embeds)
   - `Attach Files` (if you plan to send attachments)
   - `Manage Messages` (required to edit or delete messages sent by other users; not needed for the bot's own messages)
   - `Manage Channels` (only needed if the bot will post in a locked/read-only channel)
4. Copy the generated URL, open it in your browser, and add the bot to your server.

> [!WARNING]
> Avoid granting `Administrator` unless you fully trust the bot. It is not required for any feature of this script.

### 3. Get the Target Channel ID (bot mode only)

1. In Discord, enable **Developer Mode** (User Settings → Advanced → Developer Mode).
2. Right-click the channel you want to target and select **Copy Channel ID**.

### 4. (Optional) Create a Webhook

1. In Discord, open the target channel's settings → **Integrations → Webhooks**.
2. Click **New Webhook**, name it, pick a channel, and copy the **Webhook URL**.
3. Paste it into `WEBHOOK_URL` in the script.

### 5. Configure the Script

Open `sendjson.py` and replace the placeholders:

| Constant | Description |
|---|---|
| `CHANNEL_ID` | Target channel ID (bot mode). |
| `BOT_TOKEN` | Your bot token (bot mode). |
| `WEBHOOK_URL` | Webhook URL (webhook mode). Leave empty to use the bot. |
| `MESSAGE_ID` | Required for `--edit` and `--delete`. |

> [!WARNING]
> Never share your bot token or webhook URL, and never commit them to a public repository. Anyone with them can control your bot or webhook.

### 6. Create `message.json`

The script reads the entire Discord message payload from `message.json`. The contents are sent as-is.

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
  "content": "Follow the Discord guidelines!",
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

Send a new message (default):

```bash
python sendjson.py
```

Send a new message explicitly:

```bash
python sendjson.py --send
```

Edit an existing message (requires `MESSAGE_ID`):

```bash
python sendjson.py --edit
```

Delete an existing message (requires `MESSAGE_ID`):

```bash
python sendjson.py --delete
```

Force webhook mode (overrides the bot token):

```bash
python sendjson.py --send --webhook
```

Use a different payload file:

```bash
python sendjson.py --file other_message.json
```

Expected output on success:

```
Message sent successfully!
```

On failure, the script prints the HTTP status code and the error response body from Discord.

## How It Works

**Bot mode (`--send`, `--edit`, `--delete`):**

- `POST   https://discord.com/api/v10/channels/{CHANNEL_ID}/messages`
- `PATCH  https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{MESSAGE_ID}`
- `DELETE https://discord.com/api/v10/channels/{CHANNEL_ID}/messages/{MESSAGE_ID}`

Authentication header: `Authorization: Bot {BOT_TOKEN}`.

**Webhook mode:**

- `POST   {WEBHOOK_URL}`
- `PATCH  {WEBHOOK_URL}/messages/{MESSAGE_ID}`
- `DELETE {WEBHOOK_URL}/messages/{MESSAGE_ID}`

No `Authorization` header is used the webhook URL itself contains the token.

A `200`, `201`, or `204` response means the operation succeeded.

## Troubleshooting

| Status Code | Meaning | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or missing bot token / webhook URL | Double-check `BOT_TOKEN` or `WEBHOOK_URL` |
| `403 Forbidden` | Bot lacks permission in that channel | Grant `Send Messages` (and `Manage Messages` for edit/delete on others' messages) |
| `404 Not Found` | Wrong channel ID, message ID, or webhook URL | Verify `CHANNEL_ID`, `MESSAGE_ID`, or `WEBHOOK_URL` |
| `400 Bad Request` | Malformed JSON payload | Validate `message.json` against the API docs |
| `429 Too Many Requests` | Rate limited | Wait and retry; Discord will tell you how long |

Do you think [discord](https://discord.com) is down? [Click here](https://status.discord.com) for information.

## Notes

- The script runs once per invocation it does not stay running or listen for events.
- `--edit` replaces the message content with whatever is in the JSON file. To keep existing fields, use Discord's `PATCH` semantics (only the fields you provide are changed).
- `--delete` ignores the JSON file entirely; `MESSAGE_ID` is the only input needed.
- Webhooks cannot edit or delete arbitrary user messages only messages they posted.
- To change the message, edit `message.json` no code changes required.
