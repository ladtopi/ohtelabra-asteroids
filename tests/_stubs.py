from collections import defaultdict


class DisplayStub:
    def get_size(self):
        return (800, 600)


class EventQueueStub:
    def __init__(self):
        self.events = []
        self.deferred_events = []

    def get(self):
        return self.events

    def post(self, event):
        self.events.append(event)
        return self

    def defer(self, event, ms):
        self.deferred_events.append((event, ms))
        return self

    def clear(self):
        self.events = []
        self.deferred_events = []


class KeyboardStub:
    def __init__(self):
        self._pressed = defaultdict(int)

    def get_pressed(self):
        return self._pressed

    def set_pressed(self, key):
        self._pressed.update({key: 1})
        return self
