import os

from ms_notifier import notify_ms_disk_space
from maxbot_notifier import notify_maxbot_is_working


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    notify_ms_disk_space()
    notify_maxbot_is_working()
