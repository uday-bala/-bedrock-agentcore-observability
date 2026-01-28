from bedrock_agentcore.runtime import BedrockAgentCoreApp
import json

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke_agent(payload):
    """Simple test agent."""
    try:
        prompt = payload.get("prompt", payload.get("query", "Hello"))
        return f"Echo: {prompt}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()
