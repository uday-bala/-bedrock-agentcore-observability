# AgentCore V3 with Complete Observability

This repository contains a complete Amazon Bedrock AgentCore V3 deployment with full observability using AWS CDK. The agent includes weather, stock, and news tools with comprehensive tracing and monitoring.

## 🎯 What This Provides

- **Complete Observability**: ADOT auto-instrumentation for detailed tracing
- **Service-Level Spans**: AWS service-provided traces via CloudWatch delivery
- **Agent Code Spans**: Tool executions, LLM calls, S3 operations
- **Enhanced Tools**: Weather, stock price, and news retrieval
- **Production Ready**: Proper IAM permissions, X-Ray integration, CloudWatch logs

## 📁 Required Files

```
my-agentcore-cdk/
├── app_v3.py                    # CDK app entry point
├── my_agent_v3_stack.py         # CDK stack definition
├── deploy-v3.sh                 # Deployment script
├── requirements.txt             # CDK dependencies
├── cdk.json                     # CDK configuration
├── Dockerfile.cdk               # CDK deployment container
└── agent-code-v3/
    ├── agent_v3.py              # Main agent code
    ├── requirements.txt         # Agent dependencies (includes ADOT)
    ├── Dockerfile               # Agent container with auto-instrumentation
    └── test-v3.py               # Test script
```

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured with appropriate permissions
- Docker installed and running
- Admin or equivalent AWS permissions

### 1. Clone/Copy Files
Copy all required files to your deployment environment.

### 2. Update Configuration
Edit the following files for your environment:

**app_v3.py** - Update account ID:
```python
env=cdk.Environment(
    account="YOUR_ACCOUNT_ID",  # Change this
    region="us-west-2"
)
```

**my_agent_v3_stack.py** - Update S3 bucket (lines 47-52):
```python
resources=[
    "arn:aws:s3:::YOUR_BUCKET_NAME",      # Change this
    "arn:aws:s3:::YOUR_BUCKET_NAME/*"     # Change this
]
```

**agent_v3.py** - Update S3 bucket (lines 18, 42):
```python
bucket_name = "YOUR_BUCKET_NAME"  # Change this
```

### 3. Prepare S3 Cache (Optional)
Create test cache files in your S3 bucket:

```bash
# Create cache directory structure
aws s3 cp weather.json s3://YOUR_BUCKET_NAME/agentcore_test/cache/weather.json
aws s3 cp stock.json s3://YOUR_BUCKET_NAME/agentcore_test/cache/stock.json
```

**weather.json**:
```json
{"city": "Seattle", "temp": "72F", "conditions": "Partly Cloudy"}
```

**stock.json**:
```json
{"symbol": "AMZN", "price": "$150", "change": "+2.5%"}
```

### 4. Build CDK Container
```bash
docker build -f Dockerfile.cdk -t my-cdk-deploy .
```

### 5. Deploy
```bash
chmod +x deploy-v3.sh
./deploy-v3.sh
```

### 6. Test
```bash
# Update runtime ARN in test-v3.py with actual deployed ARN
python3 test-v3.py
```

## 🔍 Observability Features

### What You'll See in CloudWatch GenAI Observability:
- **AgentCore.Runtime.Invoke** - AWS service span (2-3s)
- **POST /invocations** - HTTP endpoint span (2-3s)
- **execute_event_loop_cycle** - Agent processing cycles (1-2s)
- **chat** - LLM interactions with token counts (0.5-1s)
- **execute_tool** - Individual tool executions (0.1-0.5s)
- **S3.GetObject** - S3 cache retrievals (0.1s)

### Key Observability Components:
1. **ADOT Auto-Instrumentation**: `opentelemetry-instrument python agent_v3.py`
2. **CloudWatch Delivery**: Automatic service-provided traces
3. **X-Ray Integration**: Complete trace correlation
4. **Structured Logging**: Runtime logs in CloudWatch

## 🛠 Agent Capabilities

### Tools Available:
- **get_weather(city)**: Weather information with cache/API logic
- **get_stock_price(symbol)**: Stock prices with cache/API logic  
- **get_news(topic)**: News headlines (V3 enhancement)

### Sample Queries:
```python
"What's the weather in Seattle?"
"Get me the AMZN stock price"
"What's the latest technology news?"
"Give me weather, stock, and news updates"
```

## 📊 Monitoring & Troubleshooting

### Check Deployment Status:
```bash
aws cloudformation describe-stacks --stack-name MyAgentCoreV3Stack --region us-west-2
```

### View Runtime Logs:
```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/bedrock-agentcore/runtimes/my_observability_agent_v3" --region us-west-2
```

### Check Spans:
```bash
aws logs get-log-events --log-group-name "aws/spans" --log-stream-name "default" --region us-west-2
```

### Enable Console Tracing:
1. Go to Amazon Bedrock Console → AgentCore
2. Find your agent: `my_observability_agent_v3`
3. Enable tracing toggle

## 🔧 Key Configuration Details

### ADOT Dependencies (agent-code-v3/requirements.txt):
```
strands-agents[otel]
bedrock-agentcore
boto3
aws-opentelemetry-distro>=0.10.0  # Critical for observability
```

### Auto-Instrumentation (agent-code-v3/Dockerfile):
```dockerfile
CMD ["opentelemetry-instrument", "python", "agent_v3.py"]  # Critical for spans
```

### IAM Permissions:
- Bedrock model invocation
- S3 bucket access
- CloudWatch logs
- X-Ray tracing

## 🚨 Common Issues

### No Spans Visible:
- Ensure tracing is enabled in Bedrock console
- Verify ADOT dependency is installed
- Check auto-instrumentation command in Dockerfile

### Permission Errors:
- Verify IAM role has required permissions
- Check S3 bucket access
- Ensure account ID is correct in app_v3.py

### Deployment Failures:
- Verify Docker is running
- Check CDK container is built
- Ensure AWS credentials are configured

## 📈 Performance Expectations

- **Cold Start**: 2-3 seconds for first invocation
- **Warm Invocations**: 1-2 seconds
- **Tool Execution**: 0.1-0.5 seconds per tool
- **S3 Cache Hits**: ~0.1 seconds
- **Live API Calls**: 0.3-0.5 seconds

## 🔄 Updates & Maintenance

### Update Agent Code:
1. Modify `agent_v3.py`
2. Run `./deploy-v3.sh`
3. Test with updated functionality

### Add New Tools:
1. Add `@tool` decorated function in `agent_v3.py`
2. Update tools list in Agent initialization
3. Redeploy

### Scale Considerations:
- Monitor CloudWatch costs for high-volume tracing
- Adjust X-Ray sampling rates if needed
- Consider log retention policies

## 📚 Additional Resources

- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html)
- [CloudWatch GenAI Observability](https://console.aws.amazon.com/cloudwatch/home#gen-ai-observability)
- [ADOT Documentation](https://aws-otel.github.io/docs/)
- [Strands Framework](https://github.com/aws-samples/strands-agents)

## 🏷 Version Info

- **Agent Version**: V3
- **CDK Version**: 2.236.0+
- **Python Version**: 3.11
- **Platform**: linux/arm64
- **ADOT Version**: 0.14.2+

---

**Note**: This setup provides production-ready observability without using the AgentCore starter toolkit. All observability features are manually configured using CDK and ADOT auto-instrumentation.
