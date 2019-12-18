provider "google" {
  credentials = "${file("credentials.json")}"
  project     = "testproject-261510"
  region      = "europe-north1"
  zone        = "europe-north1-a"
}

resource "google_compute_instance" "vm_instance" {

  name         = "master-1"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = google_compute_network.vpc_network.self_link
    access_config {
    }
  }

}

resource "google_compute_firewall" "default" {
  name    = "master-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "800", "1000-2000"]
  }

  source_tags = ["web"]

}


resource "google_compute_network" "vpc_network" {
  name                    = "terraform-network"
  auto_create_subnetworks = "true"
}