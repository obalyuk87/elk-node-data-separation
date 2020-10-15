# based on 
# https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
from faker import Factory
from datetime import datetime
from elasticsearch import Elasticsearch
import json
from pprint import pprint

esDomainEndpoint = "http://localhost:9200"
es = Elasticsearch(esDomainEndpoint)
def create_names(fake):
    indexes = [
        # US Indexes
        "data-us-1", "data-us-2", "data-us-3",
        "data-us-4", "data-us-5", "data-us-6",
        # EU Indexes
        "data-eu-1", "data-eu-2",
        # Other Indexes
        "data-other-1"
    ]
    for index_name in indexes:
        print(f"Indexing data into {index_name}")
        for x in range(500):
            genUname = fake.slug()
            genName = fake.name()
            genJob = fake.job()
            genCountry = fake.country()
            genText = fake.text()
            genProfile = fake.profile()
            go = es.index(
                index=index_name,
                doc_type="_doc",
                id=genUname,
                body={
                    "name": genName,
                    "job": genJob,
                    "country": genCountry,
                    "notes": genText,
                    "profile_details": genProfile,
                    "timestamp": datetime.now()
                }
            )

if __name__ == '__main__':
    fake = Factory.create()
    create_names(fake)