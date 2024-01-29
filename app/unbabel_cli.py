"""
Unbabel CLI tool to calculate SMA of the translation delivery time for the last X minutes
"""

from typing import NamedTuple, Deque, TextIO
from json import loads
from math import floor
from datetime import datetime
from collections import deque
from argparse import ArgumentParser, ArgumentTypeError


OUTPUT_FILENAME = "output.json"


class Event(NamedTuple):
    """
    Class that stores information related to the translation events
    """

    epoch_minute: int
    duration: int

    @classmethod
    def from_input_line(cls, input_line: str):
        """
        Creates a new Event instance from an event string read from the file

        Args:
            input_line: The event string read from the file

        Returns:
            Event instance
        """
        event_json = loads(input_line)
        return cls(
            floor(
                int(datetime.fromisoformat(event_json["timestamp"]).timestamp()) / 60
            ),
            event_json["duration"],
        )


class Window:
    """
    Class that implements the SMA window
    """

    def __init__(self, window_size: int, initial_epoch_minute: int):
        """
        Initializes a new sliding window

        Args:
            size: The size of the sliding window
            initial_epoch_minute: The epoch minute of the first event
        """
        self.__window_size: int = window_size
        self.__events: Deque[Event] = deque()
        self.__start: int = initial_epoch_minute - self.__window_size
        self.__agg_duration: int = 0

    def add_event(self, event: Event):
        """
        Adds an event to the window events list and updates the aggregated duration

        Args:
            event: The event read from the input file
        """
        if self.__window_size == 0:
            return

        self.__events.append(event)
        self.__agg_duration += event.duration

    def slide(self):
        """
        Slides the window removing events outside the window and updating the aggregated duration
        """
        self.__start += 1

        for event_copy in self.__events.copy():
            if event_copy.epoch_minute < self.__start:
                self.__agg_duration -= self.__events.popleft().duration
            else:
                break

    def is_event_outside_window(self, event: Event):
        """
        Determines if an event is outside the window

        Args:
            event: The event read from the input file

        Returns:
            bool
        """
        return event.epoch_minute > self.__start + self.__window_size - 1

    def __calculate_average_delivery_time(self):
        """
        Calculates the average delivery time for the window events

        Returns:
            The average delivery time
        """
        if self.__agg_duration == 0:
            return 0

        return self.__agg_duration / len(self.__events)

    def __window_right_limit_to_timestamp(self):
        """
        Transforms the right limit epoch_minute of the window to a datetime

        Returns:
            Datetime
        """
        return (
            datetime
            .fromtimestamp((self.__start + self.__window_size) * 60)
            .strftime('%Y-%m-%d %H:%M:%S')    
        )

    def __str__(self):
        return (
            f"{{\"date\":\"{self.__window_right_limit_to_timestamp()}\", "
            f'"average_delivery_time":{self.__calculate_average_delivery_time()}}}'
        )


def sma_orchestrator(input_io: TextIO, window_size: int, output_io: TextIO):
    """
    Reads the event file line by line and prints the aggregated output
    """
    window: Window = None
    for line in input_io:
        event = Event.from_input_line(line)

        if window is None:
            window = Window(window_size, event.epoch_minute)

        while window.is_event_outside_window(event):
            output_io.write(f"{str(window)}\n")
            window.slide()

        window.add_event(event)
    else:
        if window is not None:
            output_io.write(str(window))


def non_negative_int(value: str):
    ivalue: int = int(value)
    if ivalue < 0:
        raise ArgumentTypeError(f"{value} is not a non negative integer")
    return ivalue


def main():
    """
    Module main function that parses the CLI arguments and calls the SMA orchestrator
    """
    parser = ArgumentParser(
        prog="Backend Engineering Challenge",
        description="Calculates the SMA of the translation delivery time for the last X minutes",
    )
    parser.add_argument(
        "--input_file", type=str, required=True, help="input events filename"
    )
    parser.add_argument(
        "--window_size", type=non_negative_int, required=True, help="SMA window size"
    )
    parser.add_argument(
        "--output_file", type=str, help="output filename", default=OUTPUT_FILENAME
    )
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as input_io:
        with open(args.output_file, "w", encoding="utf-8") as output_io:
            sma_orchestrator(input_io, args.window_size, output_io)


if __name__ == "__main__":
    main()
