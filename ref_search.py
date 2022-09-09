import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import numpy as np
import os


def prices(ref):
    price_list = []
    for x in range(1,6):
        try:
            url = f'https://www.chrono24.com/search/index.htm?currencyId=USD&dosearch=true&facets=condition&facets=specials&facets=usedOrNew&facets=availability&maxAgeInDays=0&pageSize=120&query=Rolex+{ref}&redirectToSearchIndex=true&resultview=block&searchexplain=1&showpage={x}&sortorder=0&specials=102&usedOrNew=new'
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1200")
            DRIVER_PATH = os.environ.get('cd_path')
            driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
            driver.get(url)
            element = driver.find_elements(By.ID, "wt-watches")[0].get_attribute("innerHTML")
            soup = BeautifulSoup(element, 'html.parser')
            for items in soup.findAll('div', {'class':'d-flex justify-content-between align-items-end m-b-2'}):
                for price in items.findAll('div', {'class':'text-bold'}):
                    price_list.append(price.text.strip())
            driver.quit()
        except:
            break
    data = pd.DataFrame(price_list)
    data.rename(columns={0: ref}, inplace=True)
    data[ref] = data[ref].str.replace('\n', '', regex=False).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
    data = data.loc[(data[ref].str.isnumeric())]
    data[ref] = data[ref].astype('int')
    data[f'{ref} Listings'] = len(data)
    data['Date'] = datetime.date.today().strftime('%m/%d/%Y')
    data.set_index('Date', inplace=True)
    median = np.median(data[ref])
    return f'{ref} Median Price: ${median}, {len(data)} Observations'








