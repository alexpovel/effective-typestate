import typing as t
from dataclasses import dataclass


@dataclass
class Process:
    id: int  # So creation and conversion is more interesting


class RunningProcess(Process):
    @classmethod
    def from_scheduling(cls, process: "ReadyProcess") -> t.Self:
        return cls(id=process.id)


class ReadyProcess(Process):
    @classmethod
    def from_completing_io(cls, process: "WaitingProcess") -> t.Self:
        return cls(id=process.id)

    @classmethod
    def from_descheduling(cls, process: RunningProcess) -> t.Self:
        return cls(id=process.id)


class WaitingProcess(Process):
    @classmethod
    def from_initiating_io(cls, process: ReadyProcess) -> t.Self:  # 🔴
        return cls(id=process.id)


class OperatingSystem:
    processes: list[Process]

    # Do stuff with them...


def example() -> None:
    process: Process  # Needed for type checking; comment out for inlay hints
    process = ReadyProcess(id=1)

    # vvvvvvvvvvvvvv Inlay hints
    process = RunningProcess.from_scheduling(process)  # Reads like English
    process = WaitingProcess.from_descheduling(process)  # Impossible


def tie_break(left: Process, right: Process) -> Process:
    """Tie break between two processes, to see which to potentially run next.

    This is totally how it works in real life, too. (source: my ass)

    Types aka classes work very well with pattern matching and its destructuring.
    Imagine destructuring a string or an int!
    """
    match left, right:
        case ReadyProcess(id=lid), ReadyProcess(id=rid):
            return left if lid < rid else rid  #  🟤
        case _:  # More stuff...
            return left
