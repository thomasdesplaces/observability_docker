# Create container to run tests with k6.io
FROM grafana/k6:0.42.0
WORKDIR /scripts
COPY script.js .
CMD ["run", "/scripts/script.js", "-o", "experimental-prometheus-rw"]
