# Copyright 2019 Hereuco
# By Efrain Ortiz
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# User required actions:
# from myAssets import knownDevices requires that a file named myAssets.py be created with the list of home assets with names.
# This exporter will export entries to answer the question: What APs have my known devices associated with?

import sqlite3
import json
import os, fnmatch
from myAssets import knownDevices

def main():
    filesToImport = []
    listOfFiles = os.listdir('.')
    match = "*.kismet"
    for file in listOfFiles:
        fileInfo = os.stat(file)
        if (fnmatch.fnmatch(file, match)) and ( fileInfo.st_size > 0):
            filesToImport.append(file)
    if len(filesToImport) == 0:
        print("No .kismet files to process\n")
        exit()
    targetIndex = "homeassociatedclients"
    def loopIt(file):
        print(file)
        def dict_create(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        print('Beginning to access file ' + str(file) + '\n')
        connection = sqlite3.connect(str(file))
        connection.row_factory = dict_create
        cursor = connection.cursor()
        cursor.execute('select first_time, last_time, device from devices where type = "Wi-Fi AP"')
        results = cursor.fetchall()
        connection.close()
        jdata = []
        for each in results:
            eachDevice = json.loads(each['device'])
            if str(eachDevice['kismet.device.base.macaddr']).upper() in list(knownDevices):
                if len(eachDevice['dot11.device']['dot11.device.associated_client_map']) > 0:
                    for probe in eachDevice['dot11.device']['dot11.device.associated_client_map']:
                        entry= {'knownName': 'unknown'}
                        if str(eachDevice['kismet.device.base.macaddr']).upper() in list(knownDevices):
                            entry['knownName'] = str(knownDevices[eachDevice['kismet.device.base.macaddr']])
                        entry['kismet.device.base.name'] = ''
                        if eachDevice['kismet.device.base.name'] != '':
                            entry['kismet.device.base.name'] = eachDevice['kismet.device.base.name']
                        entry['manuf'] = eachDevice['kismet.device.base.manuf']
                        entry['kismet.device.base.macaddr'] = eachDevice['kismet.device.base.macaddr']
                        entry['first_time'] = each['first_time']
                        entry['last_time'] = each['last_time']
                        entry['client_map'] = []
                        if (str(probe) in knownDevices):
                             entry['client_map'].append({ "associatedClient": probe, "probeName": knownDevices[probe] })
                        else:
                            entry['client_map'].append( { "associatedClient" : str(probe), "probeName": "unknown" })
                        jdata.append(entry)
        if len(jdata) > 0:
            output = open(str(file) + '_' + targetIndex + '_map_to_bulk_upload.json','w')
            for rowItem in jdata:
                output.write('{ \"index\" : { \"_index\" : \"' + targetIndex + '\" } }\n')
                output.write(json.dumps(rowItem))
                output.write('\n')
            output.write('\n\n')
            output.close()
            print('Created file ' + str(file) + '_' + targetIndex + '_map_to_bulk_upload.json')
        else:
            print('No known devices in ' +  str(file) + '_' + targetIndex + '_map_to_bulk_upload.json')
    for item in filesToImport:
        loopIt(item)

if __name__ == "__main__":
    main()