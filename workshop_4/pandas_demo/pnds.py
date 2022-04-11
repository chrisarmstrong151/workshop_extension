# Based on the example at https://pandas.pydata.org/pandas-docs/version/0.15/10min.html#minutes-to-pandas


# Imports
from WasteCalculator import WasteCalculator

                


# Instantiate
wc = WasteCalculator()

# # Get the webpage information.
# wc.get_electric_rates()

# What is the minimum rate?
wc.get_minimum_rate()

# Calculate the waste.
wc.calculate_waste(
    show_data_frame = True
)