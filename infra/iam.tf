resource "google_project_iam_member" "cloudbuild_bq" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${var.project_id}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_bq_job" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${var.project_id}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild_gcs" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${var.project_id}@cloudbuild.gserviceaccount.com"
}

