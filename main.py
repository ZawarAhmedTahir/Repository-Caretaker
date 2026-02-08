from agents import Agent, Runner, tool
import subprocess
import os
from agents import Agent, Runner,  set_default_openai_client, set_tracing_disabled, function_tool
from agents.extensions.memory import SQLAlchemySession
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv("DATABASE_URL")
ai_client_url =  os.getenv("AI_CLIENT_URL")
api_key =  os.getenv("API_KEY")
model_name = os.getenv("MODEL_NAME")

@function_tool
def run_safe_commands(cmd: str)-> str:
    """Run only safe command. Never use rm, sudo, git init etc"""
    allowed = ["mod","test","vendor"]
    print("run_safe_commands: ",cmd)
    if not any(cmd.strip().startswith(a) for a in allowed):
        return "command not allowed"
    try:
        return subprocess.check_output(cmd,shell=True, text=True,cwd=os.getcwd(),timeout=30)
    except Exception as e:
        return f"Error: {e}"
    
@function_tool
def read_file(path: str)->str:
    try:
        print("read_file ",path)
        with open(path,"r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"cannot read: {e}"

@function_tool
def write_file(path: str, content: str)->str:
    try:
        print("write_file")
        with open(path,"w", encoding="utf-8") as f:
            f.write(content)
        return "File Written"
    except Exception as e:
        return f"Write failed: {e}"

caretaker = Agent(
    name="RepoCaretaker",
        model=model_name, # Must match the model name in your local server
        instructions=
        """
        You are professional, careful repository caretaker.
        1. First explore the repo(git status, list files, run linter).
        2. Fix only small, safe things: lint errors, formatting, unused imports, outdated requirements, explanatory comments, add TODO functions.
        3. Never delete file, or make bug changes.
        4. After fixes, run tests if any.
        5. Never use git init to create new git project of project already not existing, just make changes directly in file.
        6. If there is any TODO comment in the file then implement that function according to TODO description and write test cases for the function.
        7. Finally commit with a clear conventional commit message.
        8. Review files every for TODO comments or any other operation that can be performed according to instructions.
        Always ask human before committing if you are not 100% sure.
        """,
        tools=[run_safe_commands,read_file,write_file]
)

if __name__== "__main__":
    set_tracing_disabled(True)
    client = AsyncOpenAI(
        base_url=ai_client_url,
        api_key=api_key 
    )
    set_default_openai_client(client)
    session = SQLAlchemySession.from_url(
        "session ID",
        url=database_url,
        create_tables=True
    )

    result = Runner.run_sync(caretaker,"Perform routine maintenance on this repository, only update main.go for now",session=session)
    print(result.final_output)