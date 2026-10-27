# Kafka course: Stephane Maarek, *Apache Kafka Series: Learn Apache Kafka for Beginners v3*

Plan weeks 1-2 (Oct 26 - Nov 8). After this course comes the free Confluent Developer courses (Schema Registry 101, Kafka Connect 101) and the Debezium tutorial, then the wiki-pulse project.

## Kafka setup: Docker, not Conduktor and not a Mac install

```bash
docker compose up -d          # start Kafka 4.3.2 (KRaft) + web UI
open http://localhost:8080    # web UI: topics, messages, consumer groups
docker compose stop           # pause, keeps your topics
docker compose down           # remove everything (topics are wiped)
```

The Kafka CLI tools are on your PATH (added in `~/.zprofile`), so the course commands work as typed from any folder in a new terminal:

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic first_topic --partitions 3
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first_topic
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --from-beginning
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group
```

How it works: each name in `bin/` is a link to the `k` script, which runs the real tool inside the `kafka` container with `docker exec`. Kafka and Java exist only inside Docker, not on the Mac. A tool that reads a file path, such as `--producer.config my.properties`, cannot see your Mac's files; pipe input with `<` instead, or ask how to mount the folder.

### What the setup lectures say, and what to do here
| Lecture step | Here |
|---|---|
| Install Java | Skip. Java is inside the container |
| Download Kafka, extract it, add `bin` to PATH | Done: `bin/` is on PATH |
| Start ZooKeeper | Skip. Kafka 4 removed ZooKeeper |
| KRaft mode: `kafka-storage.sh random-uuid`, then `format`, then `kafka-server-start.sh` | Done by `docker compose up -d`. The broker runs in KRaft mode (`KAFKA_PROCESS_ROLES: broker,controller` in `docker-compose.yml`) with a fixed `CLUSTER_ID`. `format` and the server start/stop commands print an explanation instead of breaking the running broker |
| Conduktor playground or Conduktor UI | Use `localhost:9092` and drop `--command-config playground.config`; the UI is http://localhost:8080 |

To remove the PATH entry later, delete the three "Kafka course" lines at the end of `~/.zprofile`.

The setup was tested on 2026-10-25: topic creation, CLI produce and consume from a new shell, the KRaft lecture commands, a Python client from the Mac, and the UI.

## Course code: `code/`

The course's command files, copied from `~/Downloads/code`. They are lists of commands to paste one at a time, not scripts to run. Checked against this setup on 2026-10-25:

| Folder | Here |
|---|---|
| `1-kafka-cli` | Works as typed, except: `--replication-factor 2` fails on purpose (one broker). The `num.partitions=3` step can't be done by editing `server.properties`, and the setting can't be changed while the broker runs; to try it, add `KAFKA_NUM_PARTITIONS: 3` under `environment` in `docker-compose.yml` and run `docker compose up -d`, which recreates the broker and wipes your topics. The `--formatter` class was renamed in Kafka 4; the copy in `code/` already uses the new name |
| `2-kafka-extended` | Does not run here: Kafka Connect needs connector JARs and its config files inside the container, and Elasticsearch/OpenSearch and Schema Registry are not in `docker-compose.yml`. Watch these lectures; Kafka Connect 101 and Schema Registry 101 cover them hands-on next |
| `3-kafka-topic-configurations` | Works as typed |

Warnings such as `--property is deprecated ... Use --reader-property instead` (or `--formatter-property`, `--command-property`) are harmless: Kafka 4 renamed these flags and the old names still work.

## Java sections: redo them in Python

The course codes in Java. Write the same programs in Python with `confluent-kafka`, which is what the projects will use:

```bash
mkdir python && cd python
uv init --name kafka-course && uv add confluent-kafka
uv run producer.py
```

Python clients on the Mac use `bootstrap.servers = localhost:9092`.

## Focus on
- Topics, partitions, keys and ordering (ordering holds only within a partition)
- Consumer groups, offsets, commits, rebalancing
- `acks`, idempotent producer, retries; at-least-once vs exactly-once
- Retention vs log compaction; choosing a partition count
- Why Kafka and not RabbitMQ (a log you can replay vs a queue that deletes on ack)

## Skip
ZooKeeper, cluster administration, deep SASL/SSL security, ksqlDB, Kafka Streams in Java, the REST Proxy, Confluent Cloud-only features.

## Done when you can explain without notes
- [ ] What happens when a consumer in a group dies
- [ ] Why a message can be processed twice, and how to make processing idempotent
- [ ] How the key decides the partition, and what happens to ordering if you add partitions
- [ ] Kafka vs RabbitMQ, for analytics events and for an email task queue

## Progress
| Date | Section | Notes |
|---|---|---|
