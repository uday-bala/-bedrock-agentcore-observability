#!/bin/bash
set -e

echo "🚀 Deploying AgentCore V3 with Terraform to haytug account..."

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found. Copy terraform.tfvars.example and update values."
    exit 1
fi

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Plan deployment
echo "📋 Planning deployment..."
terraform plan

# Apply deployment
echo "🚀 Applying deployment..."
terraform apply -auto-approve

echo "✅ AgentCore V3 deployed with Terraform to haytug account!"
echo "🔍 Check outputs for runtime ARN and dashboard URL"
terraform output
