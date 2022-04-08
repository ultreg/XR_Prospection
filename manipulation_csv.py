import pandas as pd
import pandas as pd

name_company_link = pd.read_csv("name_company_link.csv")
name_company_link.duplicated().sum()
name_company_link_company_size = pd.read_csv("name_company_link_company_size.csv")
name_company_link_company_size.duplicated().sum()
name_company_link_county = pd.read_csv("name_company_link_county.csv")
name_company_link_county.duplicated().sum()
name_company_link_date = pd.read_csv("name_company_link_date.csv")
name_company_link_date.duplicated().sum()
result = pd.merge(name_company_link, name_company_link_company_size, on=["company_name", "link_company", "name_signatory"], how="outer")
result2 = pd.merge(result, name_company_link_county, on=["company_name", "link_company", "name_signatory"], how="outer")
result_final = pd.merge(result2, name_company_link_date, on=["company_name", "link_company", "name_signatory"], how="outer")
result_final.drop_duplicates(inplace=True)
result_final = result_final.sort_values("date", ascending=False)
#Replacing Nan by 0 in county
result_final["county"] = result_final["county"].fillna(0)
result_final = result_final.astype({'county' : "int8"})
result_final["date"] = result_final["date"].fillna(0)
result_final = result_final.astype({'date' : "int16"})
result_final = result_final.astype({'company_size' : "string"})
result_final = result_final.rename(columns={"company_name" : "Nom société", "link_company":"Site internet", "name_signatory":"Nom du signataire", "company_size": "Tranche d'effectif", "county":"Département", "date":"Date de la signature"})
result_final = result_final[["Nom société", "Nom du signataire", "Date de la signature", "Tranche d'effectif", "Département", "Site internet"]]
result_final.to_csv("prospect.csv", index=False, encoding='utf-8-sig')

