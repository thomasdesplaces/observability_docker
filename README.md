![alt Grafana_Labs](./assets/grafana_logo-web.svg)

![alt production](https://img.shields.io/badge/Production--Ready-No-green)
![alt docker](https://img.shields.io/badge/Deployment_tool-Docker--Compose-orange)

# Why

This repository contain an observability stack using Grafana Labs tools.  
These one is deploying with Docker Compose to test all the stack's tools.  

It is only a testing stack with no security, no production-ready configuration, ...  
This for testing purpose.  

# Architecture

Mimir, Loki and Tempo are deploy in Monolithic mode with 3 instances of each.  

![alt schema](./assets/Observability-Grafana_Stack.png)

# Prerequisite

1. Install [Docker](https://docs.docker.com/engine/install/) . 
2. Create Docker network :  
`docker network create observability-network`

# How deploy it

1. Clone this repository :  
`git clone https://github.com/tonyglandyl28/observability_docker.git`
2. Build & deploy :  
`docker-compose --profile grafana up --build`
3. Access to Grafana for visualization :  
*http://localhost:3000*

# How to send logs/metrics/traces

Deploy an application or database or other on the same docker network with these parameters :  
1. Traces :  
- Protocol : http
- Host : agent
- Port : 4318
- Path : /v1/traces
2. Logs :  
- Protocol : http
- Host : agent
- Port : 3500
- Path : /loki/api/v1/push
3. Expose Metrics with Prometheus (or based on Prometheus) on port : `8000` and modify the **targets** value in [agent.yaml](./agent/agent.yaml) (line 24).

# Sources

|                   Logo/Link                   |      Version    |               Usage                 |
|:---------------------------------------------:|-----------------|-------------------------------------|
| [<img src="./assets/agent.png" alt="Grafana Agent" width="200"/>](https://grafana.com/docs/agent/latest/) | v0.29.0 | Used to scrape data from applications (front, back, databases, ...) and send to each specific storage (like OpenTelemetry Collector). Based on https://github.com/grafana/agent/blob/main/example/docker-compose/docker-compose.yaml |
| [<img src="./assets/tempo.png" alt="Grafana Tempo" width="200"/>](https://grafana.com/docs/tempo/latest/) | v1.5.0 | Used to store Traces (like Jaeger or Zipkin). Based on https://github.com/grafana/tempo/tree/main/example/docker-compose/scalable-single-binary |
| [<img src="./assets/mimir.png" alt="Grafana Mimir" width="200"/>](https://grafana.com/docs/mimir/latest/) | v2.4.0 | Used to store Metrics (like Prometheus or Cortex). Based on https://github.com/grafana/mimir/blob/main/docs/sources/mimir/tutorials/play-with-grafana-mimir/docker-compose.yml |
| [<img src="./assets/loki.png" alt="Grafana Loki" width="200"/>](https://grafana.com/docs/loki/latest/) | v2.7.0 | Used to store Logs (like Elasticsearch). Based on https://github.com/grafana/loki/tree/main/examples/getting-started |
| [<img src="./assets/grafana.png" alt="Grafana" width="200"/>](https://grafana.com/docs/grafana/latest/) | v9.3.1 | Used to visualize data (like Kibana). Based on https://github.com/grafana/grafana |
| [<img src="./assets/minio.png" alt="Minio" width="200"/>](https://min.io) | Latest | Used to load balance traffic between each instance (on Cloud, use S3, Google Cloud Storage or similar). Based on https://github.com/minio/minio |
| [<img src="./assets/nginx.png" alt="NGinx" width="200"/>](https://www.nginx.com/) | Latest | Used to load balance traffic between each instance. Based on https://github.com/nginx/nginx |