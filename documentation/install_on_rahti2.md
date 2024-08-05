# Rahti2 install procedure

Current install work through 'Helm'. CSC documentation for this can be found at https://docs.csc.fi/cloud/tutorials/helm/ .

## Installation

The steps in nutshell:
1. Add or modify `values.yaml` -file in `elasticsearch/`. There is a template there that can be copied for this.
1. Login to Rahti with oc -client (https://docs.csc.fi/cloud/rahti2/usage/cli/).
   * Login command can be copy pasted from Rahti2 web interface. https://console-openshift-console.apps.2.rahti.csc.fi/ Top right menu: 'Copy login command'.
2. run the helm (https://helm.sh/docs/intro/install/) install command in this repo's root.
   * helm install [name-of-app-on-rahti] elasticsearch/
     * eg. `helm install dariahfi-es-test elasticsearch/`

### Useful Helm commands

* Delete previous install: `helm uninstall dariahfi-es-test`
* PVCsneed to be separately deleted with oc: `oc delete pvc/data-es-test-0`, etc ...

## Adding plugins to a Rahti (Kubernetes) install

Plugins can either be added by creating a custom image, or using init containers to install plugins. Both have their pros and cons, as laid out at https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-bundles-plugins.html

The method of creating a custom image is the recommended one, apparently. Newertheless, there are upside to using the intiContainer merhods: namely not needing to use and udate a custom image.

The custom image is currently at `vvaara/elastic-custom:[es-version]`

### Using initContainer

To install a plugin with an initContainer, the guidelines laid out at https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-init-containers-plugin-downloads.html need to be expanded with the solution found at https://discuss.elastic.co/t/official-elasticsearch-helm-chart-unable-to-install-plugins/275593 .

The initContainer, when not using the ready made elasticcloud on Kubernes -servive offered by Elastic, needs to be set up to share a mounted volume with the main container. E.g. (from the statefulset.yaml):

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


## Kibana connection

This is troublesome. Apparently oyu should be able to specify a password for the kibana_system user, but for some reason that does not work. https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#next-getting-started-tls-docker

Maybe the password could be set as part of some init script:

https://www.elastic.co/guide/en/elasticsearch/reference/current/change-passwords-native-users.html

