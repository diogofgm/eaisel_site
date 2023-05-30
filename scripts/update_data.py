import json
import yaml
import requests
import os

AIRTABLE_URL = "https://api.airtable.com/v0"

# BASE ID
EAISEL_BASE_ID = os.environ["EAISEL_AIRTABLE_BASE_ID"]

# MEMBERS DETAILS
MEMBERS_TABLE_ID = os.environ["EAISEL_AIRTABLE_TABLE_ID"]
MEMBERS_VIEW_ID = os.environ["EAISEL_AIRTABLE_VIEW_ID"]

# EVENTS DETAILS
EVENTS_TABLE_ID = os.environ["EAISEL_AIRTABLE_EVENTS_TABLE_ID"]
EVENTS_VIEW_ID = os.environ["EAISEL_AIRTABLE_EVENTS_VIEW_ID"]


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
        try:
            offset = data.get("offset")
        except:
            offset = None
        return records, offset
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred: ", e)
    except Exception as e:
        print("Other error occurred: ", e)


def get_data(node, base_id, table_id, view_id):
    a = []
    url = f"{AIRTABLE_URL}/{base_id}/{table_id}"
    params = {"view": view_id}
    headers = {"Authorization": "Bearer " + os.environ["EAISEL_AIRTABLE_API_KEY"]}

    offset = None
    while True:
        records, offset = make_request(url, headers, params=params)
        if offset is None:
            params = {"view": view_id}
        else:
            params = {"view": view_id, "offset": offset}

        for record in records:
            a.append(record.get("fields"))

        if offset is None:
            break

    yaml_string = yaml.dump(a, allow_unicode=True, sort_keys=False, Dumper=MyDumper)
    print(yaml_string)
    with open("_data/" + node + ".yml", "w") as f:
        f.write(yaml_string)


get_data("members", EAISEL_BASE_ID, MEMBERS_TABLE_ID, MEMBERS_VIEW_ID)
get_data("events", EAISEL_BASE_ID, EVENTS_TABLE_ID, EVENTS_VIEW_ID)
