import typing
from weakref import ref as weakref


class EventTrigger:

    def __init__(self):
        pass

    def trigger(self, event: "Event", **trigger_data):
        event.trigger(self, **trigger_data)


class EventListener:

    def __init__(self):
        self.__listened_events: dict = {}

    def __del__(self):
        for event in tuple(self.__listened_events.keys()):
            self.stop_listening(event)

    def listen_event(self, event: "Event", tasks: tuple, priority: int = 0):
        self.__listened_events[event] = tasks
        event.add_listener(self, priority)

    def stop_listening(self, event: "Event"):
        try:
            del self.__listened_events[event]
            event.remove_listener(self)
        except KeyError:
            pass

    def handle_event(self, event: "Event", trigger: EventTrigger, trigger_data: dict):
        for task in self.__listened_events[event]:
            task(self, trigger, trigger_data)


class Event:

    def __init__(self, name: str = "", arguments_template: tuple = ()):
        self.__name: str = name
        self.__listeners: list = [[]]
        self.__arguments_template: tuple = tuple(arguments_template)

    def __del__(self):
        for priority in tuple(self.__listeners):
            for weak_listener in priority:
                listener = weak_listener()
                if not listener is None:
                    listener.stop_listening(self)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def listeners(self) -> tuple:
        return tuple(tuple(listener) for listener in self.__listeners)

    @property
    def arguments_template(self) -> tuple:
        return tuple(self.__arguments_template)

    def add_listener(self, listener: EventListener, priority: int):
        try:
            self.__listeners[-priority - 1].append(weakref(listener))
        except IndexError:
            for i in range(priority + 1 - len(self.__listeners)):
                self.__listeners.append([])
            self.__listeners[-priority - 1].append(weakref(listener))

    def remove_listener(self, listener: EventListener):
        for priority in self.__listeners:
            for weak_listener in priority:
                current_listener = weak_listener()
                if current_listener is None or current_listener == listener:
                    priority.remove(weak_listener)

    def trigger(self, trigger: EventTrigger, **trigger_data: dict):
        for priority in self.__listeners:
            for listener in priority:
                ref_listener = listener()
                if not ref_listener is None:
                    ref_listener.handle_event(self, trigger, trigger_data)
