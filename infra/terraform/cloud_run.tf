resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_cloud_run_v2_service" "prediction_service" {
  name     = "readmission-prediction-api"
  location = var.region
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" # Placeholder until real image is built
      
      env {
        name  = "MODEL_BUCKET"
        value = google_storage_bucket.model_artifacts.name
      }
      
      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
  
  depends_on = [google_project_service.cloud_run]
}

# Allow unauthenticated invocations for demo purposes (Secure in prod!)
resource "google_cloud_run_service_iam_binding" "default" {
  location = google_cloud_run_v2_service.prediction_service.location
  service  = google_cloud_run_v2_service.prediction_service.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}
