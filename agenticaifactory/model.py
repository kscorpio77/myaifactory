from autogen_ext.models.openai import OpenAIChatCompletionClient


class MyModelConfig:
    def __init__(self, model, time_to_respond, retrycount):
        self.model = model
        self.time_to_respond= time_to_respond
        self.retrycount = retrycount

