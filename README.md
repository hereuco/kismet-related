# kismet-related
Some scripts used to extract KIsmet SQLite data for use in other tools.

These three scripts:
* elastic_home_only_access_points_to_bulk_upload_format.py
* elastic_home_only_all_devices_probing_my_network.py
* elastic_home_only_associated_clients_to_AP.py
* elastic_home_only_clients_probing_to_bulk_upload.py
* myAssets.py

Used to extract data from Kismet SQLite database and convert to format useful for elasticsearch bulk upload.


# Upload one file to Elasticsearch

curl -s -H "Content-Type: application/json" -XPOST http://elasticsearchserver:9200/_bulk --data-binary @{FILENAME}

where {FILENAME} is your Kismet-DATETIME*.json file
If {FILENAME} is Kismet-20190401-00-00-01.kismet_homeaccesspoints_list_to_bulk_upload.json then

curl -s -H "Content-Type: application/json" -XPOST http://elasticsearch:9200/_bulk --data-binary @Kismet-20190401-00-00-01.kismet_homeaccesspoints_list_to_bulk_upload.json

# Creating Elasticsearch index and mappings
To take advantage of the time fields in kismet logs for use in Elasticsearch and Kibana, the Elasticsearch indexs must have the correct mappings for the corresponding time fields. These basic python scripts should help in understanding how to prepopulate Elasticsearch.

* create_homeaccesspoints_index_and_mappings.py
* create_homeallwifiprobes_index_and_mappings.py
* create_homeassociatedclients_index_and_mappings.py
* create_homeprobes_index_and_mappings.py
