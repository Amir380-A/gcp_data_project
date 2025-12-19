import base64
import json
import functions_framework
from datetime import datetime, timezone
from google.cloud import aiplatform
from google.cloud import bigquery

PROJECT_ID = "data-pipeline-478808"
REGION = "us-east1"
ENDPOINT_RESOURCE = (
    "projects/1056401772198/"
    "locations/us-east1/"
    "endpoints/7929328214822879232"
)

BQ_PROJECT = "data-pipeline-478808"
BQ_DATASET = "ecomm"
BQ_TABLE = "model_feedback"

aiplatform.init(project=PROJECT_ID, location=REGION)
endpoint = aiplatform.Endpoint(ENDPOINT_RESOURCE)

bq_client = bigquery.Client(project=BQ_PROJECT)
table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"

@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    message_data = cloud_event.data["message"]["data"]
    decoded = base64.b64decode(message_data).decode("utf-8")
    event = json.loads(decoded)
    instance = {
        "id": str(event.get("id")),
        "user_id": str(event.get("user_id")),
        "session_id": event.get("session_id"),
        "created_at": event.get("created_at"),
        "ip_address": event.get("ip_address"),
        "city": event.get("city"),
        "state": event.get("state"),
        "postal_code": str(event.get("postal_code")),
        "browser": event.get("browser"),
        "traffic_source": event.get("traffic_source"),
        "uri": event.get("uri"),
        "event_type": event.get("event_type"),
    }

    response = endpoint.predict(instances=[instance])
    prediction = response.predictions[0]

    classes = prediction["classes"]
    scores = prediction["scores"]
    best_idx = scores.index(max(scores))

    row = {
        "event_id": str(event.get("id")),
        "user_id": str(event.get("user_id")),
        "session_id": event.get("session_id"),
        "event_type": event.get("event_type"),
        "uri": event.get("uri"),
        "predicted_class": classes[best_idx],
        "predicted_score": float(scores[best_idx]),
        "converted": event.get("event_type") == "purchase",
        "prediction_time": datetime.now(timezone.utc).isoformat(),
        "ingestion_time": datetime.now(timezone.utc).isoformat(),
    }
    errors = bq_client.insert_rows_json(table_id, [row])
    if errors:
        print("BQ errors:", errors)

    return "OK"
