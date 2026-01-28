from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import json
import random
import time
import boto3
import os

# Configure strands observability environment
os.environ["OTEL_SERVICE_NAME"] = "my_observability_agent_v2"
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "service.name=my_observability_agent_v2"

# Import strands after setting environment
from strands import Agent
from strands.models import BedrockModel
from strands.tools import tool

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
    endpoint="https://otlp.us-west-2.amazonaws.com/v1/traces"
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI(title="Observability Agent", version="1.0.0")

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@tool
def get_weather(city: str = "Seattle") -> dict:
    """Get weather information with cache vs API decision."""
    with tracer.start_as_current_span("get_weather") as span:
        span.set_attribute("city", city)
        print(f"🌤️ Getting weather for {city}...")
        
        # 70% cache, 30% live API
        use_cache = random.choices([True, False], weights=[0.7, 0.3])[0]
        span.set_attribute("cache_hit", use_cache)
        
        if use_cache:
            span.set_attribute("data_source", "s3_cache")
            s3 = boto3.client('s3')
            bucket_name = "us-west-2-balakriu"
            response = s3.get_object(Bucket=bucket_name, Key='agentcore_test/cache/weather.json')
            data = json.loads(response['Body'].read())
            data['source'] = 'cache'
            data['trace_info'] = 'S3 cache hit - fully traced'
            print(f"  ✅ Retrieved weather from CACHE (traced)")
            return data
        else:
            span.set_attribute("data_source", "live_api")
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
    with tracer.start_as_current_span("get_stock_price") as span:
        span.set_attribute("symbol", symbol)
        print(f"📈 Getting stock price for {symbol}...")
        
        # 70% cache, 30% live API
        use_cache = random.choices([True, False], weights=[0.7, 0.3])[0]
        span.set_attribute("cache_hit", use_cache)
        
        if use_cache:
            span.set_attribute("data_source", "s3_cache")
            s3 = boto3.client('s3')
            bucket_name = "us-west-2-balakriu"
            response = s3.get_object(Bucket=bucket_name, Key='agentcore_test/cache/stock.json')
            data = json.loads(response['Body'].read())
            data['source'] = 'cache'
            data['trace_info'] = 'S3 cache hit - fully traced'
            print(f"  ✅ Retrieved stock from CACHE (traced)")
            return data
        else:
            span.set_attribute("data_source", "live_api")
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
    whether data came from S3 cache or live APIs."""
)

class InvocationRequest(BaseModel):
    input: Dict[str, Any]

class InvocationResponse(BaseModel):
    output: Dict[str, Any]

@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    with tracer.start_as_current_span("invoke_agent") as span:
        try:
            prompt = request.input.get("prompt", "")
            if not prompt:
                raise HTTPException(status_code=400, detail="No prompt found in input")
            
            span.set_attribute("prompt", prompt)
            print(f"🎯 Processing request: {prompt}")
            result = strands_agent(prompt)
            
            response = {
                "message": result.message['content'][0]['text'],
                "timestamp": datetime.utcnow().isoformat()
            }
            return InvocationResponse(output=response)
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/ping")
async def ping():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
