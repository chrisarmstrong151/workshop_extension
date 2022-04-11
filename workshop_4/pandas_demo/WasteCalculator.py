# Imports

# Tag parsing
from bs4 import BeautifulSoup

# DataFrames
import pandas as pd

# Web requests
import requests


# Relative imports

# Source: https://stackoverflow.com/a/4142197
from Regex import Regex



# Note: hours unused per day counts weekends.

class WasteCalculator():


    def calculate_waste(
        self,
        show_data_frame = False
    ):

        """Calculate the waste."""

        # Open the file containing light information.
        with open('lights_by_room.tsv', 'r') as f:

            # Read straight into pandas.
            # Source: https://pandas.pydata.org/docs/reference/api/pandas.read_table.html#pandas.read_table
            light_info = pd.read_table(
                filepath_or_buffer = f,
                sep = '\t'
            )

            # Derive a wattage column from the light model.
            # Source: https://www.geeksforgeeks.org/python-pandas-split-strings-into-two-list-columns-using-str-split/
            
            # The wattage should be converted to kilowatts.
            # Source: https://stackoverflow.com/a/28648923
            light_info['wattage (kw)'] = pd.to_numeric((light_info['model'].str.split(pat = '_', n = 1, expand = True)[1]))/1000

            # Add the mean per-kw-hour-price.
            light_info['price_per_kw_hour'] = self.minimum_rate

            # Calculate the waste per month and per year.
            # light_info['price_per_month'] = light_info['wattage (kw)']*light_info['price_per_kw_hour']*light_info['hours_unused_per_week']*light_info['quantity']*4
            light_info['price_per_month'] = light_info['quantity']*light_info['hours_unused_per_week']*light_info['wattage (kw)']*light_info['price_per_kw_hour']*4
            light_info['price_per_year'] = light_info['price_per_month']*12

            # Show the calculations?
            if show_data_frame is True:
                print('\nCalculations\n------------\n')
                print(light_info)

            # 10 meals per dollar.
            # Source: https://www.feedingamerica.org/ways-to-give/faq/about-our-claims

            # Nice formatting.
            # Source: https://stackoverflow.com/questions/5180365/python-add-comma-into-number-string/5180405#5180405
            print('\nWaste per year: ${:,.2f}'.format(sum(light_info['price_per_year'])) + '\n\nApproximately {:,.0f}'.format(int(sum(light_info['price_per_year']))*10) + ' meals\n')
    
    
    def get_electric_rates(
        self
    ):

        """Get the kw-hr rates."""

        # Make the request.
        # Source: https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a
        r = requests.get(
            url = 'https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a'
        ).text
        
        # Write the text out by default.
        with open('rate_info.txt', 'w') as f:
            f.write(r)

        return r


    def get_minimum_rate(
        self
    ):
    
        """Get the minimum kw-hr rate."""
        
        # Instantiante Regex.
        rgx = Regex()
        
        # Read the text in, stripping newlines.
        with open('rate_info.txt', 'r') as f:
            
            lines = ''.join([i.strip() for i in f.readlines()])


            # Solution 1 (REGEX)
            
            # # Skip rgx.regex_search() and use rgx.searcher()
            # # directly...
            
            # # Search for "Florida" and the table row.
            # test = rgx.searcher(
            #     return_match_objects = False,
            #     search_method = 'all_matches',
            #     search_regex = 'Florida(.*?)><\/tr>',
            #     search_text = lines
            # )

            # for i in test:
            #     print(i.split('           '))

            # and so on...
            

            # Solution 2 (tag parsing + regex)

            # Source: https://www.twilio.com/blog/web-scraping-and-parsing-html-in-python-with-beautiful-soup
            # Source: https://stackoverflow.com/a/20523151

            # Use BeautifulSoup to parse the page.
            soup = BeautifulSoup(lines, 'html.parser')

            # Go over each table row, looking for 'Florida'.
            for table_row in soup.find_all('tbody')[0].findAll('tr'):
                if table_row.text.find('Florida') != -1:
                    
                    # Once we've found 'Florida', extract the price we want.
                    # In this case, the January 2022 commercial and industrial prices.
                    commercial_price = rgx.searcher(
                        return_match_objects = False,
                        search_method = 'first_match',
                        search_regex = '\d+\.\d+',
                        search_text = table_row.find_all('td')[3].text
                    )

                    industrial_price = rgx.searcher(
                        return_match_objects = False,
                        search_method = 'first_match',
                        search_regex = '\d+\.\d+',
                        search_text = table_row.find_all('td')[5].text
                    )
                    
                    # Note type conversion because the regex returns
                    # string matches...

                    # Price is in cents, divide by 100 to get dollars.
                    self.minimum_rate = min(float(commercial_price[0]), float(industrial_price[0]))/100