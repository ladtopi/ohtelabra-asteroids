import unittest
from unittest.mock import Mock

from collisions import CollisionChecker
from events import EVENT_SPAWN_SHIP
from game import Game


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


class TestGame(unittest.TestCase):
    def setUp(self):
        self.events = EventQueueStub()
        self.collision_checker = Mock(wraps=CollisionChecker())
        self.collision_checker.get_collision = Mock(return_value=None)
        self.game = Game(self.collision_checker,
                         self.events,
                         DisplayStub())
        self.game.reset()

    def test_score_is_initially_zero(self):
        self.game.reset()
        self.assertEqual(self.game.score, 0)

    def test_ship_is_initially_alive(self):
        self.assertTrue(self.game.ship is not None)
        self.assertTrue(self.game.ship.alive())

    def test_game_has_asteroids(self):
        self.game.reset()
        self.assertGreater(len(self.game.asteroids), 0)

    def test_fire_ship_adds_bullet(self):
        self.game.fire_ship()
        self.assertEqual(len(self.game.bullets), 1)

    def test_kill_ship_decreases_remaining_ships(self):
        self.game.kill_ship()
        self.assertEqual(self.game.ships_remaining, 2)

    def test_kill_ship_schedules_respawn_if_ships_remain(self):
        self.game.kill_ship()
        self.assertEqual(self.events.deferred_events,
                         [(EVENT_SPAWN_SHIP, 1000)])

    def test_kill_ship_does_not_schedule_respawn_if_no_ships_remain(self):
        for _ in range(self.game.ships_remaining):
            self.game.kill_ship()
        self.events.clear()
        self.game.kill_ship()
        self.assertEqual(self.events.deferred_events, [])

    def test_kill_bullet_removes_bullet(self):
        bullet = self.game.fire_ship()
        self.game.kill_bullet(bullet)
        self.assertEqual(len(self.game.bullets), 0)

    def test_explode_asteroid_removes_asteroid(self):
        asteroid = self.game.spawn_asteroid(400, 300, 0, 0)
        self.game.explode_asteroid(asteroid)
        self.assertFalse(self.game.objects.has(asteroid))

    def test_explode_asteroid_creates_fragments(self):
        asteroid = self.game.spawn_asteroid(400, 300, 0, 0)
        frags = self.game.explode_asteroid(asteroid)
        self.assertGreater(len(frags), 0)

    def test_explode_asteroid_adds_fragments_to_game(self):
        asteroid = self.game.spawn_asteroid(400, 300, 0, 0)
        frags = self.game.explode_asteroid(asteroid)
        self.assertTrue(all(self.game.objects.has(frag) for frag in frags))

    def test_update_moves_ship(self):
        self.game.thrust_ship()
        ppos = self.game.ship.position
        self.game.update()
        self.game.update()
        self.game.update()
        self.assertNotEqual(ppos, self.game.ship.position)

    def test_update_moves_asteroids(self):
        asteroid = self.game.spawn_asteroid(400, 300, .5, .5)
        ppos = asteroid.position
        self.game.update()
        self.assertNotEqual(ppos, asteroid.position)

    def test_update_checks_collisions_between_bullet_and_asteroids(self):
        bullet = self.game.fire_ship()
        self.game.update()
        self.collision_checker.get_collision.assert_any_call(
            bullet, self.game.asteroids)

    def test_update_checks_collisions_between_ship_and_asteroids(self):
        self.game.update()
        self.collision_checker.get_collision.assert_any_call(
            self.game.ship, self.game.asteroids)
