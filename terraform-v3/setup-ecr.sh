#!/bin/bash
set -e

echo "🐳 Setting up ECR repository and pushing Docker image..."

# Variables
ECR_REPO_NAME="agentcore-v3"
ECR_URI="YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/agentcore-v3"
AWS_REGION="YOUR_REGION"

# Create ECR repository if it doesn't exist
echo "📦 Creating ECR repository..."
aws ecr create-repository \
    --repository-name $ECR_REPO_NAME \
    --region $AWS_REGION \
    --profile haytug-test-developer_v2 || echo "Repository may already exist"

# Get ECR login token
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION --profile haytug-test-developer_v2 | \
    docker login --username AWS --password-stdin $ECR_URI

# Build Docker image
echo "🏗️ Building Docker image..."
docker build -t $ECR_REPO_NAME ./agent-code/

# Tag image for ECR
echo "🏷️ Tagging image..."
docker tag $ECR_REPO_NAME:latest $ECR_URI:latest

# Push image to ECR
echo "⬆️ Pushing image to ECR..."
docker push $ECR_URI:latest

echo "✅ Docker image pushed to ECR successfully!"
echo "📍 Image URI: $ECR_URI:latest"
