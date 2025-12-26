# Service Account for Dataflow
resource "google_service_account" "etl_sa" {
  account_id   = "etl-service-account"
  display_name = "ETL Service Account"
}

# Service Account for Training
resource "google_service_account" "training_sa" {
  account_id   = "training-service-account"
  display_name = "Training Service Account"
}

# Service Account for Serving
resource "google_service_account" "serving_sa" {
  account_id   = "serving-service-account"
  display_name = "Serving Service Account"
}

# Grant GCS Object Admin to ETL SA on raw and processed buckets
resource "google_storage_bucket_iam_member" "etl_raw_admin" {
  bucket = google_storage_bucket.raw_data.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.etl_sa.email}"
}

resource "google_storage_bucket_iam_member" "etl_processed_admin" {
  bucket = google_storage_bucket.processed_data.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.etl_sa.email}"
}

# Grant Vertex AI User to Training SA
resource "google_project_iam_member" "training_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.training_sa.email}"
}
