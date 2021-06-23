import os
import json
import time

from datetime import datetime
from pynotifier import Notification

TASKS_PATH = os.path.join(os.getcwd(), 'tasks/task.json')
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "everyday"]


class Sabu:

    tasks = None
    task_times_wise = None

    def __init__(self):
        self.tasks = {}
        self.task_times_wise = {}

    def current_day(self) -> str:
        return datetime.now().today().strftime("%A").lower()

    def get_task_time_wise(self):
        '''
        '''
        
        day_name = self.current_day()
        current_day_tasks = self.tasks["everyday"] + self.tasks[day_name]
        task_times_wise = {}

        for task in current_day_tasks:
            if task["time"] in task_times_wise:
                task_times_wise[task["time"]].append({"task": task["task"]})
            else:
                task_times_wise[task["time"]] = [{"task": task["task"]}]

        self.task_times_wise = task_times_wise

    def get_tasks(self, file: str = TASKS_PATH) -> None:
        """
        Read the task from json file
        """
        with open(file, "r") as file:
            try:
                tasks = json.load(file)
            except Exception as exc:
                tasks = {}
                print(exc)

        self.tasks = tasks

    def create_task_notification(self):
        """ """
        tasks = self.get_tasks()
        while tasks:
            current_time = datetime.now().strftime("%H:%M")
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
            time.sleep(60)

    def add_task(self, task_name: str, task_time: str, day: str) -> bool:
        """ """
        day = day.lower()
        if day in DAYS:
            task = {"task": task_name, "time": task_time}
            with open(TASKS_PATH, 'r') as file:
                data = json.load(file)
            
            day_wiese_task = data[day]
            if type(day_wiese_task) == list:
                day_wiese_task.append(task)
            else:
                day_wiese_task = [task]

            with open(TASKS_PATH, 'w') as file:
                json.dump(data, file, indent=4)

            return True

        return False


def main():
    sabu = Sabu()
    sabu.create_task_notification()


if __name__ == "__main__":
    main()
