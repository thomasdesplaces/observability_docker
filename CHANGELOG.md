0.0.4 - 2023-03-16
===================

### Features
- Add [Alert Manager](./grafana/provisioning/alerting/) #2 (@thomasdesplaces)

### Updating
- Update Change Grafana Agent [Log Level](./agent/agent.yaml) to _error_  (@thomasdesplaces)
- Update Grafana [folders](./grafana/) and adapt [Docker Compose](./docker-compose.yaml) (@thomasdesplaces)


0.0.3 - 2023-03-13
===================

### Features
- Add [Pre-Commit](./.pre-commit-config.yaml) and [PyLint](.pylinrc) #7 (@thomasdesplaces)
- Add scraping metrics from Loki, Tempo, Mimir and Postgres in Agent [Conf](./agent/agent.yaml), [docker-compose](docker-compose.yaml) and [Nginx](./nginx/nginx.conf) #15 (@thomasdesplaces)

### Updating
- Update [GitIgnore](./.gitignore) (@thomasdesplaces)
- Update README with some informations about ports and postgres exporter (@thomasdesplaces)
- Reduce testing time from 30s to 10s in [k6](./generate_data_application/load_tests/script.js) (@thomasdesplaces)
- Change the log level from DEBUG to INFO in [settings](./generate_data_application/backend/app/settings.py) (@thomasdesplaces)

### Corrections
- Correction in [Datasource](./grafana/datasource.yaml) for the link between traces to logs #12 (@thomasdesplaces)
- Correction in some files to see the traces througth the functions which are call in the FastAPI routes (@thomasdesplaces) :
    - [clients.py](./generate_data_application/backend/app/clients.py)
    - [crud_clients.py](./generate_data_application/backend/app/crud_clients.py)
    - [main.py](./generate_data_application/backend/app/main.py)
    - [observability.py](./generate_data_application/backend/app/observability.py)

0.0.2 - 2022-12-15
===================

### Features
- Add [Application stack](./generate_data_application/) (@thomasdesplaces)
- Add CHANGELOG.md (@thomasdesplaces)
- Add MAINTAINERS.md (@thomasdesplaces)

### Updating
- Update README with the architecture of application stack and a new source (@thomasdesplaces)
- Update [agent.yaml](./agent/agent.yaml) for the application stack (@thomasdesplaces)
- Change log level for Grafana in [config.ini](./grafana/config.ini) (@thomasdesplaces)
- Update [Loki config](./loki/loki-config.yaml) for the application stack (@thomasdesplaces)
- Update log level for Mimir in [mimir.yaml](./mimir/mimir.yaml) (@thomasdesplaces)
- Update log level for NGinx in [nginx.conf](./nginx/nginx.conf) (@thomasdesplaces)
- Update log level for Tempo in [tempo.yaml](./tempo/tempo.yaml) (@thomasdesplaces)
