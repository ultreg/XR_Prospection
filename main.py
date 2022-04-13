from scrapy.crawler import CrawlerProcess
from generate_prospect_by_company_size_using_btn import ProspectSpiderPerCompanySize
from generate_prospect_by_county_using_btn import ProspectSpiderPerCountry
from generate_prospect_by_sign_date_using_btn import ProspectSpiderPerDate
from generate_prospect_company_name_link_using_next_btn import ProspectSpiderLinkUsingNextBtn
from manipulation_csv import manipulation_CSV
import os
import pandas as pd


def CheckingProspectionNumber():
    liste_of_csv = os.listdir("Final CSV")
    if liste_of_csv:
        for letter in liste_of_csv[-1]:
            if letter.isnumeric():
                return int(letter) + 1
    else:
        print("No CSV file")
        return 1


num_of_prospect_file = CheckingProspectionNumber()


class ScrappListEmployeEngage:
    def __init__(self):
        # run spider
        process = CrawlerProcess(settings={
            'FEED_FORMAT': 'csv'
        })
        process.crawl(ProspectSpiderPerCompanySize)
        process.crawl(ProspectSpiderPerCountry)
        process.crawl(ProspectSpiderPerDate)
        process.crawl(ProspectSpiderLinkUsingNextBtn)

        process.start()

        # Merge all csv in one
        manipulation_CSV(num_of_prospect_file)


while (True):
    user_decision = input("\n\nXR_Prospection !\n\n"
                          "Si vous voulez scrapper le site de la liste des employeur engagés tapez 1\n"
                          "Cela vous créeras un nouveau fichier CSV implémenter de 1 avec la date du scrapping\n\n"
                          "Si vous voulez voir les différences entre différent fichier CSV taper 2\n\n"
                          "Si vous voulez quitter tapper 0\n\n"
                          "Votre réponse : ")

    if user_decision == "1":
        print("\nLe scrapping est en cours ...")
        ScrappListEmployeEngage()
    elif user_decision == "2":
        print("\nVous aller indiquer les 2 numéro des fichiers à "
              "comparer\n")
        for i, csv in enumerate(os.listdir("Final CSV")):
            print(str(i + 1) + " " + csv)

        user_decision_csv_file_compare_first_num = input("\n\n"
                                                         "Indiquer le numéro du premier fichier\n\n"
                                                         "Votre réponse : ")
        user_decision_csv_file_compare_secod_num = input("\nIndiquer le numéro du second fichier\n\n"
                                                         "Votre réponse : ")

        liste_of_csv = os.listdir("Final CSV")
        try :
            print("\nComparaison du fichier --{}-- et du fichier --{}--".format(
                liste_of_csv[int(user_decision_csv_file_compare_first_num) - 1],
                liste_of_csv[int(user_decision_csv_file_compare_secod_num) - 1]))
        except:
            print("\nFichier introuvable")
            continue

        print("\nLes différences sont : \n")
        something_new = False
        print("Final CSV/"+liste_of_csv[int(user_decision_csv_file_compare_first_num) - 1])
        df_1 = pd.read_csv("Final CSV/"+liste_of_csv[int(user_decision_csv_file_compare_first_num) - 1], sep=";")
        df_2 = pd.read_csv("Final CSV/"+liste_of_csv[int(user_decision_csv_file_compare_secod_num) - 1], sep=";")
        dif = pd.concat([df_1, df_2]).drop_duplicates(keep=False)
        if dif.empty:
            print("Il n'y a pas de différences entres les 2 fichiers")

    elif user_decision == "0":
        break
    else:
        print("\nCommande invalide")
