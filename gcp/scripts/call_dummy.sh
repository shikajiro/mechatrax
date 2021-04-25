printf '{
    "device_id": "%s",
    "temperature": "%s"
}' $1 $2 | curl localhost:8081 \
  -X POST \
  -H "Content-Type: application/json" \
  -d @-
