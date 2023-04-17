FROM postgres:latest

ENV POSTGRES_USER converter_db
ENV POSTGRES_PASSWORD ckhAMLIteFlYheRptAteapeze
ENV POSTGRES_DB conversion

RUN localedef -i es_ES -c -f utf-8 -A /usr/share/locale/locale.alias es_ES.utf-8
ENV LANG C.UTF-8

COPY docker_postgres_init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432