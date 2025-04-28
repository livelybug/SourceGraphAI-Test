from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from dotenv import load_dotenv

from setup_project import ChatOpenRouter
load_dotenv()
from pydantic import SecretStr, Field
import asyncio
import os
import re
from typing import Optional
from langchain_core.utils.utils import secret_from_env

ds_api_key = os.getenv("DEEPSEEK_API_KEY")
api_key = os.getenv("OPENAI_API_KEY")
gmn_api_key = os.getenv('GEMINI_API_KEY')

# The argument is a enum, composed of the model name: gpt, gemini, deespeek, openrounter
async def create_llm(model_name):
    if model_name == "gpt":
        return ChatOpenAI(model="gpt-4o")
    elif model_name == "gemini":
        return ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(gmn_api_key))
    elif model_name == "deepseek":
        return ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key=SecretStr(ds_api_key))
    elif model_name == "openrouter":
        return ChatOpenRouter(model_name="deepseek/deepseek-chat-v3-0324:free")
    else:
        raise ValueError("Invalid model name provided.")

browser = Browser(
	config=BrowserConfig(
		browser_binary_path='/usr/bin/google-chrome',
        # headless=False,
		# disable_security=False,
		# keep_alive=True,
        # cdp_url='http://localhost:9222',
	)
)

controller = Controller()

async def read_keywords_file(file_path):
    """Read keywords from the specified file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Extract keywords enclosed in backticks
    keywords = re.findall(r'`([^`]+)`', content)
    return keywords

async def search_google(func, *args, keyword):
    """Search keyword in Google and open the first result."""
    task = f'Search in Google for keyword: "{keyword}" . '
    task += 'and find the first 10 results that are not video. '
    task += 'for each result: open it.'
    # task += ' and extract the content.'
    # task += 'Save the results in a markdown file.'
    # task += 'The file name should be the keyword with spaces replaced by underscores.'
    # task += 'The file should be saved in the google_results directory.'
    agent = func(*args, task=task)
    await agent.run()

async def search_x_com(browser, keyword):
    """Search keyword on X.com and find the most liked post."""
    # Navigate to X.com search
    search_url = f"https://x.com/search?q={keyword.replace(' ', '%20')}&src=typed_query&f=top"
    await browser.goto(search_url)
    
    # Accept cookies if the dialog appears
    try:
        await browser.click_if_exists("button:has-text('Accept all')")
    except:
        pass
    
    # Wait for tweets to load
    await browser.wait_for_selector("article[data-testid='tweet']")
    
    # Find the tweet with the most likes
    tweets = await browser.query_selector_all("article[data-testid='tweet']")
    
    most_likes = 0
    most_liked_tweet = None
    
    for tweet in tweets[:5]:  # Check first 5 tweets
        # Find like count
        like_element = await tweet.query_selector("div[data-testid='like']")
        if like_element:
            like_text = await like_element.inner_text()
            like_count = 0
            
            # Extract number from text (handling K, M formats)
            if like_text:
                like_text = like_text.strip()
                if 'K' in like_text:
                    like_count = int(float(like_text.replace('K', '')) * 1000)
                elif 'M' in like_text:
                    like_count = int(float(like_text.replace('M', '')) * 1000000)
                else:
                    try:
                        like_count = int(like_text)
                    except:
                        like_count = 0
            
            if like_count > most_likes:
                most_likes = like_count
                most_liked_tweet = tweet
    
    if most_liked_tweet:
        # Click on the tweet to open it
        await most_liked_tweet.click()
        await browser.wait_for_load_state("networkidle")
        
        # Get tweet content
        tweet_text = await browser.extract_text("article[data-testid='tweet']")
        tweet_url = await browser.url()
        
        return {
            "title": f"X.com post about '{keyword}'",
            "url": tweet_url,
            "content": tweet_text,
            "likes": most_likes
        }
    
    return {
        "title": f"No tweets found for '{keyword}'",
        "url": search_url,
        "content": "No content found",
        "likes": 0
    }

async def save_to_markdown(data, filename):
    """Save the search result to a markdown file."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"# {data['title']}\n\n")
        file.write(f"Source: [{data['url']}]({data['url']})\n\n")
        
        if 'likes' in data:
            file.write(f"Likes: {data['likes']}\n\n")
        
        file.write("## Content\n\n")
        file.write(data['content'])

def create_agent(llm, browser, controller, task):
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        controller=controller,
    )
    return agent

async def main():
    llm = await create_llm("gemini")
    # Create output directories
    os.makedirs("google_results", exist_ok=True)
    os.makedirs("x_results", exist_ok=True)
    
    # Read keywords
    keywords = await read_keywords_file("keywords.md")
    print(f"Found {len(keywords)} keywords: {keywords}")
    
    create_agent_partial = lambda task: create_agent(llm, browser, controller, task)
    
    try:
        for i, keyword in enumerate(keywords):
            print(f"Processing keyword {i+1}/{len(keywords)}: '{keyword}'")
            
            # Search Google
            print(f"Searching Google for '{keyword}'...")
            google_result = await search_google(create_agent_partial, keyword=keyword)
            return
            google_filename = f"google_results/google_{i+1}_{keyword.replace(' ', '_')}.md"
            await save_to_markdown(google_result, google_filename)
            print(f"Saved Google result to {google_filename}")
            
            # Search X.com
            print(f"Searching X.com for '{keyword}'...")
            x_result = await search_x_com(browser, keyword)
            x_filename = f"x_results/x_{i+1}_{keyword.replace(' ', '_')}.md"
            await save_to_markdown(x_result, x_filename)
            print(f"Saved X.com result to {x_filename}")
            
    finally:
        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())