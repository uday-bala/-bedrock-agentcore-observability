#!/usr/bin/env python3
import aws_cdk as cdk
from my_agent_stack import MyAgentStack

app = cdk.App()

# Deploy to your account/region
env = cdk.Environment(
    account="426415991432",  # Your account ID
    region="us-west-2"       # Your region
)

MyAgentStack(
    app, 
    "MyAgentCoreStack",
    env=env,
    description="AgentCore agent with observability deployed via CDK"
)

app.synth()
