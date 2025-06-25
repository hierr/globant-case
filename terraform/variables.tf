# variables.tf

variable "gcp_project_id" {
  description = "GCP project ID."
  type        = string
}

variable "gcp_region" {
  description = "GCP region for resources."
  type        = string
  default     = "us-south1"
}

variable "db_password" {
  description = "Password for the Cloud SQL database user."
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "The owner of the GitHub repository."
  type        = string
}

variable "github_repo_name" {
  description = "The name of the GitHub repository."
  type        = string
}