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
        print(f"  ✅ Retrieved weather from CACHE (traced)")
        return {
            "city": city,
            "temp": "72F",
            "source": "cache",
            "trace_info": "Cache hit - fully traced"
        }
    else:
        print(f"  🌐 Calling live weather API...")
        time.sleep(0.5)  # Simulate API latency
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
        print(f"  ✅ Retrieved stock from CACHE (traced)")
        return {
            "symbol": symbol,
            "price": "$155",
            "source": "cache",
            "trace_info": "Cache hit - fully traced"
        }
    else:
        print(f"  🌐 Calling live stock API...")
        time.sleep(0.3)
        return {
            "symbol": symbol,
            "price": f"${random.randint(300, 310)}",
            "source": "live_api",
            "trace_info": "Live API call - fully traced"
        }

@app.entrypoint
def invoke_agent(payload):
    """Main agent entrypoint with complete observability."""
    model = BedrockModel(model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0")
    agent = Agent(
        model=model, 
        tools=[get_weather, get_stock_price],
        system_prompt="""You are a helpful assistant with access to weather and stock data.
        All your tool calls are fully traced for complete observability. You can see exactly 
        whether data came from cache or live APIs."""
    )
    
    query = payload.get("prompt", payload.get("query", ""))
    print(f"🎯 Processing request: {query}")
    
    result = agent(query)
    return result.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
