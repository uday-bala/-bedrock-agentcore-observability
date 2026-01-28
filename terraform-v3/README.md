# AgentCore V3 with Terraform

Complete Amazon Bedrock AgentCore V3 deployment using Terraform with full observability.

## 🏗 Architecture

- **Infrastructure**: Terraform
- **Agent Runtime**: BedrockAgentCore with Docker container
- **Observability**: ADOT auto-instrumentation + CloudWatch delivery
- **Tools**: Weather, Stock, News APIs with S3 caching

## 📁 File Structure

```
agentcore-terraform-v3/
├── providers.tf              # Terraform providers
├── variables.tf              # Input variables
├── iam.tf                   # IAM roles and policies
├── docker.tf                # Docker image build/push
├── agentcore.tf             # AgentCore runtime (via AWS CLI)
├── outputs.tf               # Output values
├── terraform.tfvars.example # Example variables
├── deploy.sh                # Deployment script
├── test_agent.py            # Test script
└── agent-code/
    ├── agent_v3.py          # Main agent code
    ├── requirements.txt     # Dependencies with ADOT
    └── Dockerfile           # Container with auto-instrumentation
```

## 🚀 Quick Deploy

### 1. Prerequisites
```bash
# Install required tools
terraform --version  # >= 1.0
docker --version
aws --version
```

### 2. Configure Variables
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 3. Create ECR Repository
```bash
aws ecr create-repository --repository-name agentcore-v3 --region us-west-2
```

### 4. Deploy
```bash
./deploy.sh
```

### 5. Test
```bash
python3 test_agent.py
```

## ⚙️ Configuration

### terraform.tfvars
```hcl
aws_region         = "us-west-2"
aws_account_id     = "YOUR_ACCOUNT_ID"
s3_bucket_name     = "YOUR_BUCKET_NAME"
agent_name         = "my_observability_agent_v3_tf"
ecr_repository_url = "YOUR_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/agentcore-v3"
```

## 🔍 Observability

Same observability features as CDK version:
- Complete ADOT auto-instrumentation
- Service-provided traces via CloudWatch delivery
- X-Ray integration with detailed spans
- CloudWatch GenAI Observability dashboard

## 🛠 Terraform Commands

```bash
# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply

# Destroy
terraform destroy

# View outputs
terraform output
```

## 📊 Outputs

- `agent_role_arn`: IAM role ARN
- `runtime_arn`: AgentCore runtime ARN
- `runtime_status`: Deployment status
- `observability_dashboard`: CloudWatch dashboard URL

## ⚠️ Limitations

- **No native BedrockAgentCore provider**: Uses AWS CLI via null_resource
- **Docker build in Terraform**: Consider CI/CD pipeline for production
- **State management**: Use remote state for team environments

## 🔄 Production Considerations

### Remote State
```hcl
terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "agentcore-v3/terraform.tfstate"
    region = "us-west-2"
  }
}
```

### CI/CD Integration
- Build/push images in CI pipeline
- Use image tags instead of `:latest`
- Separate Terraform apply from image builds

### Multi-Environment
- Use Terraform workspaces
- Environment-specific variable files
- Separate ECR repositories per environment

## 🆚 CDK vs Terraform

| Feature | CDK | Terraform |
|---------|-----|-----------|
| BedrockAgentCore Support | ✅ Native | ❌ AWS CLI workaround |
| Type Safety | ✅ TypeScript/Python | ❌ HCL |
| AWS Integration | ✅ Excellent | ✅ Good |
| Multi-Cloud | ❌ AWS only | ✅ Multi-cloud |
| Learning Curve | Medium | Low-Medium |

## 🔧 Troubleshooting

### Runtime Creation Fails
```bash
# Check AWS CLI permissions
aws bedrock-agentcore list-runtimes --region us-west-2

# Verify ECR image exists
aws ecr describe-images --repository-name agentcore-v3 --region us-west-2
```

### Docker Build Issues
```bash
# Build manually
cd agent-code
docker build --platform linux/arm64 -t test-agent .
```

### Terraform State Issues
```bash
# Import existing resources
terraform import aws_iam_role.agent_role ROLE_NAME

# Refresh state
terraform refresh
```

---

**Note**: This Terraform implementation provides the same functionality as the CDK version but uses AWS CLI for AgentCore resources until native Terraform provider support is available.
