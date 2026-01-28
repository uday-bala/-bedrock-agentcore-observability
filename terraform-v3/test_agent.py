#!/usr/bin/env python3
"""
Test the deployed AgentCore agent V3 with Terraform
"""

import boto3
import json
import uuid
import sys

def test_agent():
    # Hardcoded runtime ARN for haytug account
    runtime_arn = "arn:aws:bedrock-agentcore:YOUR_REGION:YOUR_ACCOUNT_ID:runtime/my_observability_agent_v3_tf_8e75bf3b-ArNhf57cti"

    client = boto3.client('bedrock-agentcore', region_name='YOUR_REGION')
    
    test_queries = [
        "What's the weather in Seattle?",
        "Get me the AMZN stock price", 
        "What's the latest technology news?",
        "Give me weather, stock, and news updates"
    ]
    
    print(f"🎯 Testing agent: {runtime_arn}")
    
    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        print("=" * 50)
        
        try:
            session_id = f"test-session-tf-{uuid.uuid4().hex}"
            payload = json.dumps({"prompt": query})
            
            response = client.invoke_agent_runtime(
                agentRuntimeArn=runtime_arn,
                runtimeSessionId=session_id,
                payload=payload
            )
            
            response_body = response['response'].read()
            response_data = json.loads(response_body)
            print(f"✅ Response: {response_data}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_agent()
