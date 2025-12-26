resource "google_storage_bucket" "raw_data" {
  name     = "${var.project_id}-raw-data"
  location = var.region

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "dbt_docs" {
  name     = "${var.project_id}-dbt-docs"
  location = var.region

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  uniform_bucket_level_access = true
}

