# Running exported queries

To easily get a query from Kibana to Elasticsearch, follow these steps:

1. In the **Analytics > Discover** -section of the Kibana UI, setup a relevant subset of oyur dataset. You can start from a **Dashboard** -view of the dataset and use the context menu option **Explore data in Discover**, or create a subset filter in the Discover -view.
2. In Discover, choose the **Inspect** -option from the top bar, choose the **Request** -view, and **Copy to clipboard** -button. This copies the displayed json request to oyur clipboard.
3. From here you can go to your Elasticsearch wrapper of choice, or use the copied query to download the relevant documents. See `examples/download_query.py` for a basic implementation with the Python wrapper.

## Datasets:

### Legentic dataset

This is a large social media dataset, access details below.

**url:** https://nlf-es-kibana.rahtiapp.fi/s/legentic/app/home#/
**usr:** legentic_viewer
**pwd:** leg-view

The same credentials for the Elasticsearch API.

### NLF periodicals

Dataset of periodical publications from the National Library of Finland digital collections.

**url:** https://nlf-es-kibana.rahtiapp.fi/s/nlf-periodicals/app/home#/
**usr:** nlf-periodicals-viewer
**pwd:** nlf-per-view
