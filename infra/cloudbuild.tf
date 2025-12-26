resource "google_cloudbuild_trigger" "dbt_ci" {
  name = "dbt-ci-trigger"

  github {
    owner = "Amir380-A"
    name  = "gcp_data_project"

    push {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"
}




resource "google_cloudbuild_trigger" "composer_build" {
  name = "composer-build-trigger"

  github {
    owner = "Amir380-A"
    name  = "gcp_data_project"

    push {
      branch = "^main$"
    }
  }

  included_files = [
    "composer/**"
  ]

  filename = "cloudbuild-composer.yaml"
}
