from aws_cdk import Stack, CfnOutput
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk.aws_bedrock_agentcore_alpha import (
    Runtime, 
    AgentRuntimeArtifact
)
from constructs import Construct

class MyAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create execution role
        agent_role = iam.Role(
            self, "MyAgentRole",
            assumed_by=iam.ServicePrincipal(
                "bedrock-agentcore.amazonaws.com",
                conditions={
                    "StringEquals": {"aws:SourceAccount": self.account},
                    "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{self.region}:{self.account}:*"}
                }
            )
        )
        
        # Add permissions
        agent_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream", 
                "bedrock:Converse",
                "bedrock:ConverseStream"
            ],
            resources=["*"]
        ))
        
        agent_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream", 
                "logs:PutLogEvents"
            ],
            resources=["*"]
        ))
        
        # Create agent artifact with ARM64 platform
        agent_artifact = AgentRuntimeArtifact.from_asset(
            "./agent-code",
            platform=ecr_assets.Platform.LINUX_ARM64
        )
        
        # Deploy runtime (observability enabled by default)
        agent_runtime = Runtime(
            self, "MyObservabilityAgent",
            runtime_name="my_observability_agent",
            agent_runtime_artifact=agent_artifact,
            execution_role=agent_role,
            description="AgentCore agent with observability via CDK"
        )
        
        # Outputs
        runtime_arn = f"arn:aws:bedrock-agentcore:{self.region}:{self.account}:runtime/my_observability_agent"
        
        CfnOutput(self, "AgentArn", value=runtime_arn)
        CfnOutput(
            self, "ObservabilityDashboard",
            value=f"https://console.aws.amazon.com/cloudwatch/home?region={self.region}#gen-ai-observability/agent-core"
        )
