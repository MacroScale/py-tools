import datetime

class Slog:
    def __init__(self):
        self.logs = []
    
    def add_log(self, type: str, data):
        ts = datetime.datetime.now()
        ts = ts.strftime("%m/%d/%Y %H:%M:%S")

        # Convert bytes to string if needed
        if isinstance(data, bytes):
            data = data.decode('utf-8', errors='replace')

        lines = data.splitlines()
        for line in lines:
            if line.strip():  # only log non-empty lines
                self.logs.append(f"[{ts}][{type}] {line}\n")

    def get_logs(self):
        return "".join(self.logs)
