# Medical API

API FastAPI usada pelo WSO2, com HTTPS no backend via certificado TLS montado a partir de um `Secret`.

## Build da imagem

Use a mesma tag referenciada no manifesto do Kubernetes:

```bash
docker build -t adenilsonkon/api-python-medical:openapi .
```

Se quiser publicar com a tag `latest` também:

```bash
docker tag adenilsonkon/api-python-medical:openapi adenilsonkon/api-python-medical:latest
```

## Criar o Secret TLS

O Secret precisa conter os arquivos padrão `tls.crt` e `tls.key`.

Se você já tem os arquivos do Let’s Encrypt, normalmente use `fullchain.pem` e `privkey.pem`:

```bash
kubectl create secret tls medical-api-tls \
  --cert=$(pwd)/fullchain.pem \
  --key=$(pwd)/privkey.pem \
  -n api \
  --dry-run=client -o yaml | kubectl apply -f -
```

Se o namespace ainda não existir:

```bash
kubectl create namespace api --dry-run=client -o yaml | kubectl apply -f -
```

## Push da imagem

```bash
docker push adenilsonkon/api-python-medical:openapi
```

Se você também gerar a tag `latest`:

```bash
docker push adenilsonkon/api-python-medical:latest
```

## Aplicar no Kubernetes

```bash
kubectl apply -f kubernetes/api-manifest.yaml
```

Depois de alterar `Dockerfile`, `start.sh` ou o manifesto, faça o rebuild e o push da imagem antes de aplicar no cluster:

```bash
docker build -t adenilsonkon/api-python-medical:openapi .
docker push adenilsonkon/api-python-medical:openapi
kubectl apply -f kubernetes/api-manifest.yaml
kubectl rollout restart deployment/medical-api -n api
```

## Observações

- O backend sobe em `https://` na porta `8443`.
- O `Secret` TLS precisa estar no namespace `api`.
- O hostname do certificado deve cobrir `medical-api.konzelmann.com.br` ou o subdomínio que você estiver usando.
- Se aparecer `502 Bad Gateway`, normalmente o cluster ainda está rodando a imagem antiga ou o pod não conseguiu subir com o Secret montado.
