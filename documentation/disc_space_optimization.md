# Disk Space Optimization

There are multiple ways to reduce the space taken by Elastic indices. See:

https://coralogix.com/blog/elasticsearch-disk-and-data-storage-optimizations-with-benchmarks/

https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-disk-usage.html


## Source not stored

This is strongly not recommanded, but can be done. There are other ways to retrieve stored field values, but source is the default one. See https://sease.io/2021/02/field-retrieval-performance-in-elasticsearch.html for comparison of retrieval speeds for different methods.

**NOTE!** This turns out not to have any effect on storage space. See: https://discuss.elastic.co/t/removing-source-increases-size-of-index/283699/3 and from there: https://github.com/elastic/elasticsearch/issues/41628#issuecomment-488155381 .

Additionally, when tryoing to set the `index.soft_deletes.enabled` the API for 8.5.x responds: `elasticsearch.BadRequestError: BadRequestError(400, 'illegal_argument_exception', 'Creating indices with soft-deletes disabled is no longer supported. Please do not specify a value for setting [index.soft_deletes.enabled].')`.

In light of the above, the following is moot information, but kept here for possible future use:

If \_source is not indexed, the values have to be retrived through `docvalue_fields` and `stored_fields`. E.g.:

```bash
curl -X GET "https://ds-es-dev.rahtiapp.fi/legentic-no-source/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "_id": "c59da65e142b357432e534d04003f1a931552bf7490ee96b087a7652e004aeb"
    }
  },
  "docvalue_fields": [
    "thread-title.content",
    "url"
  ]
}
'
```

And in one url: https://ds-es-dev.rahtiapp.fi/legentic-no-source/_search?pretty=true&q=*:*&docvalue_fields=url

## Using best_compression

How to change an existing index from standard to best compression:

https://discuss.elastic.co/t/elasticsearch-best-compression/320397

With the Python API:

```Python
client.indices.get_settings(index=index_name) # check current settings
client.indices.close(index=index_name) # index needs to be closed for codec setting to be changeable
client.indices.put_settings(index=index_name, settings={'codec': 'best_compression'})
client.indices.open(index=index_name)
client.indices.forcemerge(index=index_name)

```
