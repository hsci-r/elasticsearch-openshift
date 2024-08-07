# Rahti2 install procedure

Current install work through 'Helm'. CSC documentation for this can be found at https://docs.csc.fi/cloud/tutorials/helm/ .

## Installation

The steps in nutshell:
1. Add or modify `values.yaml` -file in `elasticsearch/`. There is a template (`values.yaml-template`) to start from.
2. Login to Rahti with oc -client (Needs to be locally installed: https://docs.csc.fi/cloud/rahti2/usage/cli/).
   * Login command can be copy pasted from Rahti2 web interface. https://console-openshift-console.apps.2.rahti.csc.fi/ Top right menu: 'Copy login command'.
3. Run the helm (Helm needs to be lpocally installed: https://helm.sh/docs/intro/install/) install command in this repo's root:
   * `helm install [name-of-app-on-rahti] elasticsearch/`
     * eg. `helm install dariahfi-es-test elasticsearch/`
4. Same steps for Kibana, to be performed after the Elasticsearch pods are up and running.

### Useful Helm commands

* Delete previous install: `helm uninstall dariahfi-es-test`
* PVCs need to be separately deleted with oc: `oc delete pvc/data-es-test-0`, etc ...

## Notes on peculiarities and solutions

Plugins are currently installed via an initContainer.

The ES-Kibana connection is setup via an initContainer in the Kibana Helm chart. 

These are detailed below.

### Adding plugins to a Rahti (Kubernetes) install

Plugins can either be added by creating a custom image, or using init containers to install plugins. Both have their pros and cons, as laid out at https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-bundles-plugins.html

The method of creating a custom image is the recommended one, apparently. Newertheless, there are upside to using the intiContainer merhods: namely not needing to use and udate a custom image.

The arguments for packaging the plugins into the docker image are (from https://github.com/elastic/helm-charts/tree/main/elasticsearch):

```
There are a couple reasons we recommend this.

Tying the availability of Elasticsearch to the download service to install plugins is not a great idea or something that we recommend. Especially in Kubernetes where it is normal and expected for a container to be moved to another host at random times.
Mutating the state of a running Docker image (by installing plugins) goes against best practices of containers and immutable infrastructure.
```

The custom image is currently at `vvaara/elastic-custom:[es-version]`

#### Checking installed plugings

You can check the installed plugins by the API, eg. `https://dariahfi-es-test.2.rahtiapp.fi/_cat/plugins` .

#### Using initContainer

To install a plugin with an initContainer, the guidelines laid out at https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-init-containers-plugin-downloads.html need to be expanded with the solution found at https://discuss.elastic.co/t/official-elasticsearch-helm-chart-unable-to-install-plugins/275593 .

The initContainer, when not using the ready made elasticcloud on Kubernes -service offered by Elastic, needs to be set up to share a mounted volume with the main container. E.g. (from the statefulset.yaml):

```
      initContainers:
      # init container that installs Elastic plugins
      - name: init-install-plugins
        command:
        - sh
        - -c
        - |
          bin/elasticsearch-plugin remove --purge mapper-annotated-text
          bin/elasticsearch-plugin install --batch mapper-annotated-text
        image: docker.elastic.co/elasticsearch/elasticsearch:{{ .Values.esDockerImageVersion }}
        volumeMounts:
        - mountPath: /usr/share/elasticsearch/data
          name: data
        - mountPath: /usr/share/elasticsearch/plugins
          name: plugins
        - mountPath: /usr/share/elasticsearch/config/secret
          name: secrets
          readOnly: true
```
... and same under container:
```
      containers:
      # [...] some lines cut out for clarity
        volumeMounts:
        - mountPath: /usr/share/elasticsearch/data
          name: data
        - mountPath: /usr/share/elasticsearch/plugins
          name: plugins
        - mountPath: /usr/share/elasticsearch/config/secret
          name: secrets
          readOnly: true
```
... and under their shared volumes the plugins path needs to be created (empty?).
```
        volumeMounts:
        - mountPath: /usr/share/elasticsearch/data
          name: data
        - mountPath: /usr/share/elasticsearch/plugins
          name: plugins
        - mountPath: /usr/share/elasticsearch/config/secret
          name: secrets
          readOnly: true
```

### Kibana connection

Setting the Kibana to start up and link with Elasticsearch without user input was somewhat challenging. Kibana links with Elastic throught an internal user called kibana_system, and by default this gets a random password or single-use token generated for it. I couldn't find a way to pass this automatically from Elastic to Kibana, but it was possible to set the password manually throught the Elastic API. This is now handled in the Kibana initContainer, see `kibana/statefulset.yaml`:

```
      initContainers:
      # init container that sets kibana_system password
      - name: init-set-password
        image: curlimages/curl:latest
        command:
          - curl
          - -X
          - POST
          - -H
          - 'Content-Type: application/json'
          - -u
          - '{{ .Values.elasticBasicAuth }}'
          - -d
          - '{{ `{ "password" : "`}}{{ .Values.kibanaSystemPassword }}{{ `" }` }}'
          - 'https://{{ .Values.esAppName }}.2.rahtiapp.fi/_security/user/kibana_system/_password'

```
