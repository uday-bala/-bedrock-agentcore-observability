from aws_cdk import Stack, CfnOutput
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk.aws_bedrock_agentcore_alpha import (
    Runtime, 
    AgentRuntimeArtifact
)
from constructs import Construct

class MyAgentV3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create execution role with enhanced permissions
        agent_role = iam.Role(
            self, "MyAgentV3Role",
            assumed_by=iam.ServicePrincipal(
                "bedrock-agentcore.amazonaws.com",
                conditions={
                    "StringEquals": {"aws:SourceAccount": self.account},
                    "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{self.region}:{self.account}:*"}
                }
            )
        )
        
        # Bedrock permissions
        agent_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream", 
                "bedrock:Converse",
                "bedrock:ConverseStream"
            ],
            resources=["*"]
        ))
        
        # CloudWatch permissions
        agent_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream", 
                "logs:PutLogEvents"
            ],
            resources=["*"]
        ))
        
        # S3 permissions for cache access
        agent_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            resources=[
                "arn:aws:s3:::tracing-test-bucket-YOUR_ACCOUNT_ID",
                "arn:aws:s3:::tracing-test-bucket-YOUR_ACCOUNT_ID/agent-cache/*"
            ]
        ))
        
        # X-Ray permissions for detailed tracing
        agent_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords"
            ],
            resources=["*"]
        ))
        
        # Create agent artifact
        agent_artifact = AgentRuntimeArtifact.from_asset(
            "./agent-code-v3",
            platform=ecr_assets.Platform.LINUX_ARM64
        )
        
        # Deploy runtime with enhanced observability
        agent_runtime = Runtime(
            self, "MyObservabilityAgentV3",
            runtime_name="my_observability_agent_v3",
            agent_runtime_artifact=agent_artifact,
            execution_role=agent_role,
            description="AgentCore agent v3 with enhanced observability and news tool"
        )
        
        # Outputs
        runtime_arn = f"arn:aws:bedrock-agentcore:{self.region}:{self.account}:runtime/my_observability_agent_v3"
        
        CfnOutput(self, "AgentV3Arn", value=runtime_arn)
        CfnOutput(
            self, "ObservabilityDashboard",
            value=f"https://console.aws.amazon.com/cloudwatch/home?region=YOUR_REGION#gen-ai-observability/agent-core"
        )
