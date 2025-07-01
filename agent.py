import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


def create_analyst_agent(df: pd.DataFrame, question: str):
    """
    Creates and runs a pre-built, robust LangChain agent for pandas DataFrame analysis.

    This function leverages the battle-tested `create_pandas_dataframe_agent` from
    LangChain, which handles all the complexities of the agent loop, tool creation,
    and response parsing internally.

    Args:
        df (pd.DataFrame): The DataFrame to be analyzed.
        question (str): The user's question about the DataFrame.

    Returns:
        str: The final, human-readable answer from the agent.
    """
    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4.1-mini")

    # Create the LangChain agent executor
    # This single function creates the agent, the tool, the prompt, and the loop.
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True},
        allow_dangerous_code=True  # Add this line to opt-in
    )

    # Invoke the agent with the user's question
    # The agent will now run its entire multi-step process internally
    response = agent.invoke({"input": question})

    # The response dictionary contains the final answer in the 'output' key
    return response.get("output", "The agent did not return a valid output.")