# outputs.tf

output "gbc-api-service-url" {
  description = "The URL of the deployed Cloud Run API service."
  value       = google_cloud_run_v2_service.gbc-api-service.uri
}

output "gbc-postgres-instance-connection-name" {
  description = "The connection name for the Cloud SQL instance, used by the application."
  value       = google_sql_database_instance.gbc-postgres-instance.connection_name
}