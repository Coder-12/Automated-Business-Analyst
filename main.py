import pandas as pd
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import create_analyst_agent  # Our new agent function

# Load environment variables
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in .env file.")

# --- Data Loading (Global) ---
try:
    DATA_PATH = "data/sales_data_sample.csv"
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Data file not found at '{DATA_PATH}'.")

# --- FastAPI App ---
app = FastAPI(
    title="Automated Business Insights Agent",
    description="An API for an autonomous agent that answers questions about business data."
)


class QueryRequest(BaseModel):
    question: str


@app.post("/query", summary="Ask a question to the data agent")
async def query_agent(request: QueryRequest):
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # Call the new agent function. It's no longer a generator.
        # It directly returns the final answer.
        final_answer = create_analyst_agent(df, question)
        return {"answer": final_answer}

    except Exception as e:
        # Catch any unexpected errors during agent execution
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/", summary="Root endpoint for health check")
async def read_root():
    return {"status": "Automated Business Analyst API is running."}

# To run: uvicorn main:app --reload