class Task:
    def __init__(self, name):
        self.name = name

    def execute(self):
        raise NotImplementedError("Subclasses should implement this method.")