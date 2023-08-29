import json
import requests


def send_to_discord(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, data=data)
