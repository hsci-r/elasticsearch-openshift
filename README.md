# elasticsearch-openshift

Setup instructions and scripts for Elasticsearch and Kibana on CSC Rahti2 Openshift environment.

Instructions for use and best practices at found in the [/documentation](documentation) -folder in this repository.

We currently employ the "Helm chart" -method recommended by CSC.

## Helm charts

There are two Helm charts in two directories: `elesticsearch` and `kibana`. The details for deploying those on Rahti2 are found in [/documentation/install_on_rahti2.md](documentation).

Once these have been setup, the process should be hands free.

### Passwords

Passwords are set in the Helm charts, refer to the documentation above.
