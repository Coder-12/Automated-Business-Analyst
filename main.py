import pandas as pd
import os
from dotenv import load_dotenv
from agent import create_analyst_agent


# Define some colors for nice printing
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    """
    Main function to run the interactive data analyst agent.
    """
    # Load environment variables from .env file
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{bcolors.FAIL}ERROR: OPENAI_API_KEY not found in .env file.{bcolors.ENDC}")
        return

    # Load the sample data
    try:
        data_path = "data/sales_data_sample.csv"
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(
            f"{bcolors.FAIL}ERROR: The data file was not found at '{data_path}'. Please make sure it exists.{bcolors.ENDC}")
        return

    print(f"{bcolors.HEADER}{bcolors.BOLD}Welcome to the Automated Business Analyst!{bcolors.ENDC}")
    print("You can ask questions about the sales data. Type 'exit' to quit.")

    while True:
        question = input(f"\n{bcolors.BOLD}Ask a question about the data: {bcolors.ENDC}")
        if question.lower() == 'exit':
            print(f"{bcolors.OKBLUE}Goodbye!{bcolors.ENDC}")
            break

        # Create and run the agent
        agent_generator = create_analyst_agent(df, question)

        for step in agent_generator:
            if step['type'] == 'status':
                print(f"{bcolors.OKCYAN}{step['content']}{bcolors.ENDC}")
            elif step['type'] == 'thought':
                print(f"{bcolors.OKBLUE}THOUGHT: {step['content']}{bcolors.ENDC}")
            elif step['type'] == 'action':
                print(f"{bcolors.WARNING}ACTION (Executing Code):\n---\n{step['content']}\n---{bcolors.ENDC}")
            elif step['type'] == 'tool_output':
                print(f"{bcolors.OKGREEN}OBSERVATION:\n---\n{step['content']}\n---{bcolors.ENDC}")
            elif step['type'] == 'final_answer':
                print(f"\n{bcolors.HEADER}{bcolors.BOLD}Final Answer:{bcolors.ENDC}\n{step['content']}")
                break


if __name__ == "__main__":
    main()