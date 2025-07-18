output "app_server_public_ip" {
  description = "Public IP address of the application server"
  value       = aws_instance.app.public_ip
}

output "app_server_private_ip" {
  description = "Private IP address of the application server"
  value       = aws_instance.app.private_ip
}

output "database_endpoint" {
  description = "RDS database endpoint"
  value       = aws_db_instance.main.endpoint
}

output "database_name" {
  description = "RDS database name"
  value       = aws_db_instance.main.db_name
}

output "s3_bucket_name" {
  description = "S3 bucket name for data storage"
  value       = aws_s3_bucket.data.bucket
}

output "server_info" {
  description = "Server connection information"
  value = {
    public_ip = aws_instance.app.public_ip
    note      = "Use AWS Systems Manager Session Manager or create a key pair for SSH access"
  }
}

output "application_url" {
  description = "URL to access the FastAPI application"
  value       = "http://${aws_instance.app.public_ip}:8000"
}

output "api_docs_url" {
  description = "URL to access the FastAPI documentation"
  value       = "http://${aws_instance.app.public_ip}:8000/docs"
}
