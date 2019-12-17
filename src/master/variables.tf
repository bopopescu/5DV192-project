variable "region" {
  default = "europe-north1"
}

variable "region_zone" {
  default = "europe-north1-a"
}

variable "project_name" {
  description = "testproject-261510"
}

variable "credentials_file_path" {
  description = "Path to the JSON file used to describe your account credentials"
  default     = "credentials.json"
}

variable "public_key_path" {
  description = "Path to file containing public key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "private_key_path" {
  description = "Path to file containing private key"
  default     = "~/.ssh/id_rsa"
}