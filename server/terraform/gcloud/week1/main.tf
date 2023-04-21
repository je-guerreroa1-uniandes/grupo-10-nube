
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.62.1"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

resource "google_compute_project_default_network_tier" "default" {
  network_tier = "STANDARD"
  project      = var.project
}

# [START compute_vpc]
resource "google_compute_network" "g10_vpc" {
  name                    = "g10-vpc"
  auto_create_subnetworks = false
  mtu                     = 1460
}

// Network Address:	10.120.0.0
// Usable Host IP Range:	10.120.0.1 - 10.120.0.6
// INFO: IP '10.120.0.1' is already being used by another resource (Recurso por determinar)
// Broadcast Address:	10.120.0.7
// Subnet Mask:	255.255.255.248
// Short:	10.120.0.0/29
// IP Class:	C
// Total Number of Hosts:	8
// Number of Usable Hosts:	6
resource "google_compute_subnetwork" "g10_vpc_central" {
  name          = "g10-vpc-central"
  ip_cidr_range = "10.120.0.0/29"
  region        = var.region
  network       = google_compute_network.g10_vpc.id
}
# [END compute_vpc]

# [START compute_static_addresses]
data "google_compute_address" "reverse_proxy" {
  name = "reverse-proxy"
}
# [END compute_static_addresses]

# [START compute_engine_vms]
resource "google_compute_instance" "produccion" {
  name         = "produccion"
  machine_type = "custom-1-1024" # [1]vCPU [1] GB RAM
  zone         = var.zone
  tags         = ["g10-vpc", "ssh", "https-server", "http-server"]

  # Enable virtual display
  enable_display = true

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-jammy-v20230415"
      size  = 20
      type  = "pd-standard"
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file(var.ssh_pub_key_file)}"
  }

  network_interface {
    network    = google_compute_network.g10_vpc.id
    subnetwork = google_compute_subnetwork.g10_vpc_central.id
    network_ip = "10.120.0.2"

    access_config {
      nat_ip = data.google_compute_address.reverse_proxy.address // this adds regional static ip to VM
    }
  }
}
# [END compute_engine_vms]

# [START vpc_firewall_rules]
# ["ssh", "http-server", "https-server"] son default network tags
resource "google_compute_firewall" "internal_in" {
  name = "vpc-allow-custom-in"
  allow {
    # sin ports es all-ports
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.g10_vpc.id
  priority      = 1000
  source_ranges = ["10.120.0.0/29"]
  target_tags   = ["g10-vpc"]
}

resource "google_compute_firewall" "internal_out" {
  name = "vpc-allow-custom-out"
  allow {
    # sin ports es all-ports
    protocol = "tcp"
  }
  direction          = "EGRESS"
  network            = google_compute_network.g10_vpc.id
  priority           = 1000
  destination_ranges = ["10.120.0.0/29"]
  target_tags        = ["g10-vpc"]
}

resource "google_compute_firewall" "ssh_in" {
  name = "vpc-allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.g10_vpc.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh", "g10-vpc"]
}

# Para aceptar las conexiones desde https://console.cloud.google.com
resource "google_compute_firewall" "iap_in" {
  name = "vpc-allow-rdp-ingress-from-iap"
  allow {
    ports    = ["3389"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.g10_vpc.id
  priority      = 1000
  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["g10-vpc"]
}

resource "google_compute_firewall" "https_in" {
  name = "vpc-allow-https"
  allow {
    ports    = ["443"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.g10_vpc.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["https-server"]
}

resource "google_compute_firewall" "http_in" {
  name = "vpc-allow-http"
  allow {
    ports    = ["80"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.g10_vpc.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}

resource "google_compute_firewall" "https_out" {
  name = "vpc-send-dns-http-https"
  allow {
    ports    = ["53", "80", "443"]
    protocol = "tcp"
  }
  direction   = "EGRESS"
  network     = google_compute_network.g10_vpc.id
  priority    = 1000
  target_tags = ["g10-vpc"]
}
# [END vpc_firewall_rules]
