/*
https://collabnix.com/5-minutes-to-run-your-first-docker-container-on-google-cloud-platform-using-terraform/
*/

/*
https://stackoverflow.com/questions/45359189/how-to-map-static-ip-to-terraform-google-compute-engine-instance
access_config {
      nat_ip = "35.217.38.57" // this adds regional static ip to VM
    }
*/

provider "google" {
  credentials = "${file("credentials.json")}"
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
    # A default network is created for all GCP projects
    network       = google_compute_network.vpc_network.self_link
    access_config {
      nat_ip = "35.228.95.170"
    }
  }

  metadata = {
   ssh-keys = "c15knn:${file("../../config/id_rsa.pub")}"
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
    ports    = ["80", "8080", "800", "1000-2000", "5000", "22", "5672", "15672"]
  }

  source_tags = ["web"]
  source_ranges = ["0.0.0.0/0"]

}


resource "google_compute_network" "vpc_network" {
  name                    = "network-master"
  auto_create_subnetworks = "true"
}
