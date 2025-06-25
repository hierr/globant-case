# apis.tf

locals {
  required_apis = toset([
    "run.googleapis.com",                 # Cloud Run
    "sqladmin.googleapis.com",            # Cloud SQL Admin
    "artifactregistry.googleapis.com",    # Artifact Registry
    "secretmanager.googleapis.com",       # Secret Manager
    "cloudbuild.googleapis.com",          # Cloud Build
    "iam.googleapis.com",                 # IAM
    "cloudresourcemanager.googleapis.com", # Cloud Resource Manager
    "servicenetworking.googleapis.com",   # Service Networking
    "compute.googleapis.com",             # Compute Engine
    "vpcaccess.googleapis.com",           # VPC Access
  ])
}

resource "google_project_service" "gbc-project-apis" {
  for_each = local.required_apis

  project                    = var.gcp_project_id
  service                    = each.key
  disable_on_destroy         = false
}

# This resource is used to create a single dependency point for all APIs
resource "null_resource" "api_services_gate" {
  depends_on = [google_project_service.gbc-project-apis]
}