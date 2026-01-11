from pathlib import Path


class MyPromptLoader:
    BASE = Path(__file__).parent/"prompts"

    @staticmethod
    def load(agent : str):
        path_for_version= MyPromptLoader.BASE/agent/"current.txt"
        if not path_for_version.exists():
            raise FileNotFoundError("The current.txt is not found.")
        version_to_executed = path_for_version.read_text().strip()
        path_version_in_action = MyPromptLoader.BASE/agent/version_to_executed
        if not path_version_in_action.exists():
            raise FileNotFoundError("file containing prompt is not found.")
        prompt_text=path_version_in_action.read_text().strip()
        return prompt_text

print(MyPromptLoader.load("jira"))