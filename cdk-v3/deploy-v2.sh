#!/bin/bash
set -e

echo "🚀 Deploying AgentCore V2 stack..."
docker run --rm \
  -v ~/.aws:/root/.aws \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/app \
  -w /app \
  my-cdk-deploy \
  cdk deploy MyAgentCoreV2Stack --app "python3 app_v2.py" --require-approval never

echo "✅ AgentCore agent V2 deployed with enhanced observability!"
echo "🔍 Check CloudWatch Gen AI Observability Dashboard for detailed traces"
