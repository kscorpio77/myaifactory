import asyncio

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

from agenticaifactory.myaifactory import MyAiFactory
from taskloader import MyTaskLoader
from dotenv import load_dotenv
load_dotenv()

async def main():
    jiraagent = MyAiFactory.create_jira_agent()
    myteam = RoundRobinGroupChat(participants=[jiraagent], termination_condition=TextMentionTermination("**Task Completed**"))
    await Console(myteam.run_stream(task=MyTaskLoader.load("jira","get_jira_issues")))


asyncio.run(main())