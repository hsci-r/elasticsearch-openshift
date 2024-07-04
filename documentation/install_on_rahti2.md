# Rahti2 install procedure

Current install work through 'Helm'. CSC documentation for this can be found at https://docs.csc.fi/cloud/tutorials/helm/ .

## Installation

The steps in nutshell:
1. Add or modify `values.yaml` -file in `elasticsearch/`. There is a template there that can be copied for this.
1. Login to Rahti with oc -client (https://docs.csc.fi/cloud/rahti2/usage/cli/).
   * Login command can be copy pasted from Rahti2 web interface. https://console-openshift-console.apps.2.rahti.csc.fi/ Top right menu: 'Copy login command'.
2. run the helm (https://helm.sh/docs/intro/install/) install command in this repo's root.
   * helm install [name-of-app-on-rahti] elasticsearch/

### Usefull Helm commands

* Delete previous install: `helm uninstall dariahfi-es-test`
* PVCsneed to be separately deleted with oc: `oc delete pvc/data-es-test-0`, etc ...

## Adding plugins to a Rahti (Kubernetes) install

Plugins can either be added by creating a custom image, or using init containers to install plugins. Both have their pros and cons, as laid out at https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-bundles-plugins.html

Here on how to add plugins with Helm chart:
https://discuss.elastic.co/t/official-elasticsearch-helm-chart-unable-to-install-plugins/275593

**The method of creating a custom image is the recommended one, apparently. This is fortunate, as I couldn't get the init container -method to work. -Ville**

The custom image is currently at `vvaara/elastic-custom:[es-version]`
