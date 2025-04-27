"""
Basic example of scraping pipeline using Code Generator with schema
"""

import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from scrapegraphai.graphs import ScriptCreatorMultiGraph

load_dotenv()

# ************************************************
# Define the output schema for the graph
# ************************************************


class Project(BaseModel):
    title: str = Field(description="The title of the project")
    description: str = Field(description="The description of the project")


class Projects(BaseModel):
    projects: List[Project]


# ************************************************
# Define the configuration for the graph
# ************************************************

# openai_key = os.getenv("OPENAI_APIKEY")
ds_key = os.getenv("DEEPSEEK_API_KEY")
llm_key = os.getenv("OPENROUTER_API_KEY")

from langchain_openai import ChatOpenAI

instance_config = {
    "model":"deepseek/deepseek-chat-v3-0324:free",
    "openai_api_base": "https://openrouter.ai/api/v1",  
    "api_key": llm_key
}

llm_model_instance = ChatOpenAI(**instance_config)

graph_config = {
    "llm": {
        "model_instance": llm_model_instance,
        "model_tokens": 4000,
    },
    "verbose": True,
    "headless": False,
    "library": "beautifulsoup",
    # "reduction": 2,
    "max_iterations": {
        "overall": 10,
        "syntax": 3,
        "execution": 3,
        "validation": 3,
        "semantic": 3,
    },
    "output_file_name": "extracted_data.py",
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************
urls = [
        "https://perinim.github.io/projects/", 
        "https://www.aivi.fyi/",
        ]
code_generator_graph = ScriptCreatorMultiGraph(
    prompt="List me all the projects with their description",
    source=urls,
    # schema=Projects,
    config=graph_config,
)

result = code_generator_graph.run()
print(result)
