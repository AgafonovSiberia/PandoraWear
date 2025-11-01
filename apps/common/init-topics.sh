#!/bin/bash
set -e

echo "⏳ Ждём Kafka на kafka:9092..."
while ! nc -z kafka 9092; do
  sleep 1
done

TOPICS=("pushes")

for topic in "${TOPICS[@]}"
do
  echo "📦 Проверка топика: $topic"
  kafka-topics --bootstrap-server kafka:9092 \
    --create --if-not-exists --replication-factor 1 --partitions 1 --topic "$topic"
done

echo "✅ Все топики готовы"