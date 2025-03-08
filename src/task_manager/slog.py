import datetime

class Slog:
    def __init__(self):
        self.logs = []
    
    def add_log(self, type: str, line: str, newline=False):
        now = datetime.datetime.now()
        now = now.strftime("%m/%d/%Y %H:%M:%S")
        if newline:
            self.logs.append(f"\n[{now}][{type}] {line}\n")
        else: 
            self.logs.append(f"[{now}][{type}] {line}")

    def get_logs(self):
        return self.logs
