output "raw_bucket" {
  value = google_storage_bucket.raw_data.name
}

output "dbt_docs_bucket" {
  value = google_storage_bucket.dbt_docs.name
}

