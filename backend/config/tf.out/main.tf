locals {
  input_data = jsondecode(file("input.json"))
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = local.input_data.region
  access_key = local.input_data.access_key
  secret_key = local.input_data.secret_key
}

# Create a VPC
resource "aws_vpc" "main" {
  cidr_block = local.input_data.cidr_block
  tags       = local.input_data.tags
}

resource "aws_subnet" "myvpc" {
  count                  = local.input_data.subnet_count
  vpc_id                 = aws_vpc.main.id
  cidr_block             = cidrsubnet(local.input_data.cidr_block, local.input_data.subnet_length, count.index)
  tags                   = merge(local.input_data.tags, {Name = "${local.input_data.name}-subnet-${count.index}"})
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_ids" {
  value = aws_subnet.myvpc[*].id
}
