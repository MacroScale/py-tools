from subprocess import Popen, PIPE, CalledProcessError
import threading
import sys
import time 
import io 
import os 

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self._lock = threading.Lock()

    def stream_output(self, task_id):
        stdout_buffer = io.StringIO()

        # poll process for new output until finished
        while True:
            nextline = self.tasks[task_id]["process"].stdout.readline()
            if nextline == '' and self.tasks[task_id]["process"].poll() is not None:
                break
            stdout_buffer.write(nextline)
            with self._lock:
                self.tasks[task_id]["stdout"] = stdout_buffer.getvalue()


    def run_script(self, tool_path, task_id):
        try:
            process = Popen([sys.executable, "-u", tool_path],
                                       stdout=PIPE,
                                       bufsize=1,
                                       universal_newlines=True,
                                       text=True,
                                )
            with self._lock:
                self.tasks[task_id]["process"] = process
                self.tasks[task_id]["status"] = "running"

            thread = threading.Thread(target=self.stream_output, args=(task_id,))
            self.tasks[task_id]["stream_output_thread"] = thread 
            self.tasks[task_id]["stream_output_thread"].start()

        except FileNotFoundError:
            with self._lock:
                self.tasks[task_id]["status"] = "error"
                self.tasks[task_id]["stderr"] = f"Error: Script '{tool_path}' not found."
                self.tasks[task_id]["returncode"] = -1
        except Exception as e:
            with self._lock:
                self.tasks[task_id]["status"] = "error"
                self.tasks[task_id]["stderr"] = f"An error occurred: {str(e)}"
                self.tasks[task_id]["returncode"] = -1

    def start_task(self, tool_path: str, tool_id: int):
        self.tasks[tool_id] = {
                 "tool_path": tool_path, 
                 "status": "waiting",
                 "process": None,
                 "thread": None,
                 "returncode": None,
                 "stream_thread": None,
                 "stdout": "",
                 "stderr": "" 
            }

        thread = threading.Thread(target=self.run_script, args=(tool_path, tool_id))
        self.tasks[tool_id]["thread"] = thread
        thread.start()
        print("\ntask start:", tool_path, "\n")


    def get_task_info(self, task_id):
        with self._lock:
            if task_id in self.tasks:
                return dict(self.tasks[task_id])
        return None

    def get_output(self, task_id: int):
        with self._lock:
            if task_id in self.tasks:
                return {
                    "stdout": self.tasks[task_id].get("stdout", ""),
                    "stderr": self.tasks[task_id].get("stderr", "")
                }
        return {"stdout": "", "stderr": ""}

    def delete_task(self, task_id: int):
        task_info = self.get_task_info(task_id)
        if not task_info: return
        if task_info["process"] and task_info["process"].poll() is not None:
            with self._lock:
                del self.tasks[task_id]

    def stop_all_tasks(self):
        for task_id in self.tasks:
            task_info = self.tasks[task_id]
            if task_info and task_info["process"]:
                task_info["process"].terminate()

    def stop_task(self, task_id):
        task_info = self.get_task_info(task_id)
        if task_info and task_info["process"] and task_info["stream_output_thread"]:
            task_info["process"].terminate()
            print(f"Task {task_id} terminated.")

task_manager = TaskManager()
