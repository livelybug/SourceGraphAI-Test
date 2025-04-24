"""
Example of Search Graph
"""

import json
import os
import pprint

from dotenv import load_dotenv

from scrapegraphai.graphs import SearchGraph
from scrapegraphai.graphs import SmartScraperGraph

load_dotenv()

# ************************************************
# Define the configuration for the graph
# ************************************************

ds_key = os.getenv("DEEPSEEK_API_KEY")

graph_config = {
    "llm": {
        "api_key": ds_key,
        # "model": "deepseek/deepseek-coder",
        "model": "deepseek/deepseek-chat",
    },
    "max_results": 2,
    "verbose": True,
    "temperature": 0.6,
    "headless": False,
    "search_engine": "duckduckgo",
    "rate_limit": {
        "requests_per_second": 4
    }    
}

# ************************************************
# Create the SearchGraph instance and run it
# ************************************************

# search_graph = SmartScraperGraph(
#     prompt="Extract all the posts from the website",
#     source="https://www.aivi.fyi/",
#     config=graph_config
# )

prompt="""search for profitable memecoin trading strategies logic"""

search_graph = SearchGraph(
    prompt=prompt,
    config=graph_config
)

result = search_graph.run()
# print(result)
print(json.dumps(result, indent=4, ensure_ascii=False))
