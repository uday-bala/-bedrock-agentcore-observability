#!/bin/bash

# Install CDK dependencies
python3 -m pip install -r requirements.txt

# Bootstrap CDK (run once per account/region)
cdk bootstrap

# Deploy the stack
cdk deploy MyAgentCoreStack --require-approval never

echo "✅ AgentCore agent deployed with observability!"
echo "🔍 Check CloudWatch Gen AI Observability Dashboard for traces"
