# pulsar-mastodon-sink
Mastodon data streaming


## Run the app

````
python3 stream.py

2023-01-17 17:28:17.197 INFO  [0x16ec2b000] HandlerBase:72 | [persistent://public/default/mastodon-partition-0, ] Getting connection from pool
2023-01-17 17:28:17.200 INFO  [0x16ec2b000] ProducerImpl:190 | [persistent://public/default/mastodon-partition-0, ] Created producer on broker [127.0.0.1:56776 -> 127.0.0.1:6650]
20230117222817.0

````

## JSON Schema

````
class mastodondata(Record):
    language = String()
    created_at = String()
    ts = Float()
    uuid = String()
    uri = String()
    url = String()
    favourites_count = Integer()
    replies_count = Integer()
    reblogs_count = Integer()
    content = String()
    username = String()
    accountname = String()
    displayname = String()
    note = String()
    followers_count = Integer()
    statuses_count = Integer()



````


## Schemafied Data

````
bin/pulsar-client consume "persistent://public/default/mastodon" -s "mreader2" -n 0

----- got message -----
key:[20230117222421_069e9afb-7b4a-481e-b5d3-40c03e421415], properties:[], content:{
 "language": "ja",
 "created_at": "2023-01-17 22:24:18+00:00",
 "ts": 20230117222421.0,
 "uuid": "20230117222421_069e9afb-7b4a-481e-b5d3-40c03e421415",
 "uri": "https://mstdn.jp/users/hikara/statuses/109706887715535436",
 "url": "https://mstdn.jp/@hikara/109706887715535436",
 "favourites_count": 0,
 "replies_count": 0,
 "reblogs_count": 0,
 "content": "<p>\u3093\u30fc\u307e\u3063\uff01</p>",
 "username": "hikara",
 "accountname": "hikara@mstdn.jp",
 "displayname": "\u3070\u3076\u30732023",
 "note": "<p>B70 \u541b\u306e\u6b66\u52c7\u4f1d\u3067\u3059</p>",
 "followers_count": 1640,
 "statuses_count": 51576
}

````

## Get Schema from Pulsar Schema Registry

````

bin/pulsar-admin schemas get persistent://public/default/mastodo
n
{
  "version": 5,
  "schemaInfo": {
    "name": "mastodon",
    "schema": {
      "type": "record",
      "name": "mastodondata",
      "fields": [
        {
          "name": "language",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "created_at",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "ts",
          "type": [
            "null",
            "float"
          ]
        },
        {
          "name": "uuid",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "uri",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "url",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "favourites_count",
          "type": [
            "null",
            "int"
          ]
        },
        {
          "name": "replies_count",
          "type": [
            "null",
            "int"
          ]
        },
        {
          "name": "reblogs_count",
          "type": [
            "null",
            "int"
          ]
        },
        {
          "name": "content",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "username",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "accountname",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "displayname",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "note",
          "type": [
            "null",
            "string"
          ]
        },
        {
          "name": "followers_count",
          "type": [
            "null",
            "int"
          ]
        },
        {
          "name": "statuses_count",
          "type": [
            "null",
            "int"
          ]
        }
      ]
    },
    "type": "JSON",
    "properties": {}
  }
}

````

## REFERENCE

* https://docs.joinmastodon.org/api/guidelines/#pagination
* https://aiven.io/blog/mastodon-kafka-js
* https://github.com/aiven/mastodon-to-kafka
* https://github.com/halcy/Mastodon.py
* https://docs.joinmastodon.org/client/intro/
* https://mastodonpy.readthedocs.io/en/1.8.0/
* https://mastodonpy.readthedocs.io/en/1.8.0/10_streaming.html
* https://martinheinz.dev/blog/86
* https://docs.joinmastodon.org/methods/streaming/#streams
