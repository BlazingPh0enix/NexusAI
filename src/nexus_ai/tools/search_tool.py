from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from typing import Any, Type, List, Dict, Union

class SafeSerperSearchTool(BaseTool):
    name: str = "Safe Web Search Tool"
    description: str = (
        "A robust web search tool that handles various input formats. "
        "Use this to find up-to-date information on any topic."
    )
    
    # Internal instance of the actual Serper tool
    _serper_tool: SerperDevTool = SerperDevTool()

    def _run(self, query: Union[str, Dict, List[Dict]]) -> str:
        """
        Run the search tool, intelligently handling string, dict, or list inputs.
        """
        try:
            if isinstance(query, str):
                # If input is a simple string, use it directly
                return self._serper_tool.run(query)
            
            elif isinstance(query, dict) and 'q' in query:
                # If input is a dictionary like {'q': 'search'}, extract the query
                return self._serper_tool.run(query['q'])

            elif isinstance(query, dict) and 'query' in query:
                # Handle cases where the agent uses 'query' as the key
                return self._serper_tool.run(query['query'])
            
            elif isinstance(query, list):
                # If input is a list of searches, perform the first one
                if query and isinstance(query[0], dict) and 'q' in query[0]:
                    return self._serper_tool.run(query[0]['q'])
            
            # If the format is still unrecognized, return an error message
            return "Error: Invalid input format for the search tool."

        except Exception as e:
            return f"An error occurred during search: {e}"