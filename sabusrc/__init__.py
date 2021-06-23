import json
import time

from datetime import datetime, timedelta
from pynotifier import Notification

TASKS_PATH = "/tasks/task.json"


class Sabu:
    def current_day(self) -> str:
        return datetime.now().today().strftime("%A").lower()

    def get_tasks(self, file: str = TASKS_PATH) -> list:
        """
        Read the task from json file
        """
        with open(file, "r") as stream:
            try:
                data = json.load(stream)
                day_name = self.current_day()
                tasks = data["all"] + data[day_name]
                task_times_wise = {}
                for task in tasks:
                    if task["time"] in task_times_wise:
                        task_times_wise[task["time"]].append({"task": task["task"]})
                    else:
                        task_times_wise[task["time"]] = [{"task": task["task"]}]
            except Exception as exc:
                task_times_wise = []
                print(exc)
        return task_times_wise

    def create_task_notification(self):
        """ """
        tasks = self.get_tasks()
        while True:
            current_time = datetime.now().strftime("%H:%M")
            starttime = time.time()
            print("firsdt: ", tasks)
            if current_time in tasks:
                for task in tasks[current_time]:
                    Notification(
                        title=task["task"],
                        description=task["task"],
                        icon_path="/absolute/path/to/image/icon.png",
                        duration=5,
                        urgency="normal",
                    ).send()
            # sleep for a minute        
            time.sleep(60)


def main():
    sabu = Sabu()
    sabu.create_task_notification()


if __name__ == "__main__":
    main()
