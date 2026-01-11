from pathlib import Path


class MyTaskLoader:

    BASE=Path(__file__).parent/"tasks"
    @staticmethod
    def load(agent:str, task:str) -> str:
        path_till_task_file=MyTaskLoader.BASE/agent/f"{task}.txt"

        print("Value of     Path(__file__): ", Path(__file__))
        print("Value of     Path(__file__).parent: ", Path(__file__).parent)

        print("Value of BASE: ", path_till_task_file)
        print("Value of path_till_task_file: ", path_till_task_file)
        if not path_till_task_file.exists():
            raise FileNotFoundError("The task file does not exist.")
        task_to_be_executed = path_till_task_file.read_text().strip()
        return task_to_be_executed


print(MyTaskLoader.load("jira", "get_jira_issues"))