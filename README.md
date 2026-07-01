### WSO2

### TLS

- Por default exige configuração de TLS, para desabilitar no lab adicionei a flag no docker compose:

  ```YAML
      environment:
          - JAVA_OPTS=-Dorg.apache.axis2.transport.http.ssl.disableHostnameVerification=true
  ```

### Kubernetes

-Instale o helm e o kubectl, se ainda não estiverem instalados. Em seguida, execute o seguinte comando para instalar o WSO2 usando o Helm:

```shell
helm repo add wso2 https://helm.wso2.com && helm repo update
git clone https://github.com/wso2/kubernetes-apim.git
cd kubernetes-apim
git checkout tags/v3.2.0.2
```

## Antes de instalar altere os yamls

- em: `advanced/am-pattern-1/values.yaml` subistitua a anottations de ingress pelo que vai utilizar `kubernetes.io/ingress.class: "traefik"`
- em: `advanced/am-pattern-1/requirements.yaml` altere o repository no `nfs-server-provisioner` por `https://charts.helm.sh/stable` e a versão para `"1.8.0"`
- em: todos os ingress corrija o apiVersion: `apiVersion: networking.k8s.io/v1` e configuração de porta e path:
  ```yaml
      paths:
          - path: /
              pathType: Prefix
              backend:
              service:
                  name: {{ template "am-pattern-1.resource.prefix" . }}-am-service
                  port:
                  number: 9763
  ```
-

- Altere no value os hostnames para dominio.test

```shell
helm install --dependency-update wso2 $(pwd)/advanced/am-pattern-1 --namespace wso2 --create-namespace`
```

- Adicione o apontamento ao seu etc/hosts

```sh
127.0.0.1 am.wso2.test
127.0.0.1 gateway.am.wso2.test
127.0.0.1 analytics.am.wso2.test
```
