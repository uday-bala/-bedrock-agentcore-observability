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
        bucket_name = "tracing-test-bucket-YOUR_ACCOUNT_ID"
        response = s3.get_object(Bucket=bucket_name, Key='agent-cache/weather.json')
        data = json.loads(response['Body'].read())
        data['source'] = 'cache'
        data['trace_info'] = 'S3 cache hit - V3 fully traced'
        print(f"  ✅ Retrieved weather from CACHE (V3 traced)")
        return data
    else:
        print(f"  🌐 Calling live weather API...")
        time.sleep(0.5)
        return {
            "city": city,
            "temp": f"{random.randint(60, 80)}F",
            "source": "live_api",
            "trace_info": "Live API call - V3 fully traced"
        }

@tool
def get_stock_price(symbol: str = "AMZN") -> dict:
    """Get stock price with cache vs API decision."""
    print(f"📈 Getting stock price for {symbol}...")
    
    # 70% cache, 30% live API
    use_cache = random.choices([True, False], weights=[0.7, 0.3])[0]
    
    if use_cache:
        s3 = boto3.client('s3')
        bucket_name = "tracing-test-bucket-YOUR_ACCOUNT_ID"
        response = s3.get_object(Bucket=bucket_name, Key='agent-cache/stock.json')
        data = json.loads(response['Body'].read())
        data['source'] = 'cache'
        data['trace_info'] = 'S3 cache hit - V3 fully traced'
        print(f"  ✅ Retrieved stock from CACHE (V3 traced)")
        return data
    else:
        print(f"  🌐 Calling live stock API...")
        time.sleep(0.3)
        return {
            "symbol": symbol,
            "price": f"${random.randint(300, 310)}",
            "source": "live_api",
            "trace_info": "Live API call - V3 fully traced"
        }

@tool
def get_news(topic: str = "technology") -> dict:
    """Get news headlines - V3 new feature."""
    print(f"📰 Getting news for {topic}...")
    time.sleep(0.2)
    
    headlines = [
        f"Breaking: {topic.title()} innovation announced",
        f"Latest {topic} trends for 2026",
        f"Expert analysis on {topic} market"
    ]
    
    return {
        "topic": topic,
        "headlines": random.sample(headlines, 2),
        "source": "news_api",
        "trace_info": "V3 news feature - fully traced"
    }

# Initialize Strands agent with tools
model = BedrockModel(model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0")
strands_agent = Agent(
    model=model, 
    tools=[get_weather, get_stock_price, get_news],
    system_prompt="""You are a helpful assistant V3 with access to weather, stock, and news data.
    All your tool calls are fully traced for complete observability. You have enhanced capabilities in V3."""
)

@app.entrypoint
def invoke_agent(payload):
    """Main agent entrypoint with complete V3 observability."""
    prompt = payload.get("prompt", payload.get("query", ""))
    print(f"🎯 V3 Agent processing: {prompt}")
    
    result = strands_agent(prompt)
    return result.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
