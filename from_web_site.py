""" Validation de phone number :
[https://softhints.com/regex-phone-number-find-validation-python/]
"""
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import random
import pandas as pd
import phonenumbers
import nltk
from nameparser.parser import HumanName
import sys


def testing_2_surname_base_in_phone_number(list_to_test: list):
    surname_potentially_for_number = set()
    fr_surname = pd.read_csv(
        r"C:\Users\Bluepollen_F_002\Desktop\ProspectDataScrapper\dataset\Prenom_fr_no_double.csv",
        sep=",")
    us_surnames = pd.read_csv(
        r"C:\Users\Bluepollen_F_002\Desktop\ProspectDataScrapper\dataset\surname_US.csv")

    for i, text in enumerate(list_to_test):
        for surname in fr_surname["01_prenom"]:
            try:
                if surname.capitalize() == text.capitalize():
                    surname_potentially_for_number.add(
                        list_to_test[i - 1] + " " + list_to_test[i] + " " + list_to_test[i + 1])
            except AttributeError:
                pass

    for i, text in enumerate(list_to_test):
        for us_surname in us_surnames["name"]:
            try:
                if us_surname.capitalize() == text.capitalize():
                    surname_potentially_for_number.add(
                        list_to_test[i - 1] + " " + list_to_test[i] + " " + list_to_test[i + 1])
            except AttributeError:
                pass
    return surname_potentially_for_number


def testing_2_surname_base(list_to_test: list):
    fr_surname = pd.read_csv(
        r"C:\Users\Bluepollen_F_002\Desktop\ProspectDataScrapper\dataset\Prenom_fr_no_double.csv",
        sep=",")
    us_surnames = pd.read_csv(
        r"C:\Users\Bluepollen_F_002\Desktop\ProspectDataScrapper\dataset\surname_US.csv")

    for i, text in enumerate(list_to_test):
        for surname in fr_surname["01_prenom"]:
            try:
                if surname.capitalize() == text.capitalize():
                    return True
            except AttributeError:
                pass

    for i, text in enumerate(list_to_test):
        for us_surname in us_surnames["name"]:
            try:
                if us_surname.capitalize() == text.capitalize():
                    return True
            except AttributeError:
                pass
    return False


def get_web_site_list_from_csv():
    df = pd.read_csv("Final CSV/Prospection_Client_1_scrapped_at_2022-04-13.csv", sep=";")
    web_site_list = df["Site internet"].tolist()
    return web_site_list, df


def get_all_link_web_site_url(url):
    all_link = []
    new_list = []
    facebook = []
    twitter = []
    linkedin = []
    instagram = []

    response = requests.get(url)
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
            if url in link:
                new_list.append(link)
            else:
                pass
        except:
            pass

    new_list = list(dict.fromkeys(new_list))  # del duplicates
    facebook = list(dict.fromkeys(facebook))  # del duplicates
    twitter = list(dict.fromkeys(twitter))  # del duplicates
    linkedin = list(dict.fromkeys(linkedin))  # del duplicates
    instagram = list(dict.fromkeys(instagram))  # del duplicates

    try:
        facebook = get_min_size_link(facebook)
    except ValueError:  # Empty list
        pass
    try:
        twitter = get_min_size_link(twitter)
    except ValueError:  # Empty list
        pass
    try:
        linkedin = get_min_size_link(linkedin)
    except ValueError:  # Empty list
        pass
    try:
        instagram = get_min_size_link(instagram)
    except ValueError:  # Empty list
        pass

    return new_list, facebook, twitter, linkedin, instagram


def get_min_size_link(list_of_url):
    return min(list_of_url)


def get_email_from_url(url_list):
    emails = set()
    for url in url_list:

        time_to_wait = random.randrange(1000000000, 3000000000) / 1000000000
        # print("Waiting " + str(time_to_wait))
        time.sleep(time_to_wait)  # random range sleep
        # print("Scrapping " + url)
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


def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:  # avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return person_list


def get_surname(text):
    pass


def get_phone_number_and_name(url_list):
    potentiel_name_found = {}
    surname_potentially_for_number = set()
    number_person = {}
    for url in url_list:
        response = requests.get(url)
        for i, match in enumerate(phonenumbers.PhoneNumberMatcher(response.text, "FR")):
            # print(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
            # This line write all phone number
            if "+33" in phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL):
                """print("French Number : " + phonenumbers.format_number(match.number,
                                                                      phonenumbers.PhoneNumberFormat.INTERNATIONAL))"""
                # Only get Fr number
                location_list_interval = list(map(int, str(match).split()[1][1:-1].split(",")))
                new_location_for_trying_detection = [location_list_interval[0] - 500,
                                                     location_list_interval[1] + 500]  # Get arround phone number
                html_content = response.text[new_location_for_trying_detection[0]:new_location_for_trying_detection[1]]
                soup = bs(html_content, "lxml")
                body = soup.body.text
                surname_potentially_for_number = testing_2_surname_base_in_phone_number(body.split())
                person_list_by_ml = get_human_names(
                    response.text[new_location_for_trying_detection[0]:new_location_for_trying_detection[1]])
                for elem in person_list_by_ml:
                    surname_potentially_for_number.add(elem)
                # print("res :")
                # print(response.text[new_location_for_trying_detection[0]:new_location_for_trying_detection[1]])
                # Get person surname - name
                if len(surname_potentially_for_number) == 1:
                    need_to_verify = False
                else:
                    need_to_verify = True
                number_person[phonenumbers.format_number(match.number,
                                                         phonenumbers.PhoneNumberFormat.INTERNATIONAL)] = [
                    surname_potentially_for_number, "detected on {}".format(url),
                    "need to verify : {}".format(need_to_verify)]

        potentiel_name_found[url] = get_human_names(response.text)

    return number_person, potentiel_name_found


def get_info_from_web_site(url):
    # url = "https://www.tworoule.com"
    url = "https://xroad-formation.com/"
    list_of_url, facebook, twitter, linkedin, instagram = get_all_link_web_site_url(url)
    print("all link in web site :")
    print(list_of_url)
    print("Facebook :")
    print(facebook)
    print("Twitter :")
    print(twitter)
    print("Linkedin :")
    print(linkedin)
    print("Instagram :")
    print(instagram)
    print(get_email_from_url(list_of_url))
    number_person, potentiel_name_found = get_phone_number_and_name(list_of_url)
    print(number_person)
    data = {'Facebook_link': facebook,
            'Twitter_link': twitter,
            'Linkedin_link': linkedin,
            'Instagram_link': instagram,
            'Email_extract' : get_email_from_url(list_of_url),
            }
    df = pd.DataFrame(data)
    print(df)


url = "https://xroad-formation.com/"
get_info_from_web_site(url)

# Le responsable du traitement des données à caractère personnel est Monsieur Quentin MORETTE qui peut être contacté par courriel (hello.tworoule@gmail.com) et par téléphone au 06.85.34.51.12.
# C'est le co fondateur (vu sur Linkedin)
