import unittest
from unittest.mock import Mock

from collisions import CollisionChecker
from events import EVENT_SPAWN_SHIP
from state import GameState


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

    def defer(self, event, ms):
        self.deferred_events.append((event, ms))

    def clear(self):
        self.events = []
        self.deferred_events = []


class TestGameStateReset(unittest.TestCase):
    def setUp(self):
        self.events = EventQueueStub()
        self.collision_checker = CollisionChecker()
        self.state = GameState(self.collision_checker,
                               self.events, DisplayStub())

    def test_state_should_be_empty_first(self):
        self.state = GameState(self.collision_checker,
                               self.events, DisplayStub())
        self.assertEqual(len(self.state.objects), 0)
        self.assertEqual(self.state.ship, None)
        self.assertEqual(self.state.score, None)
        self.assertEqual(self.state.ships_remaining, None)

    def test_score_is_zero_after_reset(self):
        self.state.reset()
        self.assertEqual(self.state.score, 0)

    def test_reset_spawns_ship(self):
        self.state.reset()
        self.assertTrue(self.state.ship is not None)
        self.assertTrue(self.state.ship.alive())

    def test_reset_should_spawn_asteroids(self):
        self.state.reset()
        self.assertGreater(len(self.state.asteroids), 0)


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.events = EventQueueStub()
        self.collision_checker = Mock(wraps=CollisionChecker())
        self.collision_checker.get_collision = Mock(return_value=None)
        self.state = GameState(self.collision_checker,
                               self.events, DisplayStub())
        self.state.reset()

    def test_fire_ship_adds_bullet(self):
        self.state.fire_ship()
        self.assertEqual(len(self.state.bullets), 1)

    def test_kill_ship_decreases_remaining_ships(self):
        self.state.kill_ship()
        self.assertEqual(self.state.ships_remaining, 2)

    def test_kill_ship_schedules_respawn_if_ships_remain(self):
        self.state.kill_ship()
        self.assertEqual(self.events.deferred_events,
                         [(EVENT_SPAWN_SHIP, 1000)])

    def test_kill_ship_does_not_schedule_respawn_if_no_ships_remain(self):
        for _ in range(self.state.ships_remaining):
            self.state.kill_ship()
        self.events.clear()
        self.state.kill_ship()
        self.assertEqual(self.events.deferred_events, [])

    def test_kill_bullet_removes_bullet(self):
        bullet = self.state.fire_ship()
        self.state.kill_bullet(bullet)
        self.assertEqual(len(self.state.bullets), 0)

    def test_explode_asteroid_removes_asteroid(self):
        asteroid = self.state.spawn_asteroid(400, 300, 0, 0)
        self.state.explode_asteroid(asteroid)
        self.assertFalse(self.state.objects.has(asteroid))

    def test_explode_asteroid_creates_fragments(self):
        asteroid = self.state.spawn_asteroid(400, 300, 0, 0)
        frags = self.state.explode_asteroid(asteroid)
        self.assertGreater(len(frags), 0)

    def test_explode_asteroid_adds_fragments_to_game(self):
        asteroid = self.state.spawn_asteroid(400, 300, 0, 0)
        frags = self.state.explode_asteroid(asteroid)
        self.assertTrue(all(self.state.objects.has(frag) for frag in frags))

    def test_update_moves_ship(self):
        self.state.thrust_ship()
        ppos = self.state.ship.position
        self.state.update()
        self.state.update()
        self.state.update()
        self.assertNotEqual(ppos, self.state.ship.position)

    def test_update_moves_asteroids(self):
        asteroid = self.state.spawn_asteroid(400, 300, .5, .5)
        ppos = asteroid.position
        self.state.update()
        self.assertNotEqual(ppos, asteroid.position)

    def test_update_checks_collisions_between_bullet_and_asteroids(self):
        bullet = self.state.fire_ship()
        self.state.update()
        self.collision_checker.get_collision.assert_any_call(
            bullet, self.state.asteroids)

    def test_update_checks_collisions_between_ship_and_asteroids(self):
        self.state.update()
        self.collision_checker.get_collision.assert_any_call(
            self.state.ship, self.state.asteroids)
