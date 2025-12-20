import base64
import json
import os
import smtplib
from email.mime.text import MIMEText
import functions_framework


@functions_framework.cloud_event
def notify_on_failure(cloud_event):
    # Decode Pub/Sub message
    message = cloud_event.data.get("message", {})
    data = message.get("data")

    if not data:
        print("No data found in Pub/Sub message")
        return

    payload = json.loads(base64.b64decode(data).decode("utf-8"))

    # alert on faluire build
    if payload.get("status") != "FAILURE":
        print(f"Ignoring build with status: {payload.get('status')}")
        return

    project_id = payload.get("projectId")
    build_id = payload.get("id")
    log_url = payload.get("logUrl")

    body = f"""
dbt tests failed in Cloud Build.

Project: {project_id}
Build ID: {build_id}
Logs: {log_url}
"""

    msg = MIMEText(body)
    msg["Subject"] = "❌ dbt Test Failure (Cloud Build)"
    msg["From"] = os.environ["SENDER_EMAIL"]
    msg["To"] = os.environ["RECEIVER_EMAIL"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            os.environ["SENDER_EMAIL"],
            os.environ["GMAIL_APP_PASSWORD"]
        )
        server.send_message(msg)

    print("Failure notification email sent")
