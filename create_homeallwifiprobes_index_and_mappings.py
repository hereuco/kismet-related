import requests
url = "http://elasticsearchserver:9200/homeallwifiprobes"
payload = '{ "mappings": { "properties": { "first_time": { "type": "date", "format": "epoch_second" },  "last_time": { "type": "date", "format": "epoch_second" }, "probe_map.probedssid_first_time": { "type": "date", "format": "epoch_second" }, "probe_map.probedssid_last_time": { "type": "date", "format": "epoch_second" } } } }'
headers = {'Content-Type': 'application/json'}
response = requests.request("PUT", url, data=payload, headers=headers)
print(response.text)