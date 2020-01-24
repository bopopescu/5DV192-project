provider "google" {
  credentials = "${file("credentials.json")}"
  project     = "testproject-261510"
  region      = "europe-west3"
  zone        = "europe-west3-a"
}

resource "google_compute_instance" "vm_instance" {

  count		   = 3
  name         = "worker-split-${count.index}"
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
  metadata_startup_script = "${file("init.sh")}"

}

