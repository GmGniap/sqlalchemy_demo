
import requests
import pandas as pd
import numpy as np
import os
import logging
from sqlalchemy import create_engine
import platform
from dotenv import load_dotenv

if platform.system() == "Darwin":
    load_dotenv()
else:
    print(f"Current Platform : {platform.system()}")
    
# Configure the logging module
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
    filename="./week9_demo/mmdt_etl.log"
)

def extract_json_from_url(url:str):
    try:
        return requests.get(url).json()
    except Exception as e:
        raise ConnectionError(f"Can't extract data : {e}")

def get_covid_data() -> pd.DataFrame:
    covid_url = "https://raw.githubusercontent.com/owid/covid-19-data/refs/heads/master/public/data/latest/owid-covid-latest.json"
    covid_json = extract_json_from_url(covid_url)
    df_lst = []
    for country_short_code in covid_json.keys():
        single_country_df = pd.json_normalize(covid_json[country_short_code])
        single_country_df['iso_country_code'] = country_short_code
        # single_country_df.dropna(how="all", axis=1, inplace=True) ## performance is being slow
        df_lst.append(single_country_df)
        
    all_countries_df = pd.concat(df_lst, ignore_index=True)
    # drop all blank columns
    all_countries_df.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    all_countries_df.dropna(how='all', axis=1, inplace=True)
    print(all_countries_df.shape)
    
    ## Select only required columns (first 10)
    selected_cols = ["iso_country_code", "continent", "location", "last_updated_date", "total_cases", "new_cases", "total_deaths", "new_deaths", "total_cases_per_million", "total_deaths_per_million", "hosp_patients"]
    selected_df = all_countries_df[selected_cols]
    
    return selected_df

def get_cities_data() -> pd.DataFrame:
    required_data = []
    # cities_url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/refs/heads/master/json/countries%2Bcities.json"
    cities_url = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/9dd08cb8c333928e04a1fb4105fe206a9a82a16a/json/countries%2Bstates%2Bcities.json"
    cities_json = extract_json_from_url(cities_url)
    # print(type(cities_json)) ## Assume it'll be list
    for country in cities_json:
        data_dict = {
            'country_id' : country.get('id', np.nan),
            'country_name' : country.get('name', np.nan),
            'country_iso3' : country.get('iso3', np.nan),
            'country_capital': country.get('capital', np.nan),
            'country_subregion': country.get('subregion', np.nan),
            'country_region': country.get('region', np.nan),
        }
        logging.info(f"Received data for {data_dict['country_name']} - {data_dict['country_capital']}")
        required_data.append(data_dict)
    required_df = pd.DataFrame(required_data)
    return required_df
    
def get_city_weather(city_name:str) -> dict:
    api_key = os.getenv("WEATHER_KEY")
    weather_api = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        weather_json = extract_json_from_url(weather_api)
        required_dict = {
            "condition": weather_json['weather'][0].get('description', "Unknown weather"),
            "temperature_min": weather_json['main'].get('temp_min', np.nan),
            "temperature_max": weather_json['main'].get('temp_max', np.nan),
        }
        required_dict['city'] = city_name
        return required_dict
    except ConnectionError:
        logging.debug(f"Can't get data from this city : {city_name}")
        return None
    except Exception as e:
        logging.info(f"Other error - {e}")
        return None

def get_all_cities_weather(city_names_lst: list) -> pd.DataFrame:
    all_data = []
    for city_name in city_names_lst:
        if city_dict := get_city_weather(city_name):
            all_data.append(city_dict)
        else:
            logging.info(f"This city {city_name} is being none!")
    all_city_df = pd.DataFrame(all_data)
    return all_city_df

def transform_data():
    city_df = get_cities_data()
    ## Get weather for all capital cities
    capital_names = city_df['country_capital'].to_list()
    # print(f"Total capitals : {len(capital_names)}")
    weather_df = get_all_cities_weather(capital_names)
    # print(f"Weather Result : {weather_df.shape}")
    
    ## Join city_df with weather
    city_weather_df = city_df.merge(weather_df, how="inner", left_on='country_capital', right_on='city')
    # print(f"Joined result - {city_weather_df.shape}")
    
    ## Join covid_df with joined results
    covid_df = get_covid_data()
    covid_city_weather_df = covid_df.merge(city_weather_df, how="left", left_on="iso_country_code", right_on="country_iso3")
    return covid_city_weather_df
    

def load_data(df:pd.DataFrame):
    db_path = os.getenv("sqlite")
    db_url = "sqlite:///" + os.path.abspath(db_path)
    print(f"Db url - {db_url}")
    engine = create_engine(db_url)
    df.to_sql("covid_city_demo", engine, if_exists="replace", index=False)
    print("Successfully loaded into sqlite db!")

if __name__ == "__main__":
    df = transform_data()
    print(df.shape)
    load_data(df)