variable "prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "apex"
}

variable "pg_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "image_name" {
  description = "Docker image name"
  type        = string
  default     = "apex-mvp"
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}
