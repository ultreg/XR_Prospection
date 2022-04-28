import requests
import yaml

with open("../../headers.yml") as f_headers:
    browser_headers = yaml.safe_load(f_headers)


response = requests.get("https://httpbin.org/headers", headers=browser_headers["Firefox"])
print(response.json())