import requests
import pandas as pd

owid_raw_url = "https://raw.githubusercontent.com/owid/covid-19-data/refs/heads/master/public/data/latest/owid-covid-latest.json"

raw_data = requests.get(owid_raw_url).json()

all_countries = pd.DataFrame()

for country_short_code in raw_data.keys():
    single_country_df = pd.json_normalize(raw_data[country_short_code])
    single_country_df['iso_country_code'] = country_short_code
    ## Combine/Concat
    all_countries = pd.concat([all_countries, single_country_df], ignore_index=True)

print(all_countries.shape)
print(all_countries.columns)
print("--x--")
print(all_countries.head())

# all_countries.to_csv("all_countries_covid.csv")
    