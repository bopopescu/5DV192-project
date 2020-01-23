provider "google" {
  credentials = file("credentials.json")
  project     = "testproject-261510"
  region      = "europe-west2"
  zone        = "europe-west2-a"
}

resource "google_compute_instance" "vm_instance" {

  count		   = 1
  name         = "scaler-${count.index}"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network       = "default"
    access_config {
      nat_ip = "34.89.115.86"
    }
  }

  metadata = {}
  metadata_startup_script = file("init.sh")

}

