from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool
import json
import random
import time
import os

# Initialize OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Set up tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter for AWS
otlp_exporter = OTLPSpanExporter(
    endpoint="https://otlp.us-west-2.amazonaws.com/v1/traces",
    headers={}
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI(title="Observability Agent", version="1.0.0")

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

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

# Initialize Strands agent with tools
model = BedrockModel(model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0")
strands_agent = Agent(
    model=model, 
    tools=[get_weather, get_stock_price],
    system_prompt="""You are a helpful assistant with access to weather and stock data.
    All your tool calls are fully traced for complete observability. You can see exactly 
    whether data came from cache or live APIs."""
)

class InvocationRequest(BaseModel):
    input: Dict[str, Any]

class InvocationResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    try:
        prompt = request.input.get("prompt", "")
        if not prompt:
            raise HTTPException(status_code=400, detail="No prompt found in input")
        
        print(f"🎯 Processing request: {prompt}")
        result = strands_agent(prompt)
        
        response = {
            "message": result.message['content'][0]['text'],
            "timestamp": datetime.utcnow().isoformat()
        }
        return InvocationResponse(output=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/ping")
async def ping():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
