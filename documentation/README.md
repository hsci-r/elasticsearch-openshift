# Elasticsearch in Openshift

Collection of instructions and best practices for using Elasticsearch in data exploration and subsetting. Originally in the context of the DARIAH-FI project.

## Intalling on CSC Rahti2

See [**install_on_rahti2.md**](install_on_rahti2.md) for instructions and observations on installing ES and Kibana on Rahti2. 

## Subsetting and retrieving documents

### Elasticsearch API

The Python client for the Elasticsearch API works well, and seems able to handle the API calls with Python structures. Follow the library documentation at https://elasticsearch-py.readthedocs.io/en/v8.5.2/ .

### Kibana 

See the [instructions here](exported_query.md) for steps on how to pick a subset of the data for download in Kibana.

## Technical notes

See the following for details and observations done dutring the deployment process.

* [**Indexing and storage**](indexing.md)
* [**Disk Space Optimization**](disc_space_optimization.md)
