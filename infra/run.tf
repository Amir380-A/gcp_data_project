resource "google_storage_bucket" "functions_src" {
  name                        = "${var.project_id}-functions-src"
  location                    = var.region
  uniform_bucket_level_access = true
}

resource "google_cloudfunctions2_function" "events_stream_function" {
  name     = "events-stream-function"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "handler"

    source {
      storage_source {
        bucket = google_storage_bucket.functions_src.name  
        object = "functions/events_stream.zip"
      }
    }
  }

  service_config {
    available_memory = "256M"
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.topic.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

resource "google_cloudfunctions2_function" "build_status_function" {
  name     = "build-status-function"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "handler"

    source {
      storage_source {
        bucket = google_storage_bucket.functions_src.name
        object = "functions/build_function.zip"
      }
    }
  }

  service_config {
    available_memory = "256M"
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.build_status.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}
