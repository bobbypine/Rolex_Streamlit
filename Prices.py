import pandas as pd
import streamlit as st
from urllib.error import URLError
# import bitdotio
# import config
import ref_search

st.set_page_config(page_title='Rolex Resale Prices', page_icon='crown.png', layout='wide')


@st.cache
class RolexPrices:
    def __init__(self):
        self.raw = 'https://raw.githubusercontent.com/bobbypine/Rolex/main/Prices/Weekly_Median_Prices.csv'
        self.data = pd.read_csv(self.raw)
        self.data['Date'] = pd.to_datetime(self.data['Date'], yearfirst=True, format='%m-%d-%Y')
        self.data.set_index('Date', inplace=True)
        self.download = self.data.to_csv()
        # self.b = bitdotio.bitdotio(config.key)
        # self.connection = self.b.get_connection()
        # self.raw = f'''select * from "{config.user_name}/rolex_prices"."Weekly_Median_Prices.csv";'''
        # self.download = pd.read_sql(self.raw, self.connection).set_index('Date').to_csv()
        # self.prices = f'''select * from "{config.user_name}/rolex_prices"."Prices";'''
        # self.listings = f'''select * from "{config.user_name}/rolex_prices"."Listings";'''
        # self.markup = f'''select * from "{config.user_name}/rolex_prices"."Markup";'''

    def rolex_price_data(self):
        # prices = pd.read_sql(self.prices, self.connection).set_index('Date')
        # listing_data = pd.read_sql(self.listings, self.connection).set_index('Date')
        # markup_data = pd.read_sql(self.markup, self.connection).set_index('Date')
        prices = self.data.loc[:, list(self.data.columns[0:4]) + list(self.data.columns[12:16]) + list(self.data.columns[24:25])]
        listing_data = self.data.loc[:, list(self.data.columns[4:8]) + list(self.data.columns[16:20]) + list(self.data.columns[25:26])]
        markup_data = self.data.loc[:, list(self.data.columns[8:12]) + list(self.data.columns[20:24]) + list(self.data.columns[26:27])]


        try:
            st.image('crown.png', use_column_width=True)
            reference_selection = st.multiselect("Choose Reference", list(prices.columns), ["124270"])
            listings = [f'{x} Listings' for x in reference_selection]
            markups = [f'{x} Markup' for x in reference_selection]

            if not reference_selection:
                st.error("Please Select a Reference Number")
            else:
                names = {'124270': 'Explorer', '124300': 'OP 41', '126610LN': 'Submariner Date', '126710BLRO': 'GMT-Master II (Blue/Red)',
                        '124060': 'Submariner', '126610LV': 'Submariner Date (Green)', '126710BLNR': 'GMT-Master II (Black/Blue)',
                        '226570': 'Explorer II', '116500LN': 'Daytona'}
                price_data = prices[reference_selection]
                listing_data = listing_data[listings]
                image_list = []
                caption_list = []
                for x in reference_selection:
                    image_list.append(f'{x}.png')
                    caption_list.append(names[x])
                st.subheader("Selection")
                st.image(image_list, caption=caption_list, output_format='PNG', width=200)
                col1, col2, col3 = st.columns([3, 1,  1])
                col1.header("Pricing")
                col2.header('   ')
                col3.header('   ')
                col1.line_chart(price_data)
                for x in reference_selection:
                    col2.metric(label=f'{x} Latest Price', value='${:,.0f}'.format(price_data[f'{x}'].tail(1).item()),
                                delta=(price_data[f'{x}'].tail(1).item() - price_data[f'{x}'].iloc[-2].item()))
                    col3.metric(label=f'{x} Markup', value=str(int(markup_data[f'{x} Markup'].tail(1).item())) + '%')
                col4, col5 = st.columns([3,1])
                col4.header('Listings')
                col5.header('   ')
                col4.bar_chart(listing_data)
                for x in reference_selection:
                    col5.metric(label=f'{x} Latest Listings', value=listing_data[f'{x} Listings'].tail(1).item(),
                                delta=(listing_data[f'{x} Listings'].tail(1).item() - listing_data[f'{x} Listings'].iloc[-2].item()))
            st.subheader('Looking for a different reference?')
            search = st.text_input('Enter reference number for pricing and listing data', ' ')
            if search == ' ':
                st.write(' ')
            else:
                with st.spinner(text='Gathering Data...'):
                    st.write(ref_search.prices(search))
            with st.expander('About the Data'):
                st.write("""All resell pricing and listing information is sourced from Chrono24. Data is gathered on
                    a weekly basis on Friday. Prices are the median asking price for the selected reference in new/unworn condition with box and papers. 
                    Where applicable references are not specific to a single configuration (i.e. dial colors).
                    Values are inclusive of MSRP increases occurring in January of 2022. 
                    Not affiliated with Rolex S.A. or its subsidiaries.""")
            st.download_button(label="Download Data", data=self.download, file_name='Rolex_Data.csv', mime='text/csv')

        except URLError as e:
            st.error(f'This Demo Requires Internet Access: {e.reason}')


if __name__ == "__main__":
    RolexPrices().rolex_price_data()
