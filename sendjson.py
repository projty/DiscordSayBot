import requests
import json
import sys
import os
import argparse
# Discord Say Bot 1.1.5
# Config

CHANNEL_ID = "1234356789123456799"   # Replace with your target channel ID
BOT_TOKEN  = "YOUR_BOT_TOKEN_HERE"   # Replace with your bot token
WEBHOOK_URL = ""                     # Optional: fill in to use a webhook instead of a bot
MESSAGE_ID  = ""                     # Required for --edit and --delete

JSON_FILE = "message.json"


# Do not modify below unless you know what you're doing

API_BASE = "https://discord.com/api/v10"


def load_payload(path: str) -> dict:
    if not os.path.isfile(path):
        print(f"Error: payload file '{path}' not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: '{path}' is not valid JSON: {e}")
            sys.exit(1)


def send_via_bot(payload: dict) -> requests.Response:
    url = f"{API_BASE}/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers, json=payload)


def send_via_webhook(payload: dict) -> requests.Response:
    # Webhooks ignore the Authorization header; they use the URL token.
    headers = {"Content-Type": "application/json"}
    return requests.post(WEBHOOK_URL, headers=headers, json=payload)


def edit_via_bot(payload: dict) -> requests.Response:
    url = f"{API_BASE}/channels/{CHANNEL_ID}/messages/{MESSAGE_ID}"
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json",
    }
    return requests.patch(url, headers=headers, json=payload)


def edit_via_webhook(payload: dict) -> requests.Response:
    url = f"{WEBHOOK_URL}/messages/{MESSAGE_ID}"
    headers = {"Content-Type": "application/json"}
    return requests.patch(url, headers=headers, json=payload)


def delete_via_bot() -> requests.Response:
    url = f"{API_BASE}/channels/{CHANNEL_ID}/messages/{MESSAGE_ID}"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    return requests.delete(url, headers=headers)


def delete_via_webhook() -> requests.Response:
    url = f"{WEBHOOK_URL}/messages/{MESSAGE_ID}"
    return requests.delete(url)


def report(response: requests.Response, action: str) -> None:
    if response.status_code in (200, 201, 204):
        print(f"Message {action} successfully!")
    else:
        print(f"Failed to {action} message ({response.status_code})")
        print(response.text)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send, edit, or delete a Discord message from a JSON payload."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--send", action="store_true", help="Send a new message (default)."
    )
    group.add_argument(
        "--edit", action="store_true", help="Edit an existing message."
    )
    group.add_argument(
        "--delete", action="store_true", help="Delete an existing message."
    )
    parser.add_argument(
        "--webhook",
        action="store_true",
        help="Use WEBHOOK_URL instead of the bot token + channel ID.",
    )
    parser.add_argument(
        "--file",
        default=JSON_FILE,
        help=f"Path to the JSON payload (default: {JSON_FILE}).",
    )
    args = parser.parse_args()

    use_webhook = args.webhook or bool(WEBHOOK_URL)

    if use_webhook and not WEBHOOK_URL:
        print("Error: --webhook specified but WEBHOOK_URL is empty.")
        sys.exit(1)

    if (args.edit or args.delete) and not MESSAGE_ID:
        print("Error: MESSAGE_ID must be set for --edit and --delete.")
        sys.exit(1)

    if args.delete:
        resp = delete_via_webhook() if use_webhook else delete_via_bot()
        report(resp, "deleted")
        return

    payload = load_payload(args.file)

    if args.edit:
        resp = edit_via_webhook(payload) if use_webhook else edit_via_bot(payload)
        report(resp, "edited")
    else:
        resp = send_via_webhook(payload) if use_webhook else send_via_bot(payload)
        report(resp, "sent")


if __name__ == "__main__":
    main()
