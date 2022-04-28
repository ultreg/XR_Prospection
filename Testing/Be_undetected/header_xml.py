import yaml

with open("user_agents.yml") as f_headers:
    browser_header = yaml.safe_load(f_headers)
print(browser_header["Firefox"])
