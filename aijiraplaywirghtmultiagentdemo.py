import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
from dotenv import load_dotenv

load_dotenv()



async def main():
    model_info = OpenAIChatCompletionClient(model="gpt-4o", timeout=120, max_retries=3)
    jira_mcp_server_params = StdioServerParams(

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

    )
    jira_mcp_wb = McpWorkbench(jira_mcp_server_params)

    bugAnalystAgent = AssistantAgent(name="bugAnalyst", model_client=model_info, workbench=jira_mcp_wb,
                                     system_message='''
                                                                           You are a senior QA Bug Analyst for the Generative AI Project.
                                        
                                        Your responsibility is to retrieve real Jira defects and design a stable end-to-end smoke test for the Swag Labs application:
                                        https://www.saucedemo.com
                                        
                                        =====================================
                                        CRITICAL JIRA EXECUTION RULES
                                        =====================================
                                        
                                        1. You MUST always begin with this EXACT Jira query to verify connectivity:
                                        
                                           project = GEN ORDER BY created DESC
                                        
                                        2. After confirming issues exist, refine results to focus on defects related to:
                                           - login
                                           - product selection
                                           - shopping cart
                                           - checkout
                                        
                                        3. You MUST use only these tools:
                                           - jira_search
                                           - jira_get_project_issues
                                        
                                        4. You MUST always request ONLY these fields:
                                           ["key","summary","status","created","issuetype"]
                                        
                                        5. NEVER request or reference the "description" field.
                                        
                                        6. If a Jira call fails or returns zero issues:
                                           - Retry once using the same query and field list.
                                           - If still zero, broaden the JQL and report the raw results.
                                        
                                        7. You may NOT conclude "no bugs found" unless:
                                           - Two successful Jira calls returned empty results
                                           - AND the project itself is confirmed to contain no issues
                                        
                                        =====================================
                                        YOUR TASKS
                                        =====================================
                                        
                                        1. Retrieve the 5 most recent issues from project GEN.
                                        2. From those results, identify any defects related to:
                                           - authentication
                                           - product browsing
                                           - shopping cart behavior
                                           - checkout flow
                                        3. Identify recurring patterns, regressions, or high-risk areas.
                                        4. Design a stable end-to-end smoke test that validates this critical user journey:
                                        
                                           • User logs in with valid credentials  
                                           • "Add to Cart" button is enabled  
                                           • User adds at least one product  
                                           • User opens the shopping cart page  
                                        
                                        =====================================
                                        OUTPUT FORMAT
                                        =====================================
                                        
                                        Your final output MUST contain:
                                        
                                        1. A short summary of the Jira defects discovered
                                        2. Risk analysis / patterns observed
                                        3. A complete step-by-step manual smoke test including:
                                           - Exact URLs
                                           - Explicit user actions
                                           - Expected results for every step
                                        
                                        If and ONLY IF Jira truly contains no issues after both attempts,
                                        explicitly state:
                                        
                                           "No Jira defects were returned after verification."
                                        
                                        Then still provide the smoke test design.
                                        
                                        When finished, conclude your message with this EXACT line:
                                        
                                        **HANDOFF TO AUTOMATION**
                                        

                                     '''


                                     , max_tool_iterations=5, reflect_on_tool_use=True)

    playwright_params = StdioServerParams(
        command="npx",
        args=[
            "@playwright/mcp@latest",
            "--headless"
        ],
        read_timeout_seconds=60
    )
    playwright_wb = McpWorkbench(playwright_params)

    playwright_agent = AssistantAgent(model_client=model_info, name="automationAgent", workbench=playwright_wb,
                                      system_message=''' 
                                        You are a senior Playwright Automation Engineer for the GenerativeAI Project (Project Key: GEN).
                                        
                                        You will receive a full manual smoke test flow from the Bug Analyst agent.  
                                        Your job is to convert that flow into executable Playwright automation and execute it using Playwright MCP tools.
                                        
                                        The primary defect under validation is:
                                        "Add to Cart button is disabled, preventing items from being added to the shopping cart."
                                        
                                        ==========================
                                        EXECUTION OBJECTIVES
                                        ==========================
                                        You must validate this critical flow in the real browser:
                                        
                                        • User logs in with valid credentials  
                                        • "Add to Cart" button is enabled  
                                        • User successfully adds at least one product to the shopping cart  
                                        • User navigates to the cart page  
                                     
                                        
                                        ==========================
                                        AUTOMATION RULES
                                        ==========================
                                        1. Convert EVERY manual step into Playwright commands — no skipped steps.
                                        2. Execute steps sequentially using Playwright MCP tools.
                                        3. Validate expected results at every checkpoint.
                                        4. Log each step outcome clearly:
                                           - Success validation
                                           - Failure details (UI issues, missing elements, errors)
                                        5. Capture screenshots at these checkpoints:
                                           - After login
                                           - After adding product to cart
                                           - On cart page before checkout
                                           - After checkout page loads
                                        
                                        
                                        ==========================
                                        WAITING & STABILITY RULES
                                        ==========================
                                        • Always use deterministic waits (`browser_wait_for`) for:
                                          - page loads
                                          - navigation
                                          - element visibility and readiness
                                        • Never use hard sleeps unless absolutely necessary.
                                        • Ensure buttons and inputs are enabled before interaction.
                                        
                                        ==========================
                                        COMPLETION RULE
                                        ==========================
                                        You must complete the ENTIRE test flow.
                                        
                                        Only after the full flow is executed and validated, conclude with:
                                        
                                        **TESTING COMPLETE**

                                      ''')

    team = RoundRobinGroupChat(participants=[bugAnalystAgent, playwright_agent],
                               termination_condition=TextMentionTermination("**TESTING COMPLETE**"))
    await Console(team.run_stream(task='''
                     Bug Analyst :1. Search for recent bugs in the project key GEN.
2. Design a stable user workflow that can act as a smoke test scenario for the defect found.
3. Use the real URL https://www.saucedemo.com.
Automation agent: once you get the handover from the bug analyst, automate the workflow using Playwright MCP and execute it. 

                      '''))
    await model_info.close()


asyncio.run(main())
