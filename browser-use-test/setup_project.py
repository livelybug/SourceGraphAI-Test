import os
import subprocess
import sys
from pydantic import SecretStr, Field
import asyncio
import re
from typing import Optional
from langchain_core.utils.utils import secret_from_env
from langchain_openai import ChatOpenAI

class ChatOpenRouter(ChatOpenAI):
    openai_api_key: Optional[SecretStr] = Field(
        alias="api_key",
        default_factory=secret_from_env("OPENROUTER_API_KEY", default=None),
    )
    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"openai_api_key": "OPENROUTER_API_KEY"}

    def __init__(self,
                openai_api_key: Optional[str] = None,
                 **kwargs):
        openai_api_key = (
            openai_api_key or os.environ.get("OPENROUTER_API_KEY")
        )
        super().__init__(
            base_url="https://openrouter.ai/api/v1",
            openai_api_key=openai_api_key,
            **kwargs
        )


def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}", file=sys.stderr)
    return result.returncode == 0

def main():
    # Create project directory structure
    os.makedirs("google_results", exist_ok=True)
    os.makedirs("x_results", exist_ok=True)
    
    # Check if uv is installed
    if not run_command("uv --version"):
        print("Installing uv...")
        run_command("pip install uv")
    
    # Initialize virtual environment
    print("Initializing virtual environment...")
    run_command("uv venv --python 3.11")
    
    # Determine the activate script path based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        activate_cmd = "source .venv/bin/activate"
    
    # Install dependencies
    print("Installing dependencies...")
    run_command(f"{activate_cmd} && uv pip install browser-use")
    
    print("\nSetup complete! You can now run the search script with:")
    if os.name == 'nt':
        print(".venv\\Scripts\\python search_keywords.py")
    else:
        print(".venv/bin/python search_keywords.py")

if __name__ == "__main__":
    main()