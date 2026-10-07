resource "aws_db_subnet_group" "database" {
  name       = "${var.name}-private"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name      = "${var.name}-private"
    Project   = "Assistente-Diversa"
    ManagedBy = "Terraform"
  }
}

resource "aws_security_group" "database" {
  name_prefix = "${var.name}-db-"
  description = "Private PostgreSQL access for the Assistente Diversa backend."
  vpc_id      = var.vpc_id

  tags = {
    Name      = "${var.name}-database"
    Project   = "Assistente-Diversa"
    ManagedBy = "Terraform"
  }
}

resource "aws_vpc_security_group_ingress_rule" "backend_postgres" {
  security_group_id            = aws_security_group.database.id
  referenced_security_group_id = var.backend_security_group_id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  description                  = "PostgreSQL from backend tasks only."
}

resource "aws_db_instance" "database" {
  identifier                          = var.name
  engine                              = "postgres"
  engine_version                      = var.engine_version
  instance_class                      = var.instance_class
  allocated_storage                   = 20
  max_allocated_storage               = 100
  storage_type                        = "gp3"
  storage_encrypted                   = true
  kms_key_id                          = var.kms_key_arn
  db_name                             = "assistente_diversa"
  username                            = var.db_username
  manage_master_user_password         = true
  master_user_secret_kms_key_id       = var.kms_key_arn
  port                                = 5432
  db_subnet_group_name                = aws_db_subnet_group.database.name
  vpc_security_group_ids              = [aws_security_group.database.id]
  publicly_accessible                 = false
  multi_az                            = true
  backup_retention_period             = 7
  copy_tags_to_snapshot               = true
  auto_minor_version_upgrade          = true
  deletion_protection                 = true
  skip_final_snapshot                 = false
  final_snapshot_identifier           = "${var.name}-final"
  apply_immediately                   = false
  enabled_cloudwatch_logs_exports     = ["postgresql", "upgrade"]
  performance_insights_enabled        = true
  performance_insights_retention_period = 7

  tags = {
    Name      = var.name
    Project   = "Assistente-Diversa"
    ManagedBy = "Terraform"
  }

  lifecycle {
    prevent_destroy = true
  }
}
