# SourceGraphAI-Test

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