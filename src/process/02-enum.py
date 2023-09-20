from enum import Enum, auto


class State(Enum):
    READY = auto()  # 👌
    RUNNING = auto()
    WAITING = auto()


class Process:
    def __init__(self) -> None:
        self.state = State.READY

    def schedule(self) -> None:
        if not self.state == State.READY:  # 🟤
            raise ValueError("Cannot schedule")

        self.state = State.READY  # 🟡

    def possible_operations(self) -> list[str]:
        match self.state:
            case State.READY:
                return ["schedule", "watch Netflix"]  # 🔵
            case State.RUNNING:
                return ["wait"]
            # case State.WAITING:  # 👌

        raise ValueError("Invalid state")


class OperatingSystem:
    processes: list[Process]

    # Do stuff with them...
