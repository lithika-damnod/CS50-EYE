import requests

BASE = "http://127.0.0.1:500/"

response = requests.get(BASE + "helloworld")
print(response.json()) 