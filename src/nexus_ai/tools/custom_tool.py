from crewai.tools import BaseTool
from ddgs import DDGS

class SearchTool(BaseTool):
    name: str = "Web Search"
    description: str = (
        "Tool for performing web searches to find relevant and up-to-date information."
    )

    def _run(self, query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = [result for result in ddgs.text(query, max_results=5)]
                return "\n".join(str(result) for result in results) if results else "No results found."
        except Exception as e:
            return f"An error occurred while performing the search: {e}"
