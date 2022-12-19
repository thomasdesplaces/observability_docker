FROM postgres:15-bullseye
# Install libpq-dev to solve these error : (psycopg2.OperationalError) SCRAM authentication requires libpq version 10 or above
RUN apt-get update && apt-get -y install --no-install-recommends libpq-dev=15.1-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB clients
COPY clients.sql /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/
EXPOSE 5432
