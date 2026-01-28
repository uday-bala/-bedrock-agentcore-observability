#!/usr/bin/env python3
"""
Test the deployed AgentCore agent V2 with enhanced observability
"""

import boto3
import json
import uuid

def test_agent_v2():
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')
    
    test_queries = [
        "What's the weather in Seattle?",
        "Get me the AMZN stock price", 
        "What's the weather and stock price?"
    ]
    
    # Note: Need to find the actual runtime ARN with suffix
    runtime_arn = "arn:aws:bedrock-agentcore:us-west-2:426415991432:runtime/my_observability_agent_v2-NRkzfG7Wws"
    
    for query in test_queries:
        print(f"\n🧪 Testing V2: {query}")
        print("=" * 50)
        
        try:
            # Generate a unique session ID (33+ characters required)
            session_id = f"test-session-v2-{uuid.uuid4().hex}"
            payload = json.dumps({"prompt": query})
            
            response = client.invoke_agent_runtime(
                agentRuntimeArn=runtime_arn,
                runtimeSessionId=session_id,
                payload=payload,
                qualifier="DEFAULT"
            )
            
            response_body = response['response'].read()
            response_data = json.loads(response_body)
            print(f"✅ Response: {response_data}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_agent_v2()
