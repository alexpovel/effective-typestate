READY = 0
RUNNING = 2  # 🟢
WAITING = 1

# READY = "ready"
# RUNNING = "running"
# WAITING = "waiting"


class Process:
    def __init__(self) -> None:
        self.state = READY

    def schedule(self) -> None:
        if not self.state == WAITING:  # 🟤
            raise ValueError("Cannot schedule")

        self.state = READY  # 🟡

    def possible_operations(self) -> list[str]:
        if self.state == READY:
            return ["schedule", "watch Netflix"]  # 🔵
        elif self.state == RUNNING:
            return ["wait"]
        else:  # 🔴
            raise ValueError("Invalid state")


class OperatingSystem:
    processes: list[Process]

    # Do stuff with them...
