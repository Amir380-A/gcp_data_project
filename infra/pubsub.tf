resource "google_pubsub_topic" "build_status" {
  name = "cloud-build-status"
}

resource "google_pubsub_topic" "topic" {
  name = "events-stream"
}
