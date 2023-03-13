<p align="center">
    <img src="./assets/observability.png" alt="Observability" width="500"/>
</p>

![alt version](https://img.shields.io/badge/Version-0.0.2-violet)
![alt production](https://img.shields.io/badge/Production--Ready-No-green)
![alt docker](https://img.shields.io/badge/Deployment_tool-Docker--Compose-orange)
![alt ARM](https://img.shields.io/badge/Platform-ARM--M1-red)

# Why

This repository contain an observability stack using [<img src="./assets/grafana_logo-web.svg" alt="Observability" width="200"/>](https://grafana.com/oss/) tools.
These one is deploying with Docker Compose to test all the stack's tools.

It is only a testing stack with no security, no production-ready configuration, ...
This for testing purpose.

# Architecture

The observability stack is composed by Mimir, Loki and Tempo which are deployed in Monolithic mode with 3 instances of each.
The application stack is composed by a FastAPI application with some routes and PostgreSQL database with 1 table.
Logs are written in a log file, scrape by [Grafana Promtail](https://grafana.com/docs/loki/latest/clients/promtail/) and send to Grafana Agent.
Metrics are exposed via [Prometheus Client](https://github.com/prometheus/client_python) and scraped by Grafana Agent.
Traces are sent via [Opentelemetry SDK](https://github.com/open-telemetry/opentelemetry-python) to Grafana Agent.
Unit tests are performed by [k6.io](https://k6.io).

![alt schema](./assets/Observability-Grafana_Stack.png)

# Prerequisite

This repository is run on Mac M1 (ARM architecture).
If you want to use another architecture, be sure to modify the Dockerfiles which import arm binary (ex. promtail on the app Dockerfile).

1. Install [Docker](https://docs.docker.com/engine/install/).
2. Create Docker network :
`docker network create observability-network`

# How deploy it

1. Clone this repository :
`git clone https://github.com/tonyglandyl28/observability_docker.git`

2. Build & deploy observability stack :
`docker-compose --profile grafana up --build`

3. Access to Grafana for visualization :
*http://localhost:3000*

4. Build & deploy application stack :
`docker-compose --profile application up --build`

# How to send logs/metrics/traces

Deploy an application or database or other on the same docker network with these parameters :
1. **Traces :**
- Protocol : *http*
- Host : *nginx*
- Port : *3600*
- Path : */v1/traces*
2. **Logs :**
- Protocol : *http*
- Host : *nginx*
- Port : *3500*
- Path : */loki/api/v1/push*
3. **Metrics :**
- Expose with Prometheus (or based on Prometheus) on example port : `8000` and modify the **targets** value in [agent.yaml](./agent/agent.yaml) (line 24).

# Ports configuration

## Observability stack

1. Get Logs :
Promtail --> Nginx : 3500 --> Agent : 3501 --> Nginx : 3502 --> Loki : 3503

2. Get Traces :
oTel SDK --> Nginx : 3600 --> Agent : 3601 --> Nginx : 3602 --> Tempo : 3603

3. Get Metrics :
Prometheus Exporter : 5050 (on path _/metrics_) <-- Agent --> Nginx : 3702 --> Mimir : 3703

4. Consult Logs on Grafana :
Grafana --> Nginx : 4502 --> Loki : 3503

5. Consult Traces on Grafana :
Grafana --> Nginx : 4602 --> Tempo : 4603

6. Consult Metrics on Grafana :
Grafana --> Nginx : 4702 --> Mimir : 3703

## Application stack

1. Front port : 5055

2. Backend/API port : 5050

3. Database port : 5432

# Sources

## Observability stack

|                   Logo/Link                   |      Version    |               Usage                 |
|:---------------------------------------------:|-----------------|-------------------------------------|
| [<img src="./assets/agent.png" alt="Grafana Agent" width="200"/>](https://grafana.com/docs/agent/latest/) | main-6f9d397 | Used to scrape data from applications (front, back, databases, ...) and send to each specific storage (like OpenTelemetry Collector). Based on https://github.com/grafana/agent/blob/main/example/docker-compose/docker-compose.yaml |
| [<img src="./assets/tempo.png" alt="Grafana Tempo" width="200"/>](https://grafana.com/docs/tempo/latest/) | v1.5.0 | Used to store Traces (like Jaeger or Zipkin). Based on https://github.com/grafana/tempo/tree/main/example/docker-compose/scalable-single-binary |
| [<img src="./assets/mimir.png" alt="Grafana Mimir" width="200"/>](https://grafana.com/docs/mimir/latest/) | v2.4.0 | Used to store Metrics (like Prometheus or Cortex). Based on https://github.com/grafana/mimir/blob/main/docs/sources/mimir/tutorials/play-with-grafana-mimir/docker-compose.yml |
| [<img src="./assets/loki.png" alt="Grafana Loki" width="200"/>](https://grafana.com/docs/loki/latest/) | v2.7.0 | Used to store Logs (like Elasticsearch). Based on https://github.com/grafana/loki/tree/main/examples/getting-started |
| [<img src="./assets/grafana.png" alt="Grafana" width="200"/>](https://grafana.com/docs/grafana/latest/) | v9.3.1 | Used to visualize data (like Kibana). Based on https://github.com/grafana/grafana |
| [<img src="./assets/minio.png" alt="Minio" width="200"/>](https://min.io) | Latest | Used to load balance traffic between each instance (on Cloud, use S3, Google Cloud Storage or similar). Based on https://github.com/minio/minio |
| [<img src="./assets/nginx.png" alt="NGinx" width="200"/>](https://www.nginx.com/) | Latest | Used to load balance traffic between each instance. Based on https://github.com/nginx/nginx |

## Application stack
Thanks to [@Blueswen](https://github.com/blueswen) for the FastAPI observability configuration.

|                   Logo/Link                   |      Version    |               Usage                 |
|:---------------------------------------------:|-----------------|-------------------------------------|
| [<img src="./assets/promtail.png" alt="Promtail" width="200">](https://grafana.com/docs/loki/latest/clients/promtail/) | Latest | Used to scrape application logs from file. |
| [<img src="./assets/fastapi.png" alt="FastAPI" width="200">](https://fastapi.tiangolo.com) | 0.88.0 | Used to expose API. Based on  https://github.com/Blueswen/fastapi-observability |
| [<img src="./assets/postgresql.png" alt="PostgreSQL" width="200">](https://www.postgresql.org) | 15-Bullseye | Used to store application data. |
| [<img src="./assets/prometheus.png" width="200">](https://github.com/prometheus-community/postgres_exporter) | Latest | Used to export Postgres metrics. Based on https://hub.docker.com/r/wrouesnel/postgres_exporter |
| [<img src="./assets/k6.png" alt="k6.io" width="200">](https://www.k6.io) | Latest | Used to performed unit tests. |
| [<img src="./assets/otel.png" alt="OpenTelemetry" width="200">](https://github.com/open-telemetry/opentelemetry-python) | 1.15.0 | Used to generate traces. |
