import json
import yaml
import requests
import os

AIRTABLE_URL = "https://api.airtable.com/v0/"
BASE_ID = os.environ['EAISEL_AIRTABLE_BASE_ID']
TABLE_ID = os.environ['EAISEL_AIRTABLE_TABLE_ID']
VIEW_ID = os.environ['EAISEL_AIRTABLE_VIEW_ID']

class MyDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

def make_request(url, headers, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records")
        offset = data.get("offset")
        return records, offset
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred: ", e)
    except Exception as e:
        print("Other error occurred: ", e)

a = []

url = f"{AIRTABLE_URL}/{BASE_ID}/{TABLE_ID}"
params = {"view": VIEW_ID}

headers = {
    'Authorization': 'Bearer ' + os.environ['EAISEL_AIRTABLE_API_KEY']
}

offset = None
while True:
    records, offset = make_request(url, headers, params=params)

    for member in records:
        a.append(member.pop("fields"))

    if offset is None:
        break

yaml_string = yaml.dump(a, allow_unicode=True, sort_keys=False, Dumper=MyDumper)
with open("_data/members.yml", "w") as f:
    f.write(yaml_string)
