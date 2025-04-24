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

# llm_key = os.getenv("DEEPSEEK_API_KEY")
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
    "max_results": 2,
    "verbose": True,
    "temperature": 0.6,
    "headless": False,
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

prompt="""Extract the reddit post and all its reply, 
then extract the content of all replies and document the content to a clear guide on how to trade meme coin"""

search_graph = SmartScraperGraph(
    prompt=prompt,
    source="https://www.reddit.com/r/solana/comments/1i7xk0t/how_to_trade_memecoins/",
    config=graph_config
)

result = search_graph.run()
# print(result)
print(json.dumps(result, indent=4, ensure_ascii=False))
