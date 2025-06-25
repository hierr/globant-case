# services.tf

# Enable the API
resource "google_project_service" "gbc-cloud-run-api" {
  service = "run.googleapis.com"
  depends_on = [null_resource.api_services_gate]
}

# Artifact Registry for Docker Images
resource "google_artifact_registry_repository" "gbc-api-repo" {
  location      = var.gcp_region
  repository_id = "gbc-api-repo"
  description   = "Docker repository for the Globant Case API"
  format        = "DOCKER"
  depends_on    = [null_resource.api_services_gate]
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "gbc-api-service" {
  name     = "gbc-api-service"
  location = var.gcp_region

  template {
    service_account = google_service_account.gbc-run-sa.email
    
    vpc_access {
      connector = google_vpc_access_connector.gbc-vpc-connector.name
      egress    = "ALL_TRAFFIC"
    }

    # Container config
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"  # Placeholder image

      # Environment variables
      env {
        name  = "DB_USER"
        value = google_sql_user.gbc-api-user.name
      }
      env {
        name  = "DB_NAME"
        value = google_sql_database.gbc-employment-db.name
      }
      env {
        name = "INSTANCE_CONNECTION_NAME"
        value = google_sql_database_instance.gbc-postgres-instance.connection_name
      }
      env {
        name = "DB_PASS_SECRET"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gbc-employment-db-password.secret_id
            version = "latest"
          }
        }
      }
    }
  }
  depends_on = [
    null_resource.api_services_gate,
    google_project_iam_member.gbc-sql-client,
    google_project_iam_member.gbc-secret-accessor
  ]
}

# Allow unauthenticated access to the API
resource "google_cloud_run_v2_service_iam_member" "gbc-api-noauth" {
  project  = google_cloud_run_v2_service.gbc-api-service.project
  location = google_cloud_run_v2_service.gbc-api-service.location
  name     = google_cloud_run_v2_service.gbc-api-service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
  depends_on = [
    google_cloud_run_v2_service.gbc-api-service
  ]
}