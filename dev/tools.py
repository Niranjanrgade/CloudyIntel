from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper

serper = GoogleSerperAPIWrapper()

tool_web_search = Tool(
        name="web_search",
        func=serper.run,
        description="Useful for when you need more information from an online search",
    )
