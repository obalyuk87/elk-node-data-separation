# Experiment Results Summary

## Created Index Templates

Script: `curl http://localhost:9200/_index_template/data*?pretty`

```json
{
  "index_templates" : [
    {
      "name" : "data-us",
      "index_template" : {
        "index_patterns" : [
          "data-us-*"
        ],
        "template" : {
          "settings" : {
            "index" : {
              "number_of_shards" : "1",
              "number_of_replicas" : "0",
              "routing" : {
                "allocation" : {
                  "include" : {
                    "geo_locaton" : "us"
                  }
                }
              }
            }
          }
        },
        "composed_of" : [ ],
        "priority" : 100,
        "version" : 1
      }
    },
    {
      "name" : "data-eu",
      "index_template" : {
        "index_patterns" : [
          "data-eu-*"
        ],
        "template" : {
          "settings" : {
            "index" : {
              "number_of_shards" : "1",
              "number_of_replicas" : "0",
              "routing" : {
                "allocation" : {
                  "include" : {
                    "geo_locaton" : "eu"
                  }
                }
              }
            }
          }
        },
        "composed_of" : [ ],
        "priority" : 100,
        "version" : 1
      }
    }
  ]
}
```

## Index Data

Script: `python scripts/generate-test-data.py`

```bash
Indexing data into data-us-1
Indexing data into data-us-2
Indexing data into data-us-3
Indexing data into data-us-4
Indexing data into data-us-5
Indexing data into data-us-6
Indexing data into data-eu-1
Indexing data into data-eu-2
Indexing data into data-other-1
```

## Preview Node Attributes

Script: `curl http://localhost:9200/_cat/nodeattrs | grep geo`

```bash
es01 172.20.0.4 172.20.0.4 geo_locaton       us
es02 172.20.0.2 172.20.0.2 geo_locaton       eu
es03 172.20.0.3 172.20.0.3 geo_locaton       other
```

* US - es01
* EU - es02

## Checking Shard Allocation

Script: `curl http://localhost:9200/_cat/shards/data*?v`
```bash
index        shard prirep state   docs    store ip         node
# NOTE: "eu" indices are located on es02 node
data-eu-1    0     p      STARTED 1994    3.9mb 172.20.0.2 es02
data-eu-2    0     p      STARTED  500  953.3kb 172.20.0.2 es02
# NOTE: "us" indices are located on es01 node
data-us-1    0     p      STARTED 1997    3.9mb 172.20.0.4 es01
data-us-2    0     p      STARTED 1998    3.9mb 172.20.0.4 es01
data-us-3    0     p      STARTED 1996    3.9mb 172.20.0.4 es01
data-us-4    0     p      STARTED  500    1.1mb 172.20.0.4 es01
data-us-5    0     p      STARTED  499    1.1mb 172.20.0.4 es01
data-us-6    0     p      STARTED  500    1.1mb 172.20.0.4 es01
# NOTE: "other" indicess
data-other-1 0     r      STARTED  500 1020.6kb 172.20.0.2 es02
data-other-1 0     p      STARTED  500  979.3kb 172.20.0.3 es03
```

* NOTE: `data-other-1` ended-up being routed to `es02` (eu) data node because `data-other-*` indexes do not have template specifying routing allocation.