provider "google" {
  credentials = "${file("../../credentials.json")}"
  project     = "testproject-261510"
  region      = "europe-north1"
  zone        = "europe-north1-a"
}

resource "google_compute_instance" "vm_instance" {

  count		   = 1
  name         = "master-${count.index}"
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
      nat_ip = "35.228.95.170"
    }
  }

  metadata = {
  }

  metadata_startup_script = "${file("init.sh")}"

}

resource "google_compute_firewall" "default" {
  name    = "firewall-master"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "800", "1000-2000", "5000", "22", "5672", "15672", "9419", "15692","3000","9090","5005","9100"]
  }

  source_tags = ["web"]
  source_ranges = ["0.0.0.0/0"]

}

resource "google_compute_subnetwork" "vpc_subnetwork" {
  name          = "subnetwork-master"
  ip_cidr_range = "10.0.0.0/22"
  region        = "europe-north1"
  network       = google_compute_network.vpc_network.self_link
}


resource "google_compute_network" "vpc_network" {
  name                    = "network-master"
  auto_create_subnetworks = "false"
}
