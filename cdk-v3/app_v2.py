#!/usr/bin/env python3
import aws_cdk as cdk
from my_agent_v2_stack import MyAgentV2Stack

app = cdk.App()
MyAgentV2Stack(app, "MyAgentCoreV2Stack", 
    env=cdk.Environment(
        account="426415991432",
        region="us-west-2"
    )
)

app.synth()
