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
