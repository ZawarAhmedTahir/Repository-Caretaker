from agents import function_tool
import subprocess
import os
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