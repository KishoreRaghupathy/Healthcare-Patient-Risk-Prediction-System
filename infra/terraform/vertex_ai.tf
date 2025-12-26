resource "google_project_service" "vertex_ai" {
  service = "aiplatform.googleapis.com"
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "patient-risk-repo"
  description   = "Docker repository for Patient Risk System"
  format        = "DOCKER"
}
