import pandas as pd
import streamlit as st
from urllib.error import URLError
# import bitdotio
# import config


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
        prices = self.data.loc[:, list(self.data.columns[0:4]) + list(self.data.columns[12:16])]
        listing_data = self.data.loc[:, list(self.data.columns[4:8]) + list(self.data.columns[16:20])]
        markup_data = self.data.loc[:, list(self.data.columns[8:12]) + list(self.data.columns[20:24])]


        try:
            st.image('crown.png', use_column_width=True)
            reference_selection = st.multiselect("Choose Reference", list(prices.columns), ["124270"])
            listings = [f'{x} Listings' for x in reference_selection]
            markups = [f'{x} Markup' for x in reference_selection]

            if not reference_selection:
                st.error("Please Select a Reference Number")
            else:
                price_data = prices[reference_selection]
                listing_data = listing_data[listings]
                image_list = []
                caption_list = []
                for x in reference_selection:
                    image_list.append(f'{x}.png')
                    caption_list.append(x)
                st.subheader("Selection")
                st.image(image_list, caption=caption_list, output_format='PNG', width=200)
                col1, col2, col3 = st.columns([3, 1,  1])
                col1.subheader("Pricing")
                col1.line_chart(price_data)
                for x in reference_selection:
                    col2.metric(label=f'{x} Latest Price', value='${:,.0f}'.format(price_data[f'{x}'].tail(1).item()))
                    col3.metric(label=f'{x} Markup', value=str(int(markup_data[f'{x} Markup'].tail(1).item())) + '%')
                st.subheader('Listings')
                st.bar_chart(listing_data)
                with st.expander('About the Data'):
                    st.write("""All resell pricing and listing information is sourced from Chrono24. Data is gathered on a weekly basis on Friday. Prices are the median asking price for the selected
                    reference in new/unworn condition with box and papers. Values are inclusive of MSRP increases occurring in January of 2022. 
                    Not affiliated with Rolex S.A. or its subsidiaries.""")
                st.download_button(label="Download Data", data=self.download, file_name='Rolex_Data.csv', mime='text/csv')

        except URLError as e:
            st.error(f'This Demo Requires Internet Access: {e.reason}')


if __name__ == "__main__":
    RolexPrices().rolex_price_data()
