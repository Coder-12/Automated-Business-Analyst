import pandas as pd
from io import StringIO
import sys


def python_repl_tool(code: str, df: pd.DataFrame) -> str:
    """
    A tool that executes Python code with a provided pandas DataFrame.

    This function creates a restricted environment to run Python code.
    It captures and returns any output printed to stdout, the result of
    the code execution, or any errors that occur.

    Args:
        code (str): A string of Python code to be executed.
        df (pd.DataFrame): The pandas DataFrame available to the code as 'df'.

    Returns:
        str: The captured output, result, or error message from the execution.
    """
    # Create a restricted namespace for the execution. Only 'df' and 'pd' are available.
    local_namespace = {'df': df, 'pd': pd}

    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        # Execute the code in the restricted namespace
        exec(code, {'__builtins__': {}}, local_namespace)

        # Get the captured output from stdout
        output = redirected_output.getvalue()

        # If there's output from print statements, return it
        if output:
            return f"Code executed successfully. Output:\n{output}"

        # If no print output, it might be an expression. Let's eval to get the result.
        # This is a simplified approach; a more robust solution might parse for final expressions.
        try:
            # Try to evaluate the last line if it's an expression
            last_line = code.strip().split('\n')[-1]
            result = eval(last_line, {'__builtins__': {}}, local_namespace)
            return f"Code executed successfully. Result:\n{result}"
        except Exception:
            return "Code executed successfully, but no output was captured or result returned."

    except Exception as e:
        # If an error occurs, return the formatted traceback
        error_message = f"Error executing code: {type(e).__name__}\n{e}"
        return error_message

    finally:
        # Restore stdout
        sys.stdout = old_stdout