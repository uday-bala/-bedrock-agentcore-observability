#!/usr/bin/env python3
"""Test script to invoke the deployed AgentCore agent."""

import boto3
import json

def test_agent():
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')
    
    # Test scenarios
    test_queries = [
        "What's the weather in Seattle?",
        "Get me the AMZN stock price", 
        "What's the weather and stock price?"
    ]
    
    runtime_arn = "arn:aws:bedrock-agentcore:us-west-2:426415991432:runtime/my-observability-agent"
    
    for query in test_queries:
        print(f"\n🧪 Testing: {query}")
        print("=" * 50)
        
        try:
            response = client.invoke_agent_runtime(
                runtimeArn=runtime_arn,
                payload=json.dumps({"query": query})
            )
            
            result = json.loads(response['payload'])
            print(f"✅ Response: {result}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_agent()
