#!/bin/bash

# Configuration - update these values
AWS_ACCOUNT_ID="123456789012"
AWS_REGION="us-east-1"
S3_BUCKET_NAME="my-agentcore-cache-bucket"

echo "Setting up prerequisites for AgentCore deployment..."

# Create S3 bucket for caching
echo "Creating S3 bucket: $S3_BUCKET_NAME"
aws s3 mb s3://$S3_BUCKET_NAME --region $AWS_REGION

# Enable versioning (optional but recommended)
aws s3api put-bucket-versioning \
    --bucket $S3_BUCKET_NAME \
    --versioning-configuration Status=Enabled

# Create agent-cache prefix
aws s3api put-object \
    --bucket $S3_BUCKET_NAME \
    --key agent-cache/ \
    --content-length 0

echo "S3 bucket setup complete!"

# For Terraform deployment, also create ECR repository
if [ "$1" = "terraform" ]; then
    echo "Creating ECR repository for Terraform deployment..."
    aws ecr create-repository \
        --repository-name agentcore-v3 \
        --region $AWS_REGION \
        --image-scanning-configuration scanOnPush=true
    
    echo "ECR repository created!"
fi

echo "Prerequisites setup complete!"
echo "Next steps:"
echo "1. Update terraform.tfvars with your actual values"
echo "2. Run ./deploy.sh (Terraform) or ./deploy-v3.sh (CDK)"
