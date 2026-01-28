#!/usr/bin/env python3
"""
Test the deployed AgentCore agent via Docker
"""

import boto3
import json
import uuid

def test_agent():
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')
    
    test_queries = [
        "What's the weather in Seattle?",
        "Get me the AMZN stock price", 
        "What's the weather and stock price?"
    ]
    
    runtime_arn = "arn:aws:bedrock-agentcore:us-west-2:426415991432:runtime/my_observability_agent-9bcVLiDHjj"
    
    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        print("=" * 50)
        
        try:
            # Generate a unique session ID (33+ characters required)
            session_id = f"test-session-{uuid.uuid4().hex}"
            payload = json.dumps({"input": {"prompt": query}})
            
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
    test_agent()
