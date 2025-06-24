# database.tf

# Cloud SQL instance for PostgreSQL
resource "google_sql_database_instance" "gbc-postgres-instance" {
  name             = "globant-case-postgres-instance"
  database_version = "POSTGRES_14"
  region           = var.gcp_region
  
  settings {
    tier = "db-g1-small"
    ip_configuration {
      ipv4_enabled    = false
      private_network = data.google_compute_network.gbc-default-network.self_link
    }
  }

  deletion_protection = false
  depends_on          = [null_resource.api_services_gate, google_service_networking_connection.gbc-vpc-connection]
}

# Database
resource "google_sql_database" "gbc-employment-db" {
  name     = "gbc_employment_db"
  instance = google_sql_database_instance.gbc-postgres-instance.name
}

# User
resource "google_sql_user" "gbc-api-user" {
  name     = "gbc-api-user"
  instance = google_sql_database_instance.gbc-postgres-instance.name
  password = var.db_password
}

# Secret for DB Password
resource "google_secret_manager_secret" "gbc-employment-db-password" {
  secret_id = "gbc-employment-db-password"
  replication {
    auto {}
  }
  depends_on = [null_resource.api_services_gate]
}

# Secret for DB Password version
resource "google_secret_manager_secret_version" "gbc-employment-db-password-version" {
  secret      = google_secret_manager_secret.gbc-employment-db-password.id
  secret_data = var.db_password
}