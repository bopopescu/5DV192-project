provider "google" {
  credentials = "${file("../../config/credentials.json")}"
  project     = "testproject-261510"
  region      = "europe-north1"
  zone        = "europe-north1-a"
}

resource "google_compute_instance" "vm_instance" {

  count		   = 1
  name         = "service-registry-${count.index}"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network       = google_compute_network.vpc_network.self_link
    subnetwork    = google_compute_subnetwork.vpc_subnetwork.self_link
    access_config {
    }
  }

  metadata = {
   ssh-keys = "c15knn:${file("../../config/id_rsa.pub")}"
  }

  metadata_startup_script = "${file("init.sh")}"

}

resource "google_compute_firewall" "default" {
  name    = "firewall-service-registry"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "800", "1000-2000", "5000", "22"]
  }

  source_tags = ["web"]
  source_ranges = ["0.0.0.0/0"]

}

resource "google_compute_subnetwork" "vpc_subnetwork" {
  name          = "subnetwork-worker-service-registry"
  ip_cidr_range = "10.0.0.0/22"
  region        = "europe-north1"
  network       = google_compute_network.vpc_network.self_link
}

resource "google_compute_network" "vpc_network" {
  name                    = "network-service-registry"
  auto_create_subnetworks = "false"
}
