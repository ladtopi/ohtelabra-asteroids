import threading
from time import sleep
import unittest
from unittest.mock import Mock

import pygame

from loop import GameLoop
from state.base import BaseGameState
from tests._stubs import DisplayStub, EventQueueStub, KeyboardStub


class GameStateStub(BaseGameState):
    pass


class TestLoop(unittest.TestCase):
    def setUp(self):
        self.state_a = Mock(wraps=GameStateStub())
        self.state_b = Mock(wraps=GameStateStub())
        self.events = EventQueueStub()
        self.keyboard = KeyboardStub()

        self.loop = GameLoop(
            state_map={"a": self.state_a, "b": self.state_b},
            starting_state="a",
            screen=DisplayStub(),
            event_queue=self.events,
            keyboard=self.keyboard,
            frame_callback=lambda: None)

        # run in bg thread
        self.loop_thread = threading.Thread(target=self.loop.run)
        self.loop_thread.start()

    def tearDown(self):
        self.loop.quit()
        self.loop_thread.join()

    def next_frame(self):
        sleep(0.1)

    def test_loop_initially_in_starting_state(self):
        self.assertEqual(self.loop.state, self.state_a)

    def test_loop_moves_to_next_state_if_requested(self):
        self.state_a.request_transition("b")
        self.next_frame()
        self.assertEqual(self.loop.state, self.state_b)

    def test_loop_breaks_on_quit(self):
        self.events.post(pygame.event.Event(pygame.QUIT))
        self.next_frame()
        self.assertFalse(self.loop.running)

    def test_loop_breaks_on_esc(self):
        self.keyboard.set_pressed(pygame.K_ESCAPE)
        self.next_frame()
        self.assertFalse(self.loop.running)

    def test_loop_passes_other_events_to_current_state(self):
        self.events.post(pygame.event.Event(
            pygame.KEYDOWN, key=pygame.K_RETURN))
        self.next_frame()
        self.state_a.handle_events.assert_called_with(self.events.get())

    def test_loop_passes_other_keys_to_current_state(self):
        self.keyboard.set_pressed(pygame.K_0)
        self.next_frame()
        self.state_a.handle_keys.assert_called_with(
            self.keyboard.get_pressed())
