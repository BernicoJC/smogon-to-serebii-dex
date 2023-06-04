import requests

from bs4 import BeautifulSoup
from selenium import webdriver

import unicodedata

def filter_japanese(text):
    filtered = ''
    for char in text:
        if unicodedata.category(char) not in ['Lo', 'Mn']:
            filtered += char
    return filtered

serebii = requests.get("https://www.serebii.net/black2white2/unovadex.shtml")
serebii_soup = BeautifulSoup(serebii.content, 'html.parser')
serebii_data = serebii_soup.find_all("td", attrs={"class": "cen"})

pokedex = []

# for i in serebii_data:
#     a_tags = i.find_all("a")
#     for a in a_tags:
#         content = a.string
#         if content:
#             pokedex.append(content)
# THIS IS FOR HGSS https://www.serebii.net/heartgoldsoulsilver/johtodex.shtml

for i in serebii_data:
    a_tags = i.find_all("a")
    for a in a_tags:
        for br in a.find_all("br"):
            br.replace_with("")
            content = a.text
            if content:
                final = filter_japanese(content)
                pokedex.append(final)
# THIS IS FOR BW2 https://www.serebii.net/black2white2/unovadex.shtml

driver = webdriver.Chrome()
driver.get("https://www.smogon.com/dex/bw/formats/pu/")
driver.implicitly_wait(10)

smogon_soup = BeautifulSoup(driver.page_source, 'html.parser')
smogon_data = smogon_soup.find_all("div", attrs={"class": "PokemonAltRow-name"})


tiermons = []

for i in smogon_data:
    spans = i.find_all("span")
    for span in spans:
        content = span.string
        if content:
            tiermons.append(content)

result = []
for i in pokedex:
    for j in tiermons:
        if(i == j):
            result.append(i)

result_string = ""
for i in range(len(result)):
    result_string = result_string + result[i]
    if(i != len(result) - 1):
        result_string = result_string + "\n"

with open("Output.txt", "w") as text_file:
    text_file.write(result_string)

driver.quit