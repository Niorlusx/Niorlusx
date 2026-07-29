# main.py

from agents.index import Agent
from tasks.index import Task

def main():
    # Initialize the agent and task
    agent = Agent(name="default-agent")
    task = Task(name="default-task")

    # Run the task using the agent
    agent.run_task(task)

if __name__ == "__main__":
    main()