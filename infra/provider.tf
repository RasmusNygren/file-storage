terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~>4.55.0"
        }
    }
}

provider "aws" {
  region = "eu-north-1"
  profile = "fastapi-lambda"
}
