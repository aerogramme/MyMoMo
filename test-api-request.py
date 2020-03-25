import requests

url = "https://kubedoc.appspot.com/momo/api/v1/balance/0244150150"

payload = ""
headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic ZnJlZXdvcmxkYm9zczokNSRyb3VuZHM9NTM1MDAwJGdVZi9LYW5NNE13THRsMWQkQXk5M0RyTUswSkpSZFJPSWRkelhvTk9KTjEyLjhZdHd2RXZrdmFyTTJ3Qw==",
    'User-Agent': "PostmanRuntime/7.18.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "f6422e7a-0eb5-47e5-aa18-b5bd1f99858f,45e3ef06-aef6-435c-ab01-39d5f95cf0ab",
    'Host': "kubedoc.appspot.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, data=payload, headers=headers)


if(response.status_code == 200):
    print(response.text)
    print(response.reason)
