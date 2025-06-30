import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from io import StringIO
from tools import python_repl_tool


def get_dataframe_info(df: pd.DataFrame) -> str:
    """Returns the head and info of a DataFrame as a string."""
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    return f"DataFrame Head:\n{df.head().to_string()}\n\nDataFrame Info:\n{info_str}"


def create_analyst_agent(df: pd.DataFrame, question: str, model_name: str = "gpt-4-turbo"):
    """
    Creates and runs a data analyst agent to answer a question about a DataFrame.

    This function orchestrates the agent's thinking process, including the
    self-correction loop.

    Args:
        df (pd.DataFrame): The DataFrame to be analyzed.
        question (str): The user's question about the DataFrame.
        model_name (str): The name of the OpenAI model to use.

    Yields:
        dict: A dictionary containing the step-by-step process of the agent.
    """
    llm = ChatOpenAI(temperature=0, model_name=model_name)

    # Get DataFrame schema for the prompt
    df_schema = get_dataframe_info(df)

    # System prompt defines the agent's persona, tools, and rules
    system_prompt_template = """
    You are an expert Python data analyst. You are given a pandas DataFrame named `df` and a user question.
    Your goal is to answer the user's question by generating and executing Python code.

    YOU HAVE ONE TOOL:
    - `python_repl_tool(code: str)`: Executes Python code and returns the output or error. Use this tool to explore the DataFrame and find the answer.

    THE DATAFRAME `df` has the following schema:
    {df_schema}

    YOUR WORKFLOW:
    1. **THOUGHT**: Analyze the user's question and the DataFrame schema. Decide what code you need to write to answer the question.
    2. **ACTION**: Write the Python code to be executed. The code must be a single block that can be passed to the `python_repl_tool`.

    IMPORTANT RULES:
    - Only use the `python_repl_tool`. Do not make up other tools.
    - The code you write for the tool must be valid Python code for the pandas library.
    - If your code produces an error, DO NOT apologize. Instead, in the next step, analyze the error message in your THOUGHT, and then write corrected code in your ACTION.
    - Once you have the final answer, your final response should be just the answer itself, without the "THOUGHT" and "ACTION" parts.
    - Always enclose your tool-use request in triple backticks ```.
    """

    system_prompt = PromptTemplate.from_template(system_prompt_template).format(df_schema=df_schema)

    # The conversation history tracks the agent's steps
    conversation_history = [SystemMessage(content=system_prompt), HumanMessage(content=question)]

    # Main agent loop for reasoning and self-correction
    max_turns = 7
    for turn in range(max_turns):
        yield {"type": "status", "content": f"Thinking... (Turn {turn + 1}/{max_turns})"}

        response = llm(conversation_history)
        message_content = response.content.strip()

        # Check if the agent has a final answer
        if "```" not in message_content:
            yield {"type": "final_answer", "content": message_content}
            return

        # Extract THOUGHT and ACTION
        thought = message_content.split("ACTION:")[0].replace("THOUGHT:", "").strip()
        action_code = message_content.split("ACTION:")[1].strip().replace("```", "")

        yield {"type": "thought", "content": thought}
        yield {"type": "action", "content": action_code}

        # Execute the code using the tool
        tool_output = python_repl_tool(action_code, df)

        yield {"type": "tool_output", "content": tool_output}

        # Add the agent's action and the tool's output to the history
        conversation_history.append(HumanMessage(content=f"TOOL_OUTPUT:\n{tool_output}"))

    yield {"type": "final_answer",
           "content": "The agent could not reach a final answer after the maximum number of turns."}