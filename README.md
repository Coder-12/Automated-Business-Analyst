# Autonomous Business Insights Agent

This project features an autonomous AI agent that empowers users to perform complex data analysis on business datasets using only natural language commands. The agent acts as an automated data analyst, leveraging a powerful Large Language Model (LLM) and the LangChain framework to translate plain English questions into executable Python (`pandas`) code to find and present insights.

This project was built with a focus on reliability and professional engineering practices, using the battle-tested `create_pandas_dataframe_agent` from LangChain to ensure robust, multi-step reasoning.

## Core Features

-   **Natural Language to Code**: Translates complex questions like "was revenue higher in March than January?" into a series of `pandas` commands.
-   **Robust Agentic Workflow**: Powered by LangChain's agent executor, which reliably handles multi-step reasoning, self-correction, and tool execution.
-   **Secure by Design**: Acknowledges and correctly handles LangChain's built-in security guardrails for executing Python code.
-   **API-Ready**: The entire application is served via a FastAPI endpoint, making it a self-contained service ready for integration into other applications or dashboards.
-   **Containerized & Portable**: Includes a `Dockerfile` for easy packaging and deployment, ensuring the application runs consistently in any environment.

## Project Structure

```
/automated-business-analyst/
|
├── 📂 data/
|   └── sales_data_sample.csv  # Sample data for analysis
|
├── 📄 .env                   # For storing API keys (ignored by git)
├── 📄 .gitignore
├── 📄 agent.py                # Core logic using LangChain's pandas agent
├── 📄 Dockerfile              # Instructions for building the container
├── 📄 main.py                 # FastAPI application to serve the agent
├── 📄 README.md
└── 📄 requirements.txt        # Project dependencies
```

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/automated-business-analyst.git
    cd automated-business-analyst
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    -   Create a file named `.env` in the root directory.
    -   Open the `.env` file and add your OpenAI API key:
        ```
        OPENAI_API_KEY="your_api_key_here"
        ```

## How to Run

You can run the application in two ways:

#### 1. For Local Development (with Uvicorn)

This method is best for quick testing and development.

```bash
uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000`.

#### 2. Using Docker (for Production & Portability)

This method packages the application into a self-contained container. Make sure you have Docker installed and running.

```bash
# 1. Build the Docker image
docker build -t business-analyst-agent .

# 2. Run the Docker container
docker run -d -p 8000:8000 --env-file .env business-analyst-agent
```

## How to Query the Agent

Once the server is running (using either method), you can interact with the agent via its API.

1.  Open your web browser and navigate to the interactive documentation:
    **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

2.  Expand the `POST /query` endpoint and click "Try it out".

3.  In the "Request body" text box, enter your question in JSON format.

### Example Queries

-   **Simple Aggregation:**
    ```json
    { "question": "What is the total revenue for all sales?" }
    ```
-   **Grouping & Ranking:**
    ```json
    { "question": "What were the top 3 products by total revenue?" }
    ```
-   **Filtering & Context:**
    ```json
    { "question": "For the 'Electronics' category only, what was the total number of units sold?" }
    ```
-   **Multi-Step Reasoning:**
    ```json
    { "question": "Was the total revenue in March higher than in January?" }
    ```

4.  Click "Execute" to see the agent's response. The agent's step-by-step reasoning will be printed in the server console (thanks to `verbose=True`).