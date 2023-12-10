variable "project_id" {
  type = string
  default = "apt-theme-402300"
}

variable "region" {
  type = string
  default = "us-central1"
}

variable "service_account_email" {
  type = string
  default = "brasil-api-cloud-storage@apt-theme-402300.iam.gserviceaccount.com"
  
}

variable "github_token_file" {
  description = "Token GitHub"
  default     = "../github_token.json"
}

variable "app_installation_id" {
  type = number
  default = 43531708   
}

variable "remote_uri" {
  type = string
  default = "https://github.com/brenonogueirasilva/api_cloud_build_private.git" 
}


