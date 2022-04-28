import pandas as pd

df = pd.read_csv("Final CSV/Prospection_Client_1_scrapped_at_2022-04-13.csv", sep=";")
print(df)
"""web_site_list = df["Site internet"].tolist()
print(web_site_list)"""

for web_site in df["Site internet"]:
    print(web_site)

import random


print(random.randrange(1000000000,2000000000)/1000000000)