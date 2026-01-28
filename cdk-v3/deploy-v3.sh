#!/bin/bash
set -e

echo "🚀 Deploying AgentCore V3 stack to haytug account..."
docker run --rm \
  -v ~/.aws:/root/.aws \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/app \
  -w /app \
  -e AWS_PROFILE=haytug-test-developer_v2 \
  my-cdk-deploy \
  cdk deploy MyAgentCoreV3Stack --app "python3 app_v3.py" --require-approval never --profile haytug-test-developer_v2

echo "✅ AgentCore agent V3 deployed to haytug account with enhanced observability!"
echo "🔍 Check CloudWatch Gen AI Observability Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=YOUR_REGION#gen-ai-observability/agent-core"
