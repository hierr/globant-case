# iam.tf

# Service account for Cloud Run
resource "google_service_account" "gbc-run-sa" {
  account_id   = "gbc-run-sa"
  display_name = "Service Account for Cloud Run"
  depends_on   = [null_resource.api_services_gate]
}

# Allow the Cloud Run SA to connect to Cloud SQL
resource "google_project_iam_member" "gbc-sql-client" {
  project = var.gcp_project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.gbc-run-sa.email}"
  depends_on = [
    google_service_account.gbc-run-sa,
    null_resource.api_services_gate
  ]
}

# Allow the Cloud Run SA to access the secret
resource "google_project_iam_member" "gbc-secret-accessor" {
  project = var.gcp_project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.gbc-run-sa.email}"
  depends_on = [
    google_service_account.gbc-run-sa,
    null_resource.api_services_gate
  ]
}

# Service account for Cloud Build
resource "google_service_account" "gbc-build-sa" {
  account_id   = "gbc-build-sa"
  display_name = "Service Account for Cloud Build"
  depends_on   = [null_resource.api_services_gate]
}

# Grant Cloud Build SA permissions
resource "google_project_iam_member" "gbc-build-run-admin" {
  project = var.gcp_project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.gbc-build-sa.email}"
  depends_on = [
    google_service_account.gbc-build-sa,
    null_resource.api_services_gate
  ]
}

# Allow the Cloud Build SA to write to Artifact Registry
resource "google_project_iam_member" "gbc-build-artifact-writer" {
  project = var.gcp_project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.gbc-build-sa.email}"
  depends_on = [
    google_service_account.gbc-build-sa,
    null_resource.api_services_gate
  ]
}

# Allow the Cloud Build SA to act as a user of the Cloud Run SA
resource "google_project_iam_member" "gbc-build-iam-user" {
  project = var.gcp_project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.gbc-build-sa.email}"
  depends_on = [
    google_service_account.gbc-run-sa,
    google_service_account.gbc-build-sa,
    null_resource.api_services_gate
  ]
}
