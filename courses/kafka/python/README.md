# Kafka course in Python (Section 9: Kafka Java Programming 101)

The course codes in Java. These files do the same lessons with `confluent-kafka`.

```bash
cd ~/Developer/learning/courses/kafka && docker compose up -d     # start Kafka first
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic demo_python --partitions 3
cd python && uv run <file>.py
```

`docker compose down` deletes all topics. Recreate `demo_python` with `--partitions 3` afterwards: if a producer writes to it first, Kafka auto-creates it with only 1 partition.

| Lesson | File | Key idea |
|---|---|---|
| 47 Producer | `producer_demo.py`, `producer_loop.py` | `produce()` only puts the message in a buffer; a background thread sends it. Always `flush()` before exiting, or buffered messages are lost |
| 48 Callbacks | `producer_callback.py` | One callback per message with the result: partition and offset, or the error. `poll()` runs waiting callbacks. With `acks=0` the offset is -1 (Kafka never answers) |
| 49 Keys | `producer_keys.py` | Same key goes to the same partition (`hash(key) % partitions`), so its messages stay in order. Python uses CRC32, Java uses murmur2; set `"partitioner": "murmur2_random"` to match Java |
| 50 Consumer | `consumer_demo.py` | Pull loop around `poll(1.0)`. `group.id` = the team; `auto.offset.reset` is used only when the group has no saved offset yet |
| 51 Graceful shutdown | `consumer_shutdown.py` | `close()` in `finally` commits the last offsets (no duplicates) and leaves the group at once (no 45 s wait) |
| 52 Consumer group | `consumer_group.py` | Same `group.id` started several times: partitions are split, one partition per consumer at most. `on_assign`/`on_revoke` show each rebalance. Default rebalance is "stop the world" |
| 53 Cooperative and static | `consumer_cooperative.py` | `cooperative-sticky` moves only the partitions that must move. `group.instance.id` lets a consumer restart within `session.timeout.ms` without any rebalance |

## Verified on 2026-10-30

- Lesson 53, cooperative: with one consumer owning `[0, 1, 2]`, a second consumer joined. The first revoked only `[0]` and kept reading partitions 1 and 2 without a pause.
- Lesson 53, static: starting a second consumer with an id that is still in use (`s2`) makes Kafka fence the old one: `Static consumer fenced by other consumer with same group.instance.id`. Two live consumers can't share an instance id.

## Gotchas met so far

- A consumer started without `--from-beginning` (or with a group that already has offsets) shows only new messages.
- Closing a terminal doesn't always stop a Kafka CLI tool running in Docker. Stop it with Ctrl + C first, or `docker exec kafka pkill -f ConsoleConsumer`.
- Consumers with different `partition.assignment.strategy` can't share one group; `consumer_cooperative.py` uses its own group for that reason.
- Static members do not leave the group on `close()`: their partitions stay reserved, unread, until `session.timeout.ms` (45 s) passes.
