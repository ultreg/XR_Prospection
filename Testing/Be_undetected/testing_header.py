import requests

response = requests.get("https://httpbin.org/user-agent")
print(response.json())
# User agent is Python, Web site can see that

headers = {"user-agent": "toto"}
response_change = requests.get("https://httpbin.org/user-agent", headers=headers)
print(response_change.json())
# Changemement du header user agent

response_all_header = requests.get("https://httpbin.org/headers")
print(response_all_header.json())