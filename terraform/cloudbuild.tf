# terraform/cloudbuild.tf

resource "google_cloudbuild_trigger" "github-trigger" {
  name        = "github-trigger"
  description = "Triggers build and deploy on push to the main branch"
  
  github {
    owner = var.github_owner
    name  = var.github_repo_name
    push {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"
  service_account = google_service_account.gbc-build-sa.id

  substitutions = {
    _REGION       = var.gcp_region
    _SERVICE_NAME = google_cloud_run_v2_service.gbc-api-service.name
    _REPO_ID      = google_artifact_registry_repository.gbc-api-repo.repository_id
  }
}