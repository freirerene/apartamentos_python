from selenium import webdriver
import pickle
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# This file retrieves the data from imovelweb -- a site that collects data from a bunch of real estate agencies
# Unfortunately, we tried using the much simpler requests together with bs, but the site was blocking us
# So we used selenium, instead, with chromedrive.

html_source = []
for i in range(1,1000):
    driver = webdriver.Chrome()
    driver.get("https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp-pagina-" + str(i) + ".html")
    sleep(.7)
    html_source.append(driver.page_source)
    sleep(.5)
    driver.close()

# Let's just save the html_source, just in case.
with open('html_sources.data', 'wb') as filehandle:
    pickle.dump(html_source, filehandle)

# To open the .data file, if need be:
# with open('html_sources.data', 'rb') as filehandle:
#     html_source = pickle.load(filehandle)

# Now we construct the dataframe
soup = [BeautifulSoup(source, 'html.parser') for source in html_source]
apartamentos = []
for page in soup:
    for card in page.find_all("div", {"data-posting-type": "PROPERTY"}):
        apartamentos.append(card)

aluguel, condominio = [], []
bairro = []
area, quartos, banheiros, garagem = [], [], [], []
anunciante = []

for ap in apartamentos:
    try:
        aluguel.append(ap.find("span", {"class": "firstPrice"}).text)
    except:
        aluguel.append(np.nan)
    try:
        condominio.append(ap.find("span", {"class": "postingCardExpenses"}).text)
    except:
        condominio.append(np.nan)
        
    try:
        bairro.append(ap.find("span", {"class": "postingCardLocation go-to-posting"}).text)
    except:
        bairro.append(np.nan)

    try:
        area.append(ap.find("i", {"class": "postingCardIconsFeatures iconArea"}).next)
    except:
        area.append(np.nan)
        
    try:
        quartos.append(ap.find("i", {"class": "postingCardIconsFeatures iconBedrooms"}).next)
    except:
        quartos.append(np.nan)
        
    try:
        banheiros.append(ap.find("i", {"class": "postingCardIconsFeatures iconBathrooms"}).next)
    except:
        banheiros.append(np.nan)
        
    try:
        garagem.append(ap.find("i", {"class": "postingCardIconsFeatures iconGarage"}).next)
    except:
        garagem.append(np.nan)
        
    try:
        anunciante.append(ap.find("div", {"class": "publisherLogo"}).find('a').get('href'))
    except:
        anunciante.append(np.nan)

data = {'aluguel': aluguel, 'condominio': condominio, 'area': area, 'bairro': bairro, 'quartos': quartos, 'banheiros': banheiros, 'garagem': garagem, 'anunciante': anunciante}

df = pd.DataFrame(data)

df.to_csv('apartamentos.csv')
