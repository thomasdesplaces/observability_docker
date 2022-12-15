FROM python:bullseye
RUN apt-get update && apt-get install --no-install-recommends -y systemctl=1.4.4181-1.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/local/bin/
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Configure Promtail to send logs to Grafana Agent
RUN curl -s -q https://api.github.com/repos/grafana/loki/releases/latest | grep browser_download_url |  cut -d '"' -f 4 | grep promtail-linux-arm64.zip | wget -i - && \
    unzip promtail-linux-arm64.zip && \
    mv ./promtail-linux-arm64 ./promtail
COPY config/promtail-config.yaml /etc/promtail/
RUN useradd --system promtail
COPY config/promtail.service /etc/systemd/system/

# Configure FastAPI application
WORKDIR /usr/src/app
RUN chmod a+rwx /usr/src/app
COPY config/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app .
COPY config/start.sh ./config/
EXPOSE 5050
CMD ["/bin/sh", "./config/start.sh"]
