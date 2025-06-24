# networking.tf

# Look up the default network
data "google_compute_network" "gbc-default-network" {
  name = "default"
}

# Reserve a private IP address for Cloud SQL
resource "google_compute_global_address" "gbc-private-ip-address" {
  project       = var.gcp_project_id
  provider      = google-beta
  name          = "gbc-private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = data.google_compute_network.gbc-default-network.self_link
  depends_on = [null_resource.api_services_gate]
}

# Connect the VPC to the Cloud SQL service
resource "google_service_networking_connection" "gbc-vpc-connection" {
  provider                = google-beta
  network                 = data.google_compute_network.gbc-default-network.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.gbc-private-ip-address.name]
  depends_on = [null_resource.api_services_gate]
}