import subprocess
import threading
import sys
import time 
import io 

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self._lock = threading.Lock()

    def stream_output(self, process, task_id):
        stdout_buffer = io.StringIO()

        while process.returncode is None:
            for line in process.stdout:
                stdout_buffer.write(line)
                with self._lock:
                    self.tasks[task_id]["stdout"] = stdout_buffer.getvalue()

            process.poll()

    def run_script(self, script_path, task_id):
        try:
            process = subprocess.Popen([sys.executable, script_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       bufsize=1000,
                                       text=True)
            with self._lock:
                self.tasks[task_id]["process"] = process
                self.tasks[task_id]["status"] = "running"

            # start output streaming in a separate thread
            stream_thread = threading.Thread(
                target=self.stream_output,
                args=(process, task_id),
                daemon=True
            )

            with self._lock:
                self.tasks[task_id]["stream_thread"] = stream_thread

            stream_thread.start()

        except FileNotFoundError:
            with self._lock:
                self.tasks[task_id]["status"] = "error"
                self.tasks[task_id]["stderr"] = f"Error: Script '{script_path}' not found."
                self.tasks[task_id]["returncode"] = -1
        except Exception as e:
            with self._lock:
                self.tasks[task_id]["status"] = "error"
                self.tasks[task_id]["stderr"] = f"An error occurred: {str(e)}"
                self.tasks[task_id]["returncode"] = -1

    def start_task(self, script_path, task_id):
        self.tasks[task_id] = {
                 "script_path": script_path, 
                 "status": "waiting",
                 "process": None,
                 "thread": None,
                 "returncode": None,
                 "stream_thread": None,
                 "stdout": "",
                 "stderr": "" 
            }

        thread = threading.Thread(target=self.run_script, args=(script_path, task_id))
        self.tasks[task_id]["thread"] = thread
        thread.start()


    def get_task_info(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                return dict(self.tasks[task_id])
        return None

    def get_output(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                return {
                    "stdout": self.tasks[task_id].get("stdout", ""),
                    "stderr": self.tasks[task_id].get("stderr", "")
                }
        return {"stdout": "", "stderr": ""}

    def stop_all_tasks(self):
        for task_id in self.tasks:  # Iterate over task IDs
            task_info = self.tasks[task_id]
            if task_info and task_info["process"]:
                task_info["process"].terminate()

    def stop_task(self, task_id):
        task_info = self.get_task_info(task_id)
        if task_info and task_info["process"]:
            task_info["process"].terminate()
            print(f"Task {task_id} terminated.")

task_manager = TaskManager()
