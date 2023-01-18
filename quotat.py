import json
import requests


with open("config.json") as config_file:
    config = json.load(config_file)
api_key = config["openai_api_key"]


headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}
response = requests.get(
    f'https://api.openai.com/v1/usage/api-keys/{api_key}', headers=headers)

usage = response.json()
print(usage)