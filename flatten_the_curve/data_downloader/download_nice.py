"""Download and parse NICE data to CSV"""

from pathlib import Path
import requests
import json
import csv

# JSONs to download.
# Files with single object (dict) and files with single array (list(dict)) are supported out of the box
NICE_URLS = ['https://www.stichting-nice.nl/covid-19/public/global', # aggregated stats
             'https://www.stichting-nice.nl/covid-19/public/new-intake', # new IC patients with proven COVID-19, per day
             'https://www.stichting-nice.nl/covid-19/public/intake-count', # current total IC patients with proven COVID-19, per day
             'https://www.stichting-nice.nl/covid-19/public/intake-cumulative', # cumulative IC patients with proven COVID-19, per day
             'https://www.stichting-nice.nl/covid-19/public/ic-count', # current total of ICUs with at least one proven COVID-19 patient, per day
             'https://www.stichting-nice.nl/covid-19/public/died-and-survivors-cumulative'] # cumulative IC patients with proven COVID-19 that died and surved, per day


def download_json(urls):
    """Download a list of JSONs, return dictionary with filename => data"""
    data = {}
    for url in urls:
        name = url.rsplit('/', 1)[-1]
        resp = requests.get(url)
        if name == 'died-and-survivors-cumulative':
            # parse died and survivors to their own files
            died = []
            survived = []
            for i,v in enumerate(resp.json()):
                for l in v:
                    if i == 0:
                        l['died'] = l.pop('value')
                        died.append(l)

                    else:
                        l['survived'] = l.pop('value')
                        survived.append(l)

            data['died-cumulative'] = died
            data['survived-cumulative'] = survived
        else:
            data[name] = resp.json()

    return data

# use this if you want to store the raw JSONs
def dump_json(data, dir):
    """Parse a dictionary of JSONs. Key = filename (without .json)"""
    Path(dir).mkdir(parents=True, exist_ok=True)

    for name,content in data.items():
        with open(dir+name+'.json', 'w') as out:
            json.dump(content, out)
    
    return True

def write_json_to_csv(data,dir):
    """Write a dictionary of filename => data (dict) to CSVs in dir"""
    for file,json in data.items():

        with open(dir+file+'.csv', 'w', newline='') as out_f:
            if isinstance(json, dict):
                # single object
                # get header
                header = list(json.keys())

                # put data in list so it will fit in the DictWriter
                lines = [json]
            else:
                # single array
                # get header
                l = json[0]
                header = []
                for k,v in l.items():
                    header.append(k)

                lines = json

            # write the header
            writer = csv.DictWriter(out_f,fieldnames=header)
            writer.writeheader()

            # write the data
            for l in lines:
                writer.writerow(l)

# download jsons
data = download_json(NICE_URLS)

# write jsons to csv
csv_dir = 'raw_data/nice/csv/'
Path(csv_dir).mkdir(parents=True, exist_ok=True)
write_json_to_csv(data, csv_dir)
