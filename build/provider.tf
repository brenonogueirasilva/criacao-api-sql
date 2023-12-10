terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version =  "~> 5.0.0"
    }
  }
}

provider "google" {
  credentials = file("../creds.json")
  project     = var.project_id
  region      = var.region
}