#!/usr/bin/env python3
import typing
import random


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    PLAYERS = ["alic", "bob", "charlie", "dylan"]
    ACTIONS = [
        "run", "jump", "swim", "climb", "grab",
        "release", "move", "eat", "sleep", "use"
        ]
    while True:
        name = random.choice(PLAYERS)
        action = random.choice(ACTIONS)
        yield (name, action)


def consume_event(
        event_list: list[tuple[str, str]]
        ) -> typing.Generator[tuple[str, str], None, None]:
    while len(event_list) > 0:
        index = random.randrange(len(event_list))
        event = event_list.pop(index)
        yield event


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===")
    stream = gen_event()
    for i in range(1000):
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")

    stream2 = gen_event()
    event_list = []
    for i in range(10):
        event_list += [next(stream2)]
    print(f"Built list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")
