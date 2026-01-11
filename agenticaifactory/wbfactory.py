import os

from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams


class MyWorkbenchFactory:
    @staticmethod
    def getWorkbenchInfo():
        wb_info=McpWorkbench(StdioServerParams(

        command="/usr/local/bin/docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e", f"JIRA_URL={os.getenv('JIRA_URL')}",
            "-e", f"JIRA_USERNAME={os.getenv('JIRA_USERNAME')}",
            "-e", f"JIRA_API_TOKEN={os.getenv('JIRA_TOKEN')}",
            # "-e", f"JIRA_PROJECTS_FILTER={os.getenv('JIRA_PROJECTS_FILTER')}",
            # "ghcr.io/sooperset/mcp-atlassian:latest"
            # TEMP: comment out filter while debugging
            # "-e", f"JIRA_PROJECTS_FILTER={os.getenv('JIRA_PROJECTS_FILTER')}",

            "-e", "MCP_VERBOSE=false",
            "-e", "MCP_LOGGING_STDOUT=false",

            # Pin instead of :latest while debugging (adjust to a version you choose)
             "ghcr.io/sooperset/mcp-atlassian:latest"

        ], read_timeout_seconds=60

    ))

        return wb_info