variable "aws_region" {
  description = "AWS region for the managed database."
  type        = string
}

variable "name" {
  description = "Unique, lowercase identifier for this database."
  type        = string
  default     = "assistente-diversa"
}

variable "engine_version" {
  description = "Exact RDS PostgreSQL engine version available in the selected region."
  type        = string
}

variable "instance_class" {
  description = "RDS instance size, chosen for the expected production workload."
  type        = string
}

variable "vpc_id" {
  description = "VPC where the application and private database will run."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnets in at least two Availability Zones."
  type        = list(string)

  validation {
    condition     = length(var.private_subnet_ids) >= 2
    error_message = "Provide private subnet IDs from at least two Availability Zones."
  }
}

variable "backend_security_group_id" {
  description = "Security group attached to the backend tasks; the database accepts PostgreSQL only from this group."
  type        = string
}

variable "db_username" {
  description = "Administrative database username. Its password is managed by RDS in Secrets Manager."
  type        = string
  default     = "assistente_admin"
}

variable "kms_key_arn" {
  description = "Optional customer-managed KMS key ARN for RDS storage and the managed master secret."
  type        = string
  default     = null
}
