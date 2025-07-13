class Agent:
    def __init__(self, name):
        self.name = name

    def run_task(self, task):
        print(f"{self.name} is starting task: {task.name}")
        task.execute()
        print(f"{self.name} has completed task: {task.name}")