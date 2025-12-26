resource "google_bigquery_dataset" "raw" {
  dataset_id = "ecomm"
  location   = var.region
}

resource "google_bigquery_dataset" "staging" {
  dataset_id = "analytics_staging"
  location   = var.region
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = "analytics"
  location   = var.region
}

