# # Step1: Setup FastAPI backend
# from fastapi import FastAPI
# from pydantic import BaseModel
# import uvicorn

# from ai_agent import graph, SYSTEM_PROMPT, parse_response

# app = FastAPI()

# # Step2: Receive and validate request from Frontend
# class Query(BaseModel):
#     message: str



# @app.post("/ask")
# async def ask(query: Query):
#     inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
#     #inputs = {"messages": [("user", query.message)]}
#     stream = graph.stream(inputs, stream_mode="updates")
#     tool_called_name, final_response = parse_response(stream)

#     # Step3: Send response to the frontend
#     return {"response": final_response,
#             "tool_called": tool_called_name}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







# Step 1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Import the new Ollama-based agent
from ai_agent import run_agent

app = FastAPI(title="SafeSpace AI Mental Health Backend")


# Step 2: Request schema from frontend
class Query(BaseModel):
    message: str


# Step 3: Main API endpoint
@app.post("/ask")
async def ask(query: Query):
    """
    Receives a user message, routes it through the AI agent,
    and returns the response along with the tool used.
    """
    tool_called, response = run_agent(query.message)

    return {
        "response": response,
        "tool_called": tool_called
    }


# Step 4: Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
