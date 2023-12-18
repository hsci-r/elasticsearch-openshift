## Indexing and storage

This has been succesfully done through the Python client as well.

### Expanding storage (PVC)

The current practice for increasing pod persistent volume claim (PVC) size is as follows:

1. Delete the existing Stateful Set, create a new one with a different parameter for PVC size. You can adjust this after importing the YAML at https://github.com/hsci-r/elasticsearch-openshift/tree/main 
2. Scale the stateful set down to 0 replicas, so that the pods are deleted. Two ways:
3. Edit the YAML in the Rahti Admin UI (https://rahti.csc.fi:8443/console/project/octavo2/browse/stateful-sets/  )
4. Use console, eg.: “oc scale --replicas=0 statefulset ds-es”
5. Delete one, and only one, PVC, either through Rahti UI or console: “oc delete pvc data-ds-es-dev-0”
6. Scale the stateful set back to the previous number of pods, wait for the deleted shards to be restored. This should create the missing PVC in the new size.
7. Repeat for each storage claim.

Without scaling the stateful set down first, the pod attached to the PVC will still exist, and the PVC will be stuck in “terminating”. 

### Indexing speed

Indexing a very large dataset takes a considerable amount of time. The Elastic documentation suggests adjusting batch size for the bulk indexer to optimize indexing time, but at least according to the quick tests we ran, this doesn't make a significant different. See [legentic_bulk_size_test2.csv](legentic_bulk_size_test2.csv) for details. Reducing the amount of fields that are run through various analyzers might have a greater effect.

There are other options laid out in [the Elastic documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html) that warrant further exploration. Note the following on the points listed there:
* *Disable swapping* - done by default by Kubernetes, no action needed.
* *Use auto-generated ids* - might not be advisable. The auto-generated ids for Elasticsesarch use time as a source, so if you wish to reindex the same document, autogeneration of ids result in the document replicating?
* *Disable replicas for initial loads* - this might be worth trying.

#### Multithread indexing

This does seem to have a significant effect. The test results for the legentic set were as follows, with 5 nodes and 10 shards in the index. Runtimes in seconds for indexing 20 iterations for single thread, and 3, 4 and 5 threads.

| Run#    | Single      | Multi-3     | Multi-4     | Multi-5     |
| ------- | ----------- | ----------- | ----------- | ----------- |
| 1       | 189         | 108         | 71          | 80          |
| 2       | 226         | 95          | 87          | 89          |
| 3       | 208         | 92          | 86          | 86          |

5 threads does not seem to be faster than 4, even with 5 nodes. Possibly Elasticsearch reserves a node for non-indexing requests?
