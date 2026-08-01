### WSO2

### TLS

- Por default exige configuração de TLS, para desabilitar no lab adicionei a flag no docker compose:

  ```YAML
      environment:
          - JAVA_OPTS=-Dorg.apache.axis2.transport.http.ssl.disableHostnameVerification=true
  ```

### Kubernetes

- k3d

```
k3d cluster create wso2 -a 1 -p "80:30000" -p "443:30001"
```

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

- Adicione o apontamento ao seu etc/hosts `usei dominio real, para poder usar o tls lets encrypt e não precisar lidar agora com a complexidade de certificados self-signed`

```sh
127.0.0.1 am.konzelmann.com.br
127.0.0.1 gateway.konzelmann.com.br
127.0.0.1 analytics.konzelmann.com.br
192.168.200.107 medical-api.konzelmann.com.br
```

- DNS no coredns
- Rorando local precisa adicionar o apontamento para backend no /hosts no configmap do coredns:

```yaml
NodeHosts: |
  172.19.0.1 host.k3d.internal
  172.19.0.2 k3d-wso2-server-0
  172.19.0.4 k3d-wso2-serverlb
  172.19.0.3 k3d-wso2-agent-0
  192.168.200.107 medical-api.konzelmann.com.br
```

### Configurar log4j2.properties

> OBS: Ainda é algo que precisa ser validado.

- kubectl:
  ```sh
  kubectl create configmap wso-config-log4j2 --from-file=$(pwd)/conf/wso2/log4j2-wso2-debug.properties -n wso2
  ```
- adicionar volume no deployment do am

```yaml
volumeMounts:
  - name: wso2am-log4j2
    mountPath: /home/wso2carbon/wso2am-3.2.0/repository/conf/log4j2.properties
    subPath: log4j2.properties
    readOnly: true
```

## Erros Enfrentados:

### Chamada http na porta https

```log
[2026-08-01 12:56:29,728]  WARN - SourceHandler I/O error: Unrecognized SSL message, plaintext connection?
```

- Ao chamar a api via endpoint gateway, recebia `502 - Bad Gateway` e o erro acima no pod do AM, isso ocorre porque o ingress do gateway envia uma chamada http na porta https (8243) do AM, alterado o ingress do gateway para enviar na porta http (8280)
