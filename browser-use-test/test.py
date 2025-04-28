import json
import os
import pprint
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

import dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, AgentHistoryList, Browser, BrowserConfig
from pydantic import SecretStr, Field
from typing import Optional
from langchain_core.utils.utils import secret_from_env
from browser_use.browser.context import (
    BrowserContextConfig,
    BrowserContextWindowSize,
)
from pyobjtojson import obj_to_json

dotenv.load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key=SecretStr(api_key))

# api_key = os.getenv('GEMINI_API_KEY')
# llm = ChatGoogleGenerativeAI(
#         model='gemini-2.0-flash', 
#         api_key=SecretStr(api_key),
#         temperature=0.7,
#     )

# llm=ChatOpenRouter(model_name="deepseek/deepseek-chat-v3-0324:free")

browser = Browser(
	config=BrowserConfig(
		# chrome_instance_path='/usr/bin/google-chrome',
        cdp_url="http://localhost:12922",
	)
)

# * find the first 5 text-based, non-youtube result, 
# So there would be 5 urls saved in the end.
# * extract all search results' URLs, the extraction only contains URLs, no title, no source, no description, or anything else; 
task = """
Do the following tasks step by step, each task starts with an asterisk (*);
* Visit "https://www.google.com";
* search for the keyword: input `solid and reliable memecoin trading logic`, then press ENTER button;
* use the "web" filter to refine the search result;
* extract all the search results' URLs; 
* if the extraction only contains metadata, strip the metadata, so the extraction contains URLs only;
* convert the extracted URLs into a json format array, each element of the array is a URL only, no index; 
"""

async def record_activity(agent_obj):
    """Hook function that captures and records agent activity at each step"""
    print('--- ON_STEP_END HOOK ---')

    # Make sure we have state history
    if hasattr(agent_obj, "state"):
        history = agent_obj.state.history
    else:
        history = None
        print("Warning: Agent has no state history")
        return

    # Process extracted content
    extracted_content = agent_obj.state.history.extracted_content()
    extracted_content_json = obj_to_json(
        obj=extracted_content,
        check_circular=False
    )
    if len(extracted_content_json) > 0:
        extracted_content_json_last_elem = extracted_content_json[-1]
    
    print(1111, extracted_content_json_last_elem)
    # extract_url(extracted_content_json_last_elem)


def extract_url(raw_selection):
    match = re.search(r"\[\s*(.*?)\s*\]", raw_selection, re.DOTALL)
    if match and match.group(1):
        json_content = match.group(1)
        data = json.loads(json_content)
        print(11111, data)
        if isinstance(data, list) and all(isinstance(elem, str) and elem.startswith("http") for elem in data):
            return data
        # else:
        #     raise KeyError(f'No URL found in JSON:\n {data}')
    else:
        print("No JSON code block found.")    

async def main():
    keyword = 'profitable memecoin trading strategies logic'
    
    async with await browser.new_context(
        config=BrowserContextConfig(
            # cookies_file="./gmail.cookie.json",
            # trace_path="./tmp/traces",
            # save_recording_path="./tmp/record_videos",
            # no_viewport=False,
            # browser_window_size=BrowserContextWindowSize(
            #     width=window_w, height=window_h
            # ),
        )
    ) as browser_context:
        agent = Agent(
            task=task,
            llm=llm,
            # use_vision=True,
            browser_context=browser_context
        )

        history: AgentHistoryList = await agent.run(
            max_steps=20,
            on_step_end=record_activity,
        )
        # print(history)
        
        # history.save_to_file("history.json")
        await browser.close()

        input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())