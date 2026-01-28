from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool
import boto3
import json
import random
import time

app = BedrockAgentCoreApp()

@tool
def get_weather(city: str = "Seattle") -> dict:
    """Get weather information with cache vs API decision."""
    print(f"🌤️ Getting weather for {city}...")
    
    # 70% cache, 30% live API
    use_cache = random.choices([True, False], weights=[0.7, 0.3])[0]
    
    if use_cache:
        s3 = boto3.client('s3')
        bucket_name = "us-west-2-balakriu"
        response = s3.get_object(Bucket=bucket_name, Key='agentcore_test/cache/weather.json')
        data = json.loads(response['Body'].read())
        data['source'] = 'cache'
        data['trace_info'] = 'S3 cache hit - fully traced'
        print(f"  ✅ Retrieved weather from CACHE (traced)")
        return data
    else:
        print(f"  🌐 Calling live weather API...")
        time.sleep(0.5)
        return {
            "city": city,
            "temp": f"{random.randint(60, 80)}F",
            "source": "live_api",
            "trace_info": "Live API call - fully traced"
        }

@tool
def get_stock_price(symbol: str = "AMZN") -> dict:
    """Get stock price with cache vs API decision."""
    print(f"📈 Getting stock price for {symbol}...")
    
    # 70% cache, 30% live API
    use_cache = random.choices([True, False], weights=[0.7, 0.3])[0]
    
    if use_cache:
        s3 = boto3.client('s3')
        bucket_name = "us-west-2-balakriu"
        response = s3.get_object(Bucket=bucket_name, Key='agentcore_test/cache/stock.json')
        data = json.loads(response['Body'].read())
        data['source'] = 'cache'
        data['trace_info'] = 'S3 cache hit - fully traced'
        print(f"  ✅ Retrieved stock from CACHE (traced)")
        return data
    else:
        print(f"  🌐 Calling live stock API...")
        time.sleep(0.3)
        return {
            "symbol": symbol,
            "price": f"${random.randint(300, 310)}",
            "source": "live_api",
            "trace_info": "Live API call - fully traced"
        }

# Initialize Strands agent with tools
model = BedrockModel(model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0")
strands_agent = Agent(
    model=model, 
    tools=[get_weather, get_stock_price],
    system_prompt="""You are a helpful assistant with access to weather and stock data.
    All your tool calls are fully traced for complete observability."""
)

@app.entrypoint
def invoke_agent(payload):
    """Main agent entrypoint with complete observability."""
    prompt = payload.get("prompt", payload.get("query", ""))
    print(f"🎯 Processing request: {prompt}")
    
    result = strands_agent(prompt)
    return result.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
