resource "google_project_service" "dataflow" {
  service = "dataflow.googleapis.com"
  disable_on_destroy = false
}

resource "google_storage_bucket" "dataflow_staging" {
  name          = "${var.project_id}-dataflow-staging"
  location      = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}
