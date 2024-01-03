import os
import requests
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import spacy
from spacy import displacy
from pathlib import Path

response = requests.get('https://en.wikipedia.org/wiki/Joachim_Peiper')
soup = BeautifulSoup(response.content, 'html.parser')

main_article = soup.find('div', class_ = 'mw-content-ltr mw-parser-output')
scrap_text = main_article.find_all('p')

cleaned_data = ''
for paragraph in scrap_text[:2]:
    for tag in paragraph.find_all(['span', 'a']):
        tag.unwrap()

    cleaned_text = re.sub(r'\[.*?\]', '', paragraph.get_text(strip = False))
    # cleaned_text = re.sub(r'\[.*?\]', '', paragraph.get_text())
    # cleaned_text = re.sub(r'(\w)\s*(?=[A-Z])', r'\1 ', paragraph.get_text())
    cleaned_data += cleaned_text

nlp = spacy.load("en_core_web_sm")

doc = nlp(cleaned_data)
#Joachim Peiper (30 January 1915 – 14 July 1976) was a German Schutzstaffel (SS) officer and war criminal convicted 
#for the Malmedy massacre of U.S. Army prisoners of war (POWs).

sentence1 = list(doc.sents)[2]

extract_spo = []
cc_count = 0
for i in list(doc.sents):
    subject = ''
    predicate = ''
    object = ''
    for token in i:
        if subject == '' or predicate == '' or object == '':
            if token.dep_ == 'nsubj':
                subject = token.text
            if token.dep_ == 'ROOT':
                predicate = token.text
            if token.dep_ == 'attr' or token.dep_ == 'conj':
                object = token.text
            # if token.pos_ == 'ADP' and token.dep_ == 'prep':

        else:
            extract_spo.append([subject, predicate, object])
            object = ''
    subject, predicate, object = '', '', ''
        #print(subject, predicate, object, '-------')
print(extract_spo)

# for sent in doc.sents:
#     for ent in sent.ents:
#         print(ent.text)
#     print(sent.)

svg_path = Path("visualization1.svg")
svg_content = displacy.render(sentence1, style="dep")
svg_path.write_text(svg_content)