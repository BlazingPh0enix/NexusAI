from typing import Dict, Union
from crewai.tools import BaseTool
from ddgs import DDGS

class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Web Search"
    description: str = (
        "A reliable web search tool using DuckDuckGo. "
        "Searches the web for current information on any topic. "
        "Input should be a search query string."
    )

    def _run(self, query: Union[str, Dict]) -> str:
        """
        Perform web search using DuckDuckGo
        """
        try:
            # Handle different input formats
            if isinstance(query, dict):
                search_query = query.get('query') or query.get('q') or str(query)
            else:
                search_query = str(query)

            # Clean the query
            search_query = search_query.strip()
            if not search_query:
                return "Error: Empty search query provided"

            with DDGS() as ddgs:
                results = []
                try:
                    # Get search results
                    search_results = ddgs.text(search_query, max_results=10)
                    
                    for i, result in enumerate(search_results, 1):
                        if isinstance(result, dict):
                            title = result.get('title', 'No title')
                            body = result.get('body', 'No description')
                            url = result.get('href', 'No URL')
                            
                            results.append(f"{i}. **{title}**\n   {body}\n   Source: {url}\n")
                        else:
                            results.append(f"{i}. {str(result)}\n")
                            
                    if results:
                        return f"Search Results for '{search_query}':\n\n" + "\n".join(results)
                    else:
                        return f"No results found for '{search_query}'"
                        
                except Exception as search_error:
                    return f"Search failed for '{search_query}': {str(search_error)}"
                    
        except Exception as e:
            return f"Error in DuckDuckGo search tool: {str(e)}"
