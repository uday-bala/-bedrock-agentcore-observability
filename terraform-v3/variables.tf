variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "aws_account_id" {
  description = "AWS account ID"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3 bucket name for cache"
  type        = string
}

variable "agent_name" {
  description = "Agent name"
  type        = string
  default     = "my_observability_agent_v3"
}

variable "ecr_repository_url" {
  description = "ECR repository URL for agent container"
  type        = string
}
