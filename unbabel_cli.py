"""

"""

from typing import NamedTuple, Deque, TextIO
from json import loads
from math import floor
from datetime import datetime
from collections import deque


class Event(NamedTuple):
    """ """

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
    """ """

    def __init__(self, size: int, initial_epoch_minute: int):
        """
        Initializes a new sliding window

        Args:
            size: The size of the sliding window
            initial_epoch_minute: The epoch minute of the first event
        """
        self.__size: int = size
        self.__events: Deque[Event] = deque()
        self.__start: int = initial_epoch_minute - self.__size
        self.__agg_duration: int = 0

    def add_event(self, event: Event):
        """
        Adds an event to the window events list and updates the aggregated duration

        Args:
            event: The event read from the input file
        """
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
        return event.epoch_minute > self.__start + self.__size - 1

    def __calculate_average_delivery_time(self):
        """
        Calculates the average delivery time for the window events

        Returns:
            The average delivery time
        """
        if self.__agg_duration == 0:
            return 0

        return self.__agg_duration / len(self.__events)

    def __str__(self):
        return (
            f"{{\"date\":\"{datetime.fromtimestamp((self.__start + self.__size)*60).strftime('%Y-%m-%d %H:%M:%S')}\", "
            f'"average_delivery_time":{self.__calculate_average_delivery_time()}}}'
        )

def main():
    """ 
    """
    size = 10

    with open("events.json", "r", encoding="utf-8") as input_file:
        with open("output.json", "w", encoding="utf-8") as output_file:
            window = None

            for line in input_file:
                event = Event.from_input_line(line)

                if window is None:
                    window = Window(size, event.epoch_minute)

                while window.is_event_outside_window(event):
                    output_file.write(f"{str(window)}\n")
                    window.slide()

                window.add_event(event)
            else:
                output_file.write(str(window))

if __name__ == "__main__":
    main()
