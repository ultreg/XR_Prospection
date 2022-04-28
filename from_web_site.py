import requests
from bs4 import BeautifulSoup as bs
import re
import time
import random
import pandas as pd
import phonenumbers


def get_web_site_list_from_csv():
    df = pd.read_csv("Final CSV/Prospection_Client_1_scrapped_at_2022-04-13.csv", sep=";")
    web_site_list = df["Site internet"].tolist()
    return web_site_list, df


def get_all_link_web_site_url():
    all_link = []
    new_list = []
    facebook = []
    twitter = []
    linkedin = []
    instagram = []

    response = requests.get("https://www.tworoule.com")
    soup = bs(response.text, "lxml")

    for link in soup.find_all("a"):
        all_link.append(link.get("href"))

    for link in all_link:
        try:
            if "facebook" in link:
                facebook.append(link)
            if "twitter" in link:
                twitter.append(link)
            if "linkedin" in link:
                linkedin.append(link)
            if "instagram" in link:
                instagram.append(link)
        except:
            pass

    for link in all_link:
        try:
            if "https://www.tworoule.com" in link:
                new_list.append(link)
            else:
                pass
        except:
            pass

    new_list = list(dict.fromkeys(new_list))  # del duplicates

    print("all link in web site :")
    print(new_list)
    print("Facebook :")
    print(facebook)
    print("Twitter")
    print(twitter)
    print("Linkedin")  # TODO Try to get the more short to exclude feed link
    print(linkedin)
    print("Instagram")
    print(instagram)
    return new_list, facebook, twitter, linkedin, instagram


def get_email_from_url(url_list):
    emails = set()
    for url in url_list:

        time_to_wait = random.randrange(1000000000, 3000000000) / 1000000000
        print("Waiting " + str(time_to_wait))
        time.sleep(time_to_wait)  # random range sleep
        print("Scrapping " + url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', response.text, re.I))
        emails.update(new_emails)

        soup = bs(response.text, 'lxml')

        try:
            new_emails_2 = set(soup.select("a[href*=mailto]")[-1].text)
            emails.update(new_emails_2)
        except:
            pass

    emails = list(emails)
    for email in emails:
        if email.endswith("."):
            emails.remove(email)
    return emails


def get_phone_number(url_list):
    number = []
    for url in url_list:
        try:
            response = requests.get(url)
            for match in phonenumbers.PhoneNumberMatcher(response.text, "FR"):
                # print(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
                # This line write all phone number
                if "+33" in phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL):
                    """print("French Number : " + phonenumbers.format_number(match.number,
                                                                          phonenumbers.PhoneNumberFormat.INTERNATIONAL))"""
                    # Only get Fr number
                    number.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))

        except:
            print('Failed')

    number = list(dict.fromkeys(number))
    return number


list_of_url, facebook, twitter, linkedin, instagram = get_all_link_web_site_url()
print(list_of_url)
print(facebook)
print(twitter)
print(linkedin)
print(instagram)
print(get_email_from_url(list_of_url))
print(get_phone_number(list_of_url))

# Le responsable du traitement des données à caractère personnel est Monsieur Quentin MORETTE qui peut être contacté par courriel (hello.tworoule@gmail.com) et par téléphone au 06.85.34.51.12.
# C'est le co fondateur (vu sur Linkedin)
