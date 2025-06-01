create a `.env` file and add below env vars:

```
GOOGLE_API_KEY=<API KEY>
LANGCHAIN_TRACING_V2=false
```

Required tools:
- python3
- uv

To install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Running the agent:
- `uv pip install -r pyproject.toml`
- `uv run multiCLientAgent.py` or `uv run singleClientAgent.py`