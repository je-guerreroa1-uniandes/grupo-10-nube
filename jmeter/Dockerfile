FROM arm64v8/openjdk:8-jre-slim-buster

ARG JMETER_VERSION=5.4.1

ENV JMETER_HOME /opt/apache-jmeter-${JMETER_VERSION}
ENV PATH $JMETER_HOME/bin:$PATH

RUN apt-get update && \
    apt-get -y install curl unzip && \
    curl -L https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz \
    | tar xz -C /opt && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

CMD ["jmeter", "--version"]
