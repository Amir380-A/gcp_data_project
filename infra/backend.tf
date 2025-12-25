terraform {
  backend "gcs" {
    bucket  = "terraform-state-data-pipeline-v1"
    prefix  = "infra/state"
  }
}

