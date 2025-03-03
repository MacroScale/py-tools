import datetime

class Tool:
    def __init__(self, id, name, execution_status, exit_status, last_run):
        self.id = id
        self.name = name
        self.execution_status = execution_status
        self.exit_status = exit_status
        self.last_run = last_run

    @staticmethod
    def MapTuple(data: tuple):
        id, name, execution_status, exit_status, last_run = data
        return Tool(id, name, execution_status, exit_status, last_run)

    def __eq__(self, other):
        if isinstance(other, Tool):
            return (self.id == other.id and
                    self.name == other.name and
                    self.execution_status == other.execution_status and
                    self.exit_status == other.exit_status and
                    self.last_run == other.last_run)
        return False
