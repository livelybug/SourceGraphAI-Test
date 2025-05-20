# Python AI Test

## Install
```shell
uv venv --python 3.11
source .venv/bin/activate
uv pip install scrapegraphai
uv pip install -U duckduckgo-search
uv pip install scrapegraphai'[other-language-models]'
uv pip install scrapegraphai'[more-semantic-options]'
uv pip install scrapegraphai'[more-browser-options]'
# Install browsers in Playwright: You can install specific browsers
playwright install --with-deps chromium
# Install all browsers
playwright install
```
Verify
```shell
uv run basis/search_graph_or.py 
```

## Scrape to Markdown
```shell
git clone https://github.com/livelybug/SourceGraphAI-Test.git
cd SourceGraphAI-Test
uv venv --python 3.11
source .venv/bin/activate
uv pip install

copy .env.example .env
# Fill JINA_API_KEY, DEEPSEEK_API_KEY

# Set keywords you want to search in scrape-to-markdown/config/keywords.json

uv run ruff check scrape-to-markdown/
python scrape-to-markdown/main.py

# python scrape-to-markdown/main.py --help
# python scrape-to-markdown/main.py --skip-search True
```
