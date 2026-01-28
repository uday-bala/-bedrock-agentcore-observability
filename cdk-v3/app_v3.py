#!/usr/bin/env python3
import aws_cdk as cdk
from my_agent_v3_stack import MyAgentV3Stack

app = cdk.App()
MyAgentV3Stack(app, "MyAgentCoreV3Stack", 
    env=cdk.Environment(
        account="YOUR_ACCOUNT_ID",
        region="YOUR_REGION"
    )
)

app.synth()
