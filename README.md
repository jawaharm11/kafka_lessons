# kafka_lessons

**Deploying a PLAINTEXT Cluster using docker**

Default cluster build is located in docker-compose.yml file, builds 3 node zookeeper and 3 broker cluster with PLAINTEXT Listener.
```
# git clone https://github.com/babjid/kafka_lessons.git
# cd build_docker
# docker-compose up
```


**Deploying an SSL Cluster using docker**

We will need to generate ssl certificates for deploying an SSL cluster. The script located under `scripts/gen_docker_ssl_certs.sh` will generate keystores for 3 brokers, a producer and a consumer client under the directory located at environment variable KAFKA_SSL_SECRETS_DIR.

```
# export KAFKA_SSL_SECRETS_DIR=$HOME/secrets (or any other location as required)
# sh scripts/gen_docker_ssl_certs.sh
# cd build_docker
# docker-compose -f kafka-ssl.yml up
```

**Connecting to an SSL Cluster and creating a topic**

Assuming that kafka binaries are downloaded locally on the laptop and ssl.properties has been updated with proper location of the client keystore and truststore

```
# kafka-topics.sh --command-config <path>/ssl.properties --bootstrap-server localhost:19092  --list 
# kafka-topics.sh --command-config <path>/ssl.properties --bootstrap-server localhost:19092 --create --topic test --partitions 3 --replication-factor 2
```
