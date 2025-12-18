import json
import time
from datetime import datetime, timezone
from google.cloud import bigquery
from google.cloud import pubsub_v1

# Configs
PROJECT_ID = "data-pipeline-478808"  
BQ_DATASET = "ecomm"      
BQ_TABLE   = "events"                
PUBSUB_TOPIC_ID = "events-stream"   
SPEEDUP_FACTOR = 300.0  

def fetch_events():
    """
    Read events from BigQuery ordered by created_at, sequence_number, id.
    You can add a WHERE filter or LIMIT when testing.
    """
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        SELECT
          id,
          user_id,
          sequence_number,
          session_id,
          created_at,
          ip_address,
          city,
          state,
          postal_code,
          browser,
          traffic_source,
          uri,
          event_type
        FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}`
        WHERE created_at IS NOT NULL
        ORDER BY created_at, sequence_number, id
        -- LIMIT 10000
    """

    job = client.query(query)
    for row in job:
        yield row


def replay_events():
    """
    Stream events from BigQuery into Pub/Sub, simulating real-time based on
    created_at and SPEEDUP_FACTOR.
    """
    pub_client = pubsub_v1.PublisherClient()
    topic_path = pub_client.topic_path(PROJECT_ID, PUBSUB_TOPIC_ID)

    prev_ts = None
    count = 0

    for row in fetch_events():
        event_ts = row["created_at"]
        if isinstance(event_ts, str):
            event_ts = datetime.fromisoformat(event_ts.replace("Z", "+00:00"))
        elif isinstance(event_ts, datetime):
            if event_ts.tzinfo is None:
                event_ts = event_ts.replace(tzinfo=timezone.utc)

        if prev_ts is not None and event_ts is not None:
            delta_sec = (event_ts - prev_ts).total_seconds()
            sleep_sec = max(delta_sec / SPEEDUP_FACTOR, 0.0)
            if sleep_sec > 0:
                time.sleep(sleep_sec)
        prev_ts = event_ts

        payload = {
            "id": row["id"],
            "user_id": row["user_id"],
            "sequence_number": row["sequence_number"],
            "session_id": row["session_id"],
            "created_at": event_ts.isoformat() if event_ts else None,
            "ip_address": row["ip_address"],
            "city": row["city"],
            "state": row["state"],
            "postal_code": row["postal_code"],
            "browser": row["browser"],
            "traffic_source": row["traffic_source"],
            "uri": row["uri"],
            "event_type": row["event_type"],
        }

        data = json.dumps(payload).encode("utf-8")

        attrs = {
            "event_type": payload["event_type"] or "",
            "traffic_source": payload["traffic_source"] or "",
        }

        pub_client.publish(topic_path, data=data, **attrs)
        count += 1

        if count % 1000 == 0:
            print(f"Published {count} events so far...")

    print(f"Replay finished. Total events published: {count}")


if __name__ == "__main__":
    replay_events()

