# ELK Data Separation via Templates & Node Attributes

## Objective

Proof of concept for ONE Elasticsearch cluster with geolocation separated data using elasticsearch node attributes.

In this example we will separate US and EU data for the use-case of data privacy laws. Data will reside in ONE ES cluster, on nodes in different geographies.

## Prerequisites
1. Docker & docker-compose
2. Python3 with pip

## Setup

1. Spin-up environmnet using docker-compose

    ```bash
    # build & run in background
    docker-compose up --build --detach
    ```

2. Ensure environment is up

    ```bash
    curl http://localhost:9200/_cat/health
    ```

3. Apply index templates

4. Index some data manually or by running script

    ```bash
    # install dependencies
    python -m pip install -r scripts/requirements.txt
    # execute script
    python scripts/generate-test-data.py
    ```

5. Validate results

## Index Templates

```json
PUT _index_template/data-us
{
  "version": 1,
  "index_patterns": ["data-us-*"],
  "priority": 100,
  "template": {
    "settings": {
      "index.routing.allocation.include.geo_locaton": "us",
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}

PUT _index_template/data-eu
{
  "version": 1,
  "index_patterns": ["data-eu-*"],
  "priority": 100,
  "template": {
    "settings": {
      "index.routing.allocation.include.geo_locaton": "eu",
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }
}
```

## Useful Links

* https://www.elastic.co/guide/en/elasticsearch/reference/7.x/shard-allocation-filtering.html
* https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-allocation-filtering.html

## Encountered Issues

* https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html

```
ERROR: [1] bootstrap checks failed

[1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

ERROR: Elasticsearch did not exit normally - check the logs at /usr/share/elasticsearch/logs/es-docker-cluster.log
```
