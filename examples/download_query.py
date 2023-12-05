from smart_open import open
from elasticsearch import Elasticsearch, helpers
import json


def get_query_from_file(f):
    with open(f, 'r') as reader:
        return json.loads(reader.read())


ELASTIC_PASSWORD = "my-elastic-password"
ELASTIC_USER = "my-elastic-user"
# Create the client instance
# test env client
client = Elasticsearch("https://ds-es.rahtiapp.fi:443",
                       basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD), request_timeout=60)

index_name = "my-elastic-index"
query_f = 'my-exported-query.json'

q_json = get_query_from_file(query_f)

try:
    search_res = client.search(index=index_name, body=q_json, request_timeout=120)
except Exception as error:
    print("Elasticsearch Client Error:", error)
