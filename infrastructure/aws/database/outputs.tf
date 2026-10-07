output "database_address" {
  description = "Private DNS address for the RDS instance."
  value       = aws_db_instance.database.address
}

output "database_name" {
  description = "Database name."
  value       = aws_db_instance.database.db_name
}

output "database_port" {
  description = "Database port."
  value       = aws_db_instance.database.port
}

output "master_secret_arn" {
  description = "Secrets Manager ARN for the RDS-managed administrative credentials. Do not use this account in the application."
  value       = aws_db_instance.database.master_user_secret[0].secret_arn
}

output "database_security_group_id" {
  description = "Security group attached to the private RDS instance."
  value       = aws_security_group.database.id
}
