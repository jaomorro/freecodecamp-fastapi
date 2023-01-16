import requests
import json


url_base = "http://localhost:8000/"


def get_token(url_path, username, password):

    url = url_base + url_path

    body = {
        "username": username,
        "password": password
    }
    r = requests.post(url, data=body)
    # print(r)
    # print(r.text)
    token_data = json.loads(r.text)
    # return token_data["access_token"]
    return token_data

token_data = get_token("login", "jimmy@gmail.com", "password")
print(token_data)

# connect to an api now that you have a token
access_token = token_data["access_token"]
url = url_base + "posts"
headers = {"Authorization": f"Bearer {access_token}"}
r = requests.get(url, headers=headers)
print(r)
print(r.text)