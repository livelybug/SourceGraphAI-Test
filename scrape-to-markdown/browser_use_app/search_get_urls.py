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
import time

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

def extract_json_array(text):
    """
    Extracts the first JSON array from text with optional prefix.
    Handles multi-line arrays and trailing commas.
    """
    # Find JSON array pattern (allowing for multi-line content)
    array_match = re.search(r'\[\s*([\s\S]*?)\s*\]', text, re.DOTALL)
    
    if not array_match:
        return None
        
    try:
        # Clean up potential JSON issues
        array_content = array_match.group(0)
        
        # Remove trailing commas before closing bracket
        cleaned_content = re.sub(r',\s*\]', ']', array_content)
        
        # Parse cleaned JSON
        return json.loads(cleaned_content)
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return None

async def record_activity(agent_obj):
    global urls_returned
    
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
        clean_arr = extract_json_array(extracted_content_json_last_elem)
        if clean_arr and isinstance(clean_arr, list) and all(isinstance(elem, str) and elem.startswith("http") for elem in clean_arr):
            print("clean arr", clean_arr)
            urls_returned = clean_arr

urls_returned = []

async def search_get_urls(keywords):
    global urls_returned
    
    task = f"""
    Do the following tasks step by step, each task starts with an asterisk (*);
    * Visit "https://www.google.com";
    * search for the keyword: input `{keywords}`, then press ENTER button to trigger a search;
    * append URL parameter "&udm=14" to the browser's current URL, then press ENTER button to use the "web" filter to refine the search result;
    * extract all the search results' URLs; 
    * if the extraction only contains metadata, strip the metadata, so the extraction contains URLs only;
    * convert the extracted URLs into a json format array, each element of the array is a URL only, no index; 
    """
    
    async with await browser.new_context(
        config=BrowserContextConfig()
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
        await browser.close()
        
        # check if "urls_returned" is an empty array, if yes, sleep 2 secondes and check again, if no, print it and exit
        retries = 10
        while not urls_returned and retries > 0:
            print("No URLs found yet, waiting 2 seconds...")
            await asyncio.sleep(1)
            retries -= 1

        if urls_returned:
            if len(urls_returned) > 3:
                print("Extracted URLs:", urls_returned)
                return urls_returned
                sys.exit(0)
            else:
                raise KeyError(f'number of URL not enough: {urls_returned}')
        else:
            print("No URLs extracted after waiting.")
            sys.exit(1)

        input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(search_get_urls("solid and reliable memecoin trading logic"))