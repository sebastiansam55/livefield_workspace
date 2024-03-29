#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth
import json
import argparse
from tabulate import tabulate
from pathlib import Path
import sys

class square9api():

    def __init__(self, config):
        self.square9api = config['square9api']
        self.auth = HTTPBasicAuth(config['user'], config['password'])
        self.dbid = config['dbid']
        self.token = self.get_token()

    def request(self, verb, endpoint, body=None, headers={'Content-type':'application/json'}):
        r = requests.request(verb, endpoint, headers=headers, data=body, auth=self.auth)
        if r.status_code==200:
            return r.json()
        else:
            if r.status_code==500:
                if 'name already exists' in r.text:
                    print(r.content)
                    raise Exception("Live Field with name already exists")
                else:
                    print(r.content)
                    raise Exception("HTTP 500 error")
            r.raise_for_status()

    def get_token(self):
        endpoint = f"{self.square9api}/api/licenses"
        token = self.request('GET', endpoint)
        return token['Token']

    def get_live_fields(self, raw=False):
        # get lists and filter
        endpoint = f"{self.square9api}/api/admin/databases/{self.dbid}/fields"
        data = self.request('GET', endpoint)
        livefields = []
        for field in data:
            if field['ExtendedConfig']['LiveField']:
                livefields.append(field)
        if raw:
            return data
        else:
            return livefields
    
    def script_escape(self, script:str):
        script = script.replace('\n', '\\n')
        return script
    
    def make_live_field(self, name, script):
        endpoint = f"{self.square9api}/api/admin/databases/{self.dbid}/fields"
        body = f"""{{
                        "Name": "{name}",
                        "Type": "CHARACTER",
                        "Format": "",
                        "Regex": "",
                        "Length": 50,
                        "Required": false,
                        "MultiValue": false,
                        "SystemField": "",
                        "List": {{
                            "Type": null,
                            "ListId": 0,
                            "Primary": 0,
                            "Secondary": 0,
                            "Mapping": []
                        }},
                        "ExtendedConfig": {{
                            "LiveField": {{
                            "Method": "GET",
                            "Url": "",
                            "Headers": {{}},
                            "JsonPath": "",
                            "Script": "{self.script_escape(script)}",
                            "Body": null
                            }}
                        }}
                    }}"""
        data = self.request('POST', endpoint, body=body)
        return data

    def update_live_field(self, field, script, local_field):
        endpoint = f"{self.square9api}/api/admin/databases/{self.dbid}/fields/{field['ID']}"
        #populate script from file
        field['ExtendedConfig']['LiveField']['Script'] = script.replace('\n', '')

        # populate other values from config.json
        field['ExtendedConfig']['LiveField']['Method'] = local_field['method']
        field['ExtendedConfig']['LiveField']['Url'] = local_field['url']
        field['ExtendedConfig']['LiveField']['Headers'] = local_field['headers']
        field['ExtendedConfig']['LiveField']['JsonPath'] = local_field['jsonPath']
        field['ExtendedConfig']['LiveField']['Body'] = local_field['body']

        json_data = json.dumps(field)
        data = self.request('PUT', endpoint, body=json_data)
        return data


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', help='Action to take [init|sync|ls|mkfield|rm|update]')

    parser.add_argument("--config", dest="config", default="config.json", help="Path to config file, defaults to ./config.json")

    parser_make_field = subparsers.add_parser('mkfield', help='Make Live Field')
    parser_make_field.add_argument("name", help='Live Field')
    parser_make_field.add_argument("script", help='File to use as Live Field script')

    parser_update_field = subparsers.add_parser('update')
    parser_update_field.add_argument("id", help='Live Field ID')
    parser_update_field.add_argument("name", help='Live Field Name')
    parser_update_field.add_argument("script", help='File to use as Live Field script')

    parser_init_workspace = subparsers.add_parser('init', help="Import from GlobalSearch instance")

    parser_sync_workspace = subparsers.add_parser('sync', help="Sync workspace to server")


    parser_list_field = subparsers.add_parser('ls', help="List Live Fields")
    parser_rm_field = subparsers.add_parser('rm', help="Delete Live Field (PERMANENT!)")
    

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    api = square9api(config)
    # print(api.token)
    
    if args.command == "ls":
        fields = api.get_live_fields()
        # print(len(fields))
        headers = ["ID", "Name"]
        grid_print = []
        for field in fields:
            grid_print.append([field["ID"], field["Name"]])
        print(tabulate(grid_print, headers=headers))

    elif args.command == "mkfield":
        print(f"Creating Live Field {args.name}. Script path: {args.script}")
        with open(args.script, 'r') as f:
            api.make_live_field(args.name, f.read())
    
    elif args.command == "update":
        print(f"Updating Live Field {args.name}. Script path: {args.script}")
        with open(args.script, 'r') as f:
            api.update_live_field(args.id, args.name, f.read())
    
    elif args.command == "init":
        print("Creating development directory for Live Fields")
        fields = api.get_live_fields()
        mapping = []

        output_folder = Path(config['directory'])
        if not output_folder.is_dir():
            output_folder.mkdir(parents=True, exist_ok=True)

        for field in fields:
            #TODO sanitize filenames
            live_field = field['ExtendedConfig']['LiveField']
            print(live_field)
            filename = f"{output_folder.name}/{field['Name']}.js"
            mapping.append({
                "id":field['ID'], "name":field['Name'], "filename":filename,
                "method":live_field['Method'], 
                "url":live_field['Url'],
                "headers":live_field['Headers'],
                "jsonPath":live_field['JsonPath'],
                "body":live_field['Body']
            })
            with open(filename, 'w') as f:
                f.write(field['ExtendedConfig']['LiveField']['Script'])
        
        with open(args.config, 'w+') as f:
            config['mapping'] = mapping
            json.dump(config, f, indent=4)

    elif args.command == "sync":
        print("Syncing filestate with server")
        raw_fields = api.get_live_fields(raw=True)
        lfields = {}
        for raw_field in raw_fields:
            lfields[raw_field['Name']] = raw_field
        
        for field in config['mapping']:
            with open(field['filename'], 'r') as f:
                print(f"Updating: {field}")
                # print(f"Field Retrieved from API: {lfields[field['name']]}")
                api.update_live_field(lfields[field['name']], f.read(), field)
                
        pass
