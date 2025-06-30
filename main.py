import pandas as pd
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import create_analyst_agent
import uvicorn

# Load environment variables from .env file
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("ERROR: OPENAI_API_KEY not found in .env file.")

# --- Data Loading ---
try:
    data_path = "data/sales_data_sample.csv"
    df = pd.read_csv(data_path)
except FileNotFoundError:
    raise FileNotFoundError(f"ERROR: The data file was not found at '{data_path}'. Please make sure it exists.")

# --- FastAPI Application ---
app = FastAPI(
    title="Automated Business Insights Agent",
    description="An API for querying business data using a natural language-powered autonomous agent.",
    version="1.0.0"
)


# Pydantic model for the request body to ensure type safety
class QueryRequest(BaseModel):
    question: str


@app.post("/query-agent/")
async def query_agent(request: QueryRequest):
    """
    Receives a natural language question, passes it to the agent,
    and returns the agent's final answer.
    """
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="Question field cannot be empty.")

    try:
        # We only need the final answer from the agent for the API response
        final_answer = "Could not determine the answer."

        # The agent_generator yields its step-by-step process.
        # We will loop through it to get the final result.
        agent_generator = create_analyst_agent(df, question)
        for step in agent_generator:
            if step['type'] == 'final_answer':
                final_answer = step['content']
                break  # Stop once we have the final answer

        return {"question": question, "answer": final_answer}

    except Exception as e:
        # This provides a more detailed error for debugging if something goes wrong
        raise HTTPException(status_code=500, detail=f"An error occurred in the agent: {str(e)}")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Business Insights Agent API. Please use the /docs endpoint to see the API documentation and test the /query-agent/ endpoint."}


# --- Running the App ---
if __name__ == "__main__":
    # This block allows you to run the app directly using `python main.py`
    # Uvicorn is a lightning-fast ASGI server.
    uvicorn.run(app, host="0.0.0.0", port=8000)