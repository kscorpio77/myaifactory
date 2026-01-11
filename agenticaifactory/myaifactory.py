from autogen_agentchat.agents import AssistantAgent

from agenticaifactory.model import MyModelConfig
from agenticaifactory.modelfactory import MyModelFactory
from agenticaifactory.promptloader import MyPromptLoader
from agenticaifactory.wbfactory import MyWorkbenchFactory


class MyAiFactory:

    @staticmethod
    def create_jira_agent():
        model_info = MyModelFactory.getModelInfo(MyModelConfig("gpt-4o", 120, 3))
        sys_msg=MyPromptLoader.load("jira")
        wb_info=MyWorkbenchFactory.getWorkbenchInfo()
        jiragent= AssistantAgent(name="jiraagent", system_message=sys_msg, model_client=model_info, workbench=wb_info)
        return jiragent

    def create_mcp_agent(self):
        pass

    def create_db_agent(self):
        pass