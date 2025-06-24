# main.tf

# Google Cloud provider
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.34"
    }
  }
}

# Provider configuration
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Remote state bucket
terraform {
  backend "gcs" {
    bucket = "globant-case-tfstate-w85vr1"
    prefix = "globant-case/state"
  }
}
