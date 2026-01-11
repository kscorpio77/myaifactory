from autogen_ext.models.openai import OpenAIChatCompletionClient

from agenticaifactory.model import MyModelConfig


class MyModelFactory:
    @staticmethod
    def getModelInfo(config: MyModelConfig):
        model_info= OpenAIChatCompletionClient(model=config.model,
                                               max_retries=config.retrycount, timeout=config.time_to_respond)

        return model_info