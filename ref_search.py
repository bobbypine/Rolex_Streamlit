import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import numpy as np


def prices(ref):
    price_list = []
    for x in range(1, 6):
        url = 'https://www.chrono24.com/search/index.htm?currencyId=USD&dosearch=true&facets=condition&facets=specials&facets=usedOrNew&facets=availability&maxAgeInDays=0&pageSize=120&query=Rolex+{}&redirectToSearchIndex=true&resultview=block&searchexplain=1&showpage={}&sortorder=0&specials=102&usedOrNew=new'.format \
            (ref, x)
        response = requests.get(url=url, verify=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        for prices in soup.findAll('strong')[5:]:
            price_list.append(prices.text)
    data = pd.DataFrame(price_list)
    data.rename(columns={0: ref}, inplace=True)
    data[ref] = data[ref].str.replace('\n', '', regex=False).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
    data = data.loc[(data[ref].str.isnumeric())]
    data[ref] = data[ref].astype('int')
    data[f'{ref} Listings'] = len(data)
    data['Date'] = datetime.date.today().strftime('%m-%d-%Y')
    data.set_index('Date', inplace=True)
    median = np.median(data[ref])
    return f'{ref} Median Price: ${median}, {len(data)} Observations'



