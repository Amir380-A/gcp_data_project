resource "google_composer_environment" "myenv" {
  name   = "composer-env"
  region = "us-east1"
 config {
    software_config {
      image_version = "composer-3-airflow-2"
    }
  }
}