import requests
import os
import pandas as pd

def download_league_season(base_path, filename, season, key):
    url = f"https://www.football-data.co.uk/mmz4281/{season}/{key}.csv"

    try:
        print(f"Downloading league: {key}, season: {season}, filename: {filename}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        with open(os.path.join(base_path, filename), 'wb') as csv_file:
            csv_file.write(response.content)

        print(f"Download successful for league: {key}, season: {season}, filename: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download league: {key}, season: {season}, filename: {filename}")
        print(f"Error: {e}")
        
def download_fixtures(base_path, filename):
    url = "https://www.football-data.co.uk/fixtures.csv"

    try:
        print(f"Downloading league next fixtures, filename: {filename}")
        response = requests.get(url)
        response.raise_for_status()

        with open(os.path.join(base_path, filename), 'wb') as csv_file:
            csv_file.write(response.content)

        print(f"Download successful for next fixtures, filename: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download league next fixtures, filename: {filename}")
        print(f"Error: {e}")
        
def load_data(base_path, all_seasons, usecols, keys, unique_key = True):
    data_frames = []
    # print(usecols)
    no_time = usecols.copy()
    no_time.remove('Time')
    
    with os.scandir(base_path) as entries:
        for entry in entries:
            if unique_key == True:
                if entry.is_file() and keys[0] == entry.name[:len(keys[0])] and entry.name.endswith(".csv"):
                        file_path = entry.path
                        season_value = entry.name.split('_')[1].split('.')[0] #
                        if season_value in all_seasons:
                            try:
                                df = pd.read_csv(file_path, usecols = usecols, encoding='ISO-8859-1')
                                df.insert(1, 'Season', season_value)  
                                data_frames.append(df.dropna(subset = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'])) #,'HTHG','HTAG'
                            except:
                                try:
                                    df = pd.read_csv(file_path, usecols = no_time, encoding='ISO-8859-1')
                                    df.insert(2, 'Time', '16:00')
                                    df.insert(1, 'Season', season_value)  
                                    data_frames.append(df.dropna(subset = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'])) #,'HTHG','HTAG'
                                except Exception as e:
                                    print(f"Error loading file {entry.name}: {e}")
            else:
                for key in keys:
                    if entry.is_file() and key in entry.name and entry.name.endswith(".csv"):
                        file_path = entry.path
                        season_value = entry.name.split('_')[1].split('.')[0] #
                        if season_value in all_seasons:
                            try:
                                df = pd.read_csv(file_path, usecols = usecols, encoding='ISO-8859-1')
                                df.insert(1, 'Season', season_value)  
                                data_frames.append(df.dropna(subset = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'])) #,'HTHG','HTAG'
                            except:
                                try:
                                    df = pd.read_csv(file_path, usecols = no_time, encoding='ISO-8859-1')
                                    df.insert(2, 'Time', '16:00')
                                    df.insert(1, 'Season', season_value)  
                                    data_frames.append(df.dropna(subset = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'])) #,'HTHG','HTAG'
                                except Exception as e:
                                    print(f"Error loading file {entry.name}: {e}")

    result_df = pd.concat(data_frames, ignore_index=True)

    return result_df

def load_fixtures(base_path, filename, usecols, current_season, leagues_keys, unique_key=True):
    try:
        df = pd.read_csv(os.path.join(base_path, "resources", filename), usecols = usecols, encoding='ISO-8859-1')
        if unique_key:
            df = df[df['Div'] == leagues_keys[0]]
            df.insert(1, 'Season', current_season)  
        else:
            df = df[df['Div'].isin(leagues_keys)]  # Keep games with 'Div' in leagues_keys
            df.insert(1, 'Season', current_season)  
        return df
    except Exception as e:
        print(f"Error loading file {filename}: {e}")

    