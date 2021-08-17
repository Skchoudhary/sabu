import argparse
import json
import os
import time
import sys

from datetime import datetime
from pynotifier import Notification
import multiprocessing

TASKS_PATH = os.path.join(os.getcwd(), "tasks/task.json")
DAYS = [
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
    "sun",
    "eve",
]


class Sabu:
    """
    Sabu a helpful tool to remind you of day to day tasks
    """

    tasks = None
    task_times_wise = None

    def __init__(self):
        self.tasks = {}
        self.task_times_wise = {}
        self.get_tasks()

    def current_day(self) -> str:
        return datetime.now().today().strftime("%a").lower()

    def get_task_time_wise(self):
        """ """

        day_name = self.current_day()
        current_day_tasks = self.tasks["eve"] + self.tasks[day_name]
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
        tasks = self.get_task_time_wise()
        while tasks:
            current_time = datetime.now().strftime("%H:%M")
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

        print('No task!')

    def add_task(self, task_name: str, task_time: str, day: str) -> bool:
        """ """
        day = day.lower()
        if day in DAYS:
            task = {"task": task_name, "time": task_time}
            try:
                with open(TASKS_PATH, "r") as file:
                    data = json.load(file)

                day_wiese_task = data[day]
                if type(day_wiese_task) == list:
                    day_wiese_task.append(task)
                else:
                    day_wiese_task = [task]

                with open(TASKS_PATH, "w") as file:
                    json.dump(data, file, indent=4)

                self.get_tasks()
            except Exception as e:
                print("Something went wrong while saving new task. Please try again.")

        else:
            print("Not a valid day")
            sys.exit(1)
        return False

    def print_tasks(self, tasks, day):
        """ """
        for index, task in enumerate(tasks):
            if index and task:
                key = f"{index}:{day[0:3]}"
                print(f'key: {key} \tTasks: {task["task"]} at {task["time"]}')

    def list_tasks(self, curr_day: str = ""):
        """ """
        tasks = self.get_tasks()
        if curr_day:
            tasks = tasks[curr_day]
            self.print_tasks(tasks, curr_day)

        else:
            for day, tasks in tasks.items():
                self.print_tasks(tasks, day)

    def delete_task(self, task_id):
        """ """

        task_id_list = task_id.split(":")
        day = task_id_list[-1]
        index = int(task_id_list[0])

        try:
            with open(TASKS_PATH, "r") as file:
                data = json.load(file)

            day_wiese_task = data[day]
            print(day_wiese_task)
            if type(day_wiese_task) == list:
                day_wiese_task.pop(index - 1)

            with open(TASKS_PATH, "w") as file:
                json.dump(data, file, indent=4)

            self.get_tasks()
        except Exception as e:
            print(e)
            print("Something went wrong while deleting a task. Please try again!")


def main():
    p = argparse.ArgumentParser(
        description="A helpful tool to remind you of day to day tasks"
    )

    # g = p.add_mutually_exclusive_group()
    p.add_argument(
        "-st",
        "--start",
        action="store_true",
        dest="start",
        help="start the remainder in the background",
    )
    # g.add_argument(
    #     "-stp",
    #     "--stop",
    #     action="store_true",
    #     dest="stop",
    #     help="stop the remainder in the background",
    # )

    p.add_argument(
        "-a", "--add", dest="add", help="add the tasks, format <task name> <time> <day>", nargs='+'
    )
    # p.add_argument("-n", "--name", help="name/desc of the task to be added")
    # p.add_argument(
    #     "-d", "--day", dest="day", help="day name for which task to be added"
    # )
    # p.add_argument("-t", "--time", dest="add", help="add new task(s)")

    # p.add_argument(
    #     "-d", "--delete", action="store_true", dest="delete", help="delete the task"
    # )
    p.add_argument("-ll", "--list", help="list the tasks")

    p.add_argument("-llist", "--llist", help="list the tasks", nargs='+')

    args = p.parse_args()
    sabu = Sabu()

    try:
        if args.start:
            sabu.create_task_notification()

        elif args.add:
            sabu.add_task(*args.add)
        elif args.add:
            print('Enter task descriptiom/Name')
            task_name = str(input())

            print('Enter time in HH:MM format.')
            task_time = str(input())

            print(f'Enter day, leave blank if wan to add current day or choose from {"-".join(DAYS)}')
            day = str(input())
            if not day:
                day= sabu.current_day()

            sabu.add_task(task_name, task_time, day)
        elif args.list:
            print(f'Enter day for the tasks or leave blank')
            day = str(input())
            sabu.list_tasks(day)
        elif args.llist:
            print(args.llist)

    except Exception as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
