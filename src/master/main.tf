provider "google" {
  credentials = "${file("credentials.json")}"
  project     = "testproject-261510"
  region      = "europe-north1"
}
