#!/bin/bash
set -e

echo "🐳 Building CDK Docker image..."
docker build -f Dockerfile.cdk -t my-cdk-deploy .

echo "✅ CDK Docker image built successfully!"

echo "🚀 Bootstrapping CDK (if needed)..."
docker run --rm \
  -v ~/.aws:/root/.aws \
  -v $(pwd):/app \
  -v /var/run/docker.sock:/var/run/docker.sock \
  my-cdk-deploy cdk bootstrap

echo "🚀 Deploying AgentCore stack..."
docker run --rm \
  -v ~/.aws:/root/.aws \
  -v $(pwd):/app \
  -v /var/run/docker.sock:/var/run/docker.sock \
  my-cdk-deploy cdk deploy MyAgentCoreStack --require-approval never

echo "✅ AgentCore agent deployed with observability!"
echo "🔍 Check CloudWatch Gen AI Observability Dashboard for traces"
