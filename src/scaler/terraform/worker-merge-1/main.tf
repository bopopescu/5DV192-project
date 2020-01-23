provider "google" {
  credentials = file("credentials.json")
  project     = "testproject-261510"
  region      = "europe-west1"
  zone        = "europe-west1-b"
}

resource "google_compute_instance" "vm_instance" {

  count		   = 1
  name         = "worker-merge-${count.index}"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  metadata = {}
  metadata_startup_script = file("init.sh")

}


