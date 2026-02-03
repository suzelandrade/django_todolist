# Docker Operations (Guia Prático)

Este guia tem como objetivo capacitar os formandos a **compreender Docker desde os conceitos fundamentais até à criação e distribuição de imagens**, com foco em uso prático no desenvolvimento moderno e em ambientes DevSecOps.

---

## Índice

1. [O que é Docker](#1️⃣-o-que-é-docker)
2. [Docker vs Máquina Virtual (VM)](#2️⃣-docker-vs-máquina-virtual-vm)
3. [Conceitos Essenciais do Docker](#3️⃣-conceitos-essenciais-do-docker)
4. [Instalação do Docker](#4️⃣-instalação-do-docker)
5. [Comandos Docker Básicos](#5️⃣-comandos-docker-básicos)
6. [Trabalhar com Containers (`docker run`)](#6️⃣-trabalhar-com-containers-docker-run)
7. [Volumes](#7️⃣-volumes)
8. [Redes Docker](#8️⃣-redes-docker)
9. [Docker Compose (uso prático)](#9️⃣-docker-compose-uso-prático)
10. [Dockerfile (definição da imagem)](#🔟-dockerfile-definição-da-imagem)
11. [Docker Build (criar a imagem)](#1️⃣1️⃣-docker-build-criar-a-imagem)
12. [Docker Registry (armazenar a imagem)](#1️⃣2️⃣-docker-registry-armazenar-a-imagem)
13. [Docker e Segurança](#1️⃣3️⃣-docker-e-segurança)
14. [Exercícios Práticos](#-exercícios-práticos)
15. [Documentação Oficial](#-documentação-oficial)

---

## 1️⃣ O que é Docker?

O **Docker** é uma plataforma que permite **empacotar e executar aplicações em containers**.

Um container inclui:

* a aplicação
* as dependências
* as bibliotecas necessárias
* configurações básicas

O objetivo principal do Docker é garantir que:

> *“A aplicação funciona da mesma forma em qualquer ambiente.”*

Docker **não é uma máquina virtual**.

Documentação: [https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)

---

## 2️⃣ Docker vs Máquina Virtual (VM)

| Docker              | Máquina Virtual (VM) |
| --------------------| ---------------- |
| Partilha kernel com o host  | Possui Kernel próprio |
| Executa aplicações isoladas | Executa um sistema operativo completo |
| Arranque Rápido           | Arranque Lento            |
| Muito mais Leve             |  Pesada - Consome mais recursos (CPU, RAM, disco) |
| Isola aplicações | Isola SO inteiro |

| |  | |
|---------------------| ---- | ----------------------|
| ![Docker](https://docker.com/app/uploads/2021/11/docker-containerized-appliction-blue-border_2.png) | VS |  ![VM](https://www.docker.com/app/uploads/2021/11/container-vm-whatcontainer_2.png) |

**Simples e Direta:**
> VM virtualiza o sistema operativo\
> Docker virtualiza a aplicação

---

## 3️⃣ Conceitos Essenciais do Docker

### Imagem

* É um **modelo (template)** da aplicação
* É imutável (read-only)
* Serve de base para criar containers

Exemplos:

```text
nginx
python:3.12
postgres:15
```

---

### Container

* É uma **imagem em execução**
* Pode ser iniciado, parado ou removido
* Não guarda dados permanentemente

Se o container for removido, os dados internos perdem-se.

---

### Volume

* Mecanismo de **persistência de dados**
* Os dados sobrevivem à remoção do container
* Usado para bases de dados, uploads, logs

---

### Rede

* Permite comunicação entre containers
* Containers na mesma rede comunicam-se pelo `nome` ou `containar_id`

Exemplo:

```text
web → db:5432
```

---

## 4️⃣ Instalação do Docker

### Windows / macOS

Docker Desktop:
[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### Linux / WSL2

[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

Verificar instalação:

```bash
docker --version
docker compose version
```

---

## 5️⃣ Comandos Docker Básicos

```bash
docker pull nginx
docker push bca/web-app:0.0.0
docker images
docker run
docker ps
docker ps -a
docker logs
docker stop container_id
docker rm container_id
```

---

## 6️⃣ Trabalhar com Containers (`docker run`)

Executar um container simples:

```bash
docker run nginx
```

Executar com porta exposta:

```bash
docker run -p 8080:80 nginx
```

Executar em background:

```bash
docker run -d nginx
```

Ver logs:

```bash
docker logs container_id
```

Aceder ao container:

```bash
docker exec -it container_id sh
```

---

## 7️⃣ Volumes

Criar volume:

```bash
docker volume create dados
```

Usar volume:

```bash
docker run -v dados:/data nginx
```

Volumes garantem persistência de dados.

---

## 8️⃣ Redes Docker

Listar redes:

```bash
docker network ls
```

Criar rede:

```bash
docker network create minha-rede
```

Usar rede:

```bash
docker run --network minha-rede nginx
```

Comunicação entre containers depende da rede Docker.

---

## 9️⃣ Docker Compose (uso prático)

O **Docker Compose** permite executar **vários containers em conjunto**, ideal para desenvolvimento local e ambiente de validação.

Exemplo:

```yaml
version: "3.8" ### (Optional)

services:
  web:
    image: nginx
    ports:
      - "8080:80"

  db:
    image: postgres:18
    environment:
      POSTGRES_PASSWORD=postgres
```

Executar:

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

Neste ponto estamos **a usar imagens existentes**, não a criar imagens novas.

[https://docs.docker.com/compose/](https://docs.docker.com/compose/)

---

## 🔟 Dockerfile (definição da imagem)

O **Dockerfile** é um ficheiro de texto que define **como uma imagem deve ser construída**.

Exemplo:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

O Dockerfile **descreve a imagem**, mas ainda não a cria.

---

## 1️⃣1️⃣ Docker Build (criar a imagem)

Após criar o Dockerfile, usamos `docker build` para **criar a imagem**.

```bash
docker build -t bca/web-app:0.0.0 .
```

Ver imagens criadas:

```bash
docker images
```

Sem este passo, não existe imagem própria.

---

## 1️⃣2️⃣ Docker Registry (armazenar a imagem)

Depois de criada, a imagem deve ser **armazenada num Docker Registry**.

Um **Docker Registry** é um **repositório de imagens Docker**, usado para:
* armazenar imagens
* versionar imagens
* partilhar imagens entre equipas e ambientes
* integrar com CI/CD
* *Um registry é para imagens o que o GitHub ou GitLab é para código.*

Sempre que executas:

```bash
docker pull nginx
```
estás a descarregar uma imagem de um **registry**.

**Doc:** [https://docs.docker.com/registry/](https://docs.docker.com/registry/)

### Exemplos de registries (público)

* Docker Hub (registry padrão do Docker): [https://hub.docker.com](https://hub.docker.com)
* GitHub Container Registry
* GitLab Container Registry

**Limitações:**

* limites de imagens privados
* limites de build (CI/CD)
* não recomendado para ambientes corporativos sensíveis


## Docker Registry em ambientes corporativos (Privado)

Em empresas e projetos institucionais, é comum usar **registries privados**, por razões de:

* segurança
* controlo de acesso
* soberania dos dados
* integração com CI/CD
* ambientes on-premise/controlado

### Open-source / On-Premise (recomendado para instituições)

* Harbor (muito utilizado)
* Docker Registry (`registry:2`)
* GitLab Container Registry (self-hosted)
* Quay (Red Hat)

Exemplo de registry local:

```bash
docker run -d -p 5000:5000 registry:2
```

Push:

```bash
docker tag bca/web-app:1.0 localhost:5000/bca/web-app:1.0
docker push localhost:5000/bca/web-app:1.0
```

---

## 1️⃣3️⃣ Docker e Segurança

Boas práticas:

* utilizar imagens oficiais
* evitar `latest`
* utilizar `.env` para segredos
* scan de imagens (Trivy, Snyk)
* utilizar registries privados
* autenticação e autorização
* versionar imagens (`:v1`, `:v2`, nunca só `latest`)
* restringir quem pode fazer `push`

Em ambientes DevSecOps, **a imagem também é código**.

[https://docs.docker.com/engine/security/](https://docs.docker.com/engine/security/)

---

## Exercícios Práticos

1. Executar nginx com `docker run`
2. Criar volume e persistir dados
3. Criar rede Docker
4. Subir serviços com Docker Compose
5. Criar Dockerfile
6. Construir imagem com `docker build`
7. Push para registry local ou publico

---

## Documentação Oficial

* Docker: [https://docs.docker.com](https://docs.docker.com)
* Dockerfile: [https://docs.docker.com/engine/reference/builder/](https://docs.docker.com/engine/reference/builder/)
* Docker Compose: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
* Docker Registry: [https://docs.docker.com/registry/](https://docs.docker.com/registry/)
* Harbor: [https://goharbor.io/docs/](https://goharbor.io/docs/)
* GitHub Container Registry: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
* GitLab Registry: https://docs.gitlab.com/ee/user/packages/container_registry/
---

## Nota Final

Este README serve como:

* guia de formação
* material de apoio
* referência prática pós-formação

Aproveite!