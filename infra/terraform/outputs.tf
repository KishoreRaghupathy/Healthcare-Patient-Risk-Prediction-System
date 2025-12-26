output "raw_data_bucket" {
  value = google_storage_bucket.raw_data.name
}

output "processed_data_bucket" {
  value = google_storage_bucket.processed_data.name
}

output "model_bucket" {
  value = google_storage_bucket.model_artifacts.name
}

output "prediction_service_url" {
  value = google_cloud_run_v2_service.prediction_service.uri
}

output "artifact_registry_repo" {
  value = google_artifact_registry_repository.docker_repo.name
}
