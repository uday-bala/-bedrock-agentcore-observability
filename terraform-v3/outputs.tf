output "agent_role_arn" {
  description = "ARN of the IAM role for the agent"
  value       = aws_iam_role.agent_role.arn
}

output "runtime_arn" {
  description = "ARN of the AgentCore runtime"
  value       = awscc_bedrockagentcore_runtime.agent_runtime.id
}

output "runtime_name" {
  description = "Name of the AgentCore runtime"
  value       = awscc_bedrockagentcore_runtime.agent_runtime.agent_runtime_name
}

output "observability_dashboard" {
  description = "CloudWatch GenAI Observability Dashboard URL"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#gen-ai-observability/agent-core"
}

output "test_command" {
  description = "Command to test the deployed agent"
  value       = "python3 test_agent.py"
}
