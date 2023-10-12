# elasticsearch-openshift

Setup instructions and scripts for Elasticsearch and Kibana on CSC Rahti.

## YAML templates

These are imported into Rahti to setup the environments. Ideally no manual input needed (still working on that).

### Passwords

Currently requires entering passwords manually. In Rahti, for ELASTIC_PASSWORD and ELASTIC_BASIC_AUTH these need to be Base64 encoded. Eg. in Linux shell: `echo 'this-is-my-password' | base64` and for BASIC_AUTH `echo 'elastic:this-is-my-password' | base64`, or use a site like: https://www.base64encode.org/ .

### TODO

Elasticsearch and Kibana need to connect at setup. Kibana connects to ES with the user `kibana_system`. The user is automatically generated, but password for this user needs to be set. Currently the easiest solution seems to be with a POST request:

```
curl -X POST "https://ds-es.rahtiapp.fi:443/_security/user/kibana_system/_password?pretty" -H 'Content-Type: application/json' -d'
{
  "password" : "[password]"
}
' --user "elastic:[password]"
```

This should be automated somehow. Either by dding that request to the setup scripts, or in some other way. The username and password need to be specified in Kibana setup too (see `kibana-template.yaml`). Kibana should probably ideally have it's own secret in Rahti.
