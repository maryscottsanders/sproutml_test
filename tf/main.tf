provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "excella-prod-ml"
    key    = "terraform/terraform.tfstate"
    region = "us-east-1"
  }
}

variable "region" {}
variable "accountId" {}
