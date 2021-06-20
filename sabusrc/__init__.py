import yaml

from datetime import datetime
from pynotifier import Notification

TASKS_PATH = "sabusrc/tasks/task.yml"


def current_day() -> str:
    return datetime.now().today().strftime("%A")


def read_tasks(file: str = TASKS_PATH):
    with open(file, "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


class NotificationHandler:
    def __init__(self) -> None:
        pass

    def create_notification(
        title: str,
        desc: str,
        icon_path: str = "/absolute/path/to/image/icon.png",
        duration: int = 5,
    ) -> None:
        """
        create the system notifications
        """
        Notification(
            title=title,
            description=desc,
            icon_path=icon_path,
            duration=duration,
            urgency="normal",
        ).send()


def main():
    pass


if __name__ == "__main__":
    main()
