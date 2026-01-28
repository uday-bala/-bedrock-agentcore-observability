# Generate random suffix for unique naming
resource "random_id" "suffix" {
  byte_length = 4
}

# Create AgentCore Runtime using AWSCC provider (exact CDK equivalent)
resource "awscc_bedrockagentcore_runtime" "agent_runtime" {
  agent_runtime_name = "${replace(var.agent_name, "-", "_")}_${random_id.suffix.hex}"
  description        = "AgentCore V3 with complete observability and news tool"
  role_arn          = aws_iam_role.agent_role.arn

  agent_runtime_artifact = {
    container_configuration = {
      container_uri = "${var.ecr_repository_url}:latest"
    }
  }

  network_configuration = {
    network_mode = "PUBLIC"
  }

  environment_variables = {
    "OTEL_SERVICE_NAME" = "${replace(var.agent_name, "-", "_")}_${random_id.suffix.hex}"
    "LOG_LEVEL"         = "INFO"
  }

  tags = {
    "Environment" = "observability-demo"
    "Version"     = "v3"
    "Framework"   = "terraform"
  }

  depends_on = [
    aws_iam_role.agent_role,
    aws_iam_role_policy.bedrock_policy,
    aws_iam_role_policy.cloudwatch_policy,
    aws_iam_role_policy.s3_policy,
    aws_iam_role_policy.ecr_policy
  ]
}
