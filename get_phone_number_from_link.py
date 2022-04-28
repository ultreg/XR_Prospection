""" Validation de phone number :
[https://softhints.com/regex-phone-number-find-validation-python/]
"""
import requests
import bs4
import phonenumbers


url = "https://www.tworoule.com"
number = []
try:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    for match in phonenumbers.PhoneNumberMatcher(response.text, "FR"):
        # print(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        # This line write all phone number
        if "+33" in phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL):
            print("French Number : " + phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
            # Only get Fr number
            number.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))

except:
    print('Failed')

number = list(dict.fromkeys(number))  # del duplicates
print(number)