# Bedrock AgentCore Observability Setup - Simple Example

This repository contains both CDK and Terraform implementations for deploying AWS Bedrock AgentCore with complete observability using ADOT (AWS Distro for OpenTelemetry) and without use of Starter Toolkit

## Features

- **Complete Observability**: ADOT auto-instrumentation for full trace visibility
- **Enhanced Agent**: V3 agent with weather, stock price, and news tools
- **S3 Caching**: Intelligent caching system for API responses
- **CloudWatch Integration**: Automatic trace delivery to CloudWatch and X-Ray
- **Multi-Framework Support**: Both CDK and Terraform implementations

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker installed and running
- CDK CLI (for CDK deployment) or Terraform (for Terraform deployment)
- Python 3.8+

## Quick Start

### Option 1: CDK Deployment

```bash
cd cdk-v3
# Update configuration
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Deploy
./deploy-v3.sh
```

### Option 2: Terraform Deployment

```bash
cd terraform-v3
# Update configuration
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Setup ECR repository
./setup-ecr.sh

# Deploy infrastructure
./deploy.sh
```

## Configuration

### Required Variables

Update the following in your configuration files:

- `YOUR_ACCOUNT_ID`: Your AWS account ID
- `YOUR_REGION`: Your preferred AWS region (e.g., us-east-1)
- `your-s3-bucket-name`: S3 bucket for agent caching
- `your-ecr-repo`: ECR repository name for container images

### S3 Bucket Setup

Create an S3 bucket for agent caching:

```bash
aws s3 mb s3://your-s3-bucket-name --region YOUR_REGION
```

## Architecture

### Agent V3 Features

The V3 agent includes:

1. **Weather Tool**: Get current weather for any city
2. **Stock Price Tool**: Retrieve real-time stock prices
3. **News Tool**: Fetch latest news articles
4. **S3 Caching**: Intelligent caching to reduce API calls

### Observability Stack

- **ADOT Auto-Instrumentation**: Complete trace capture
- **CloudWatch Logs**: Centralized logging with `/aws/spans` log group
- **X-Ray Integration**: Distributed tracing visualization
- **Transaction Search**: Pre-configured with 10% sampling rate

## Key Components

### ADOT Integration

The critical component for observability is the ADOT auto-instrumentation:

```dockerfile
CMD ["opentelemetry-instrument", "python", "agent.py"]
```

This enables automatic span generation for:
- Service-level operations
- Agent code execution
- Tool invocations
- External API calls

### Agent Code Structure

```python
from bedrock_agentcore_app import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def chat(message: str) -> str:
    # Agent logic with automatic tracing
    pass

@app.tool
def get_weather(city: str) -> str:
    # Tool implementation with S3 caching
    pass
```

## Testing

Test your deployed agent:

```python
import boto3

client = boto3.client('bedrock-agent-runtime', region_name='YOUR_REGION')

response = client.invoke_agent(
    agentId='your-agent-id',
    agentAliasId='TSTALIASID',
    sessionId='test-session',
    inputText='What is the weather in London?'
)
```

## Observability Features

### CloudWatch Dashboard

Access the observability dashboard:
```
https://console.aws.amazon.com/cloudwatch/home?region=YOUR_REGION#gen-ai-observability/agent-core
```

### Trace Hierarchy

Complete trace visibility:
```
AgentCore.Runtime.Invoke
├── POST /invocations
│   ├── execute_event_loop_cycle
│   │   ├── chat
│   │   │   ├── execute_tool (get_weather)
│   │   │   ├── S3 operations
│   │   │   └── External API calls
```

### Log Groups

Monitor logs in CloudWatch:
- `/aws/spans`: Trace and span data
- `/aws/lambda/your-agent-name`: Agent execution logs

## Security Best Practices

1. **IAM Roles**: Minimal required permissions
2. **S3 Bucket Policy**: Restrict access to agent cache prefix
3. **VPC Configuration**: Optional VPC deployment for enhanced security
4. **Encryption**: Enable S3 bucket encryption

## Troubleshooting

### Common Issues

1. **Missing Spans**: Ensure ADOT auto-instrumentation is enabled
2. **Permission Errors**: Verify IAM role permissions
3. **Container Issues**: Check ECR repository access
4. **S3 Access**: Confirm bucket exists and permissions are correct

### Debug Commands

```bash
# Check agent logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/your-agent"

# View traces
aws logs filter-log-events --log-group-name "/aws/spans" --start-time $(date -d '1 hour ago' +%s)000

# Test S3 access
aws s3 ls s3://your-s3-bucket-name/agent-cache/
```

## Comparison: CDK vs Terraform

Both implementations provide identical functionality:

| Feature | CDK | Terraform |
|---------|-----|-----------|
| ADOT Integration | ✅ | ✅ |
| S3 Caching | ✅ | ✅ |
| CloudWatch Logs | ✅ | ✅ |
| X-Ray Tracing | ✅ | ✅ |
| IAM Permissions | ✅ | ✅ |
| Container Deployment | ✅ | ✅ |

Choose based on your team's preference and existing infrastructure.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
