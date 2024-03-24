
variable "region" {
    description = "The region where the resources will be created."
}

variable "name" {
    description = "Name of the Resources"
}

variable "cidr_block" {
    description = "Base CIDR block"
    type        = string
    default     = "10.0.0.0/16"
}

variable "subnet_length" {
    description = "The new prefix length for the subnet"
    type        = number
}

variable "subnet_count" {
    description = "The number of subnets to create"
    type        = number
}

variable "tags" {
    description = "tags"
    type        = map(string)
    default     = {}
}

