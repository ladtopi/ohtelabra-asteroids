import unittest
from unittest.mock import Mock

from collisions import CollisionChecker
from core.asteroid import Asteroid
from core.game import Game
from events import EVENT_SPAWN_ASTEROID_WAVE, EVENT_SPAWN_SHIP
from tests._stubs import DisplayStub, EventQueueStub


class TestGame(unittest.TestCase):
    def setUp(self):
        self.events = EventQueueStub()
        self.collision_checker = Mock(wraps=CollisionChecker())
        self.collision_checker.get_collision = Mock(return_value=None)
        self.game = Game(collision_checker=self.collision_checker,
                         event_queue=self.events,
                         display=DisplayStub())
        self.game.reset()

    def test_score_is_initially_zero(self):
        self.game.reset()
        self.assertEqual(self.game.score, 0)

    def test_ship_is_initially_alive(self):
        self.assertTrue(self.game.ship is not None)
        self.assertTrue(self.game.ship.alive())

    def test_game_has_asteroids(self):
        self.game.reset()
        self.assertGreater(self.game.asteroids_remaining, 0)

    def test_fire_ship_adds_bullet(self):
        bullet = self.game.fire_ship()
        self.assertTrue(self.game.objects.has(bullet))

    def test_fire_decreases_bullets_remaining(self):
        n = self.game.bullets_remaining
        self.game.fire_ship()
        self.assertEqual(self.game.bullets_remaining, n-1)

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
        self.assertFalse(self.game.objects.has(bullet))

    def test_nuke_asteroids_removes_all_asteroids(self):
        self.game.nuke_asteroids()
        self.assertEqual(self.game.asteroids_remaining, 0)

    def test_explode_asteroid_removes_asteroid(self):
        asteroid = Asteroid()
        self.game.place_asteroid(asteroid)
        self.game.explode_asteroid(asteroid)
        self.assertFalse(self.game.objects.has(asteroid))

    def test_explode_asteroid_creates_fragments(self):
        asteroid = Asteroid()
        self.game.place_asteroid(asteroid)
        frags = self.game.explode_asteroid(asteroid)
        self.assertGreater(len(frags), 0)

    def test_explode_asteroid_adds_fragments_to_game(self):
        asteroid = Asteroid()
        self.game.place_asteroid(asteroid)
        frags = self.game.explode_asteroid(asteroid)
        self.assertTrue(all(self.game.objects.has(frag) for frag in frags))

    def test_explode_schedules_new_wave_if_no_asteroids_remain(self):
        self.game.nuke_asteroids()
        asteroid = Asteroid()
        self.game.place_asteroid(asteroid)
        self.game.explode_asteroid(asteroid)
        self.assertEqual(self.events.deferred_events,
                         [(EVENT_SPAWN_ASTEROID_WAVE, 1000)])

    def test_update_moves_ship(self):
        self.game.thrust_ship()
        ppos = self.game.ship.position
        self.game.update()
        self.game.update()
        self.game.update()
        self.assertNotEqual(ppos, self.game.ship.position)

    def test_update_moves_asteroids(self):
        asteroid = Asteroid(velocity=(1, 1))
        self.game.place_asteroid(asteroid)
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

    def test_ship_cannot_fire_if_not_alive(self):
        self.game.kill_ship()
        self.assertIsNone(self.game.fire_ship())

    def test_spawn_ship_places_new_ship(self):
        self.game.kill_ship()
        ship = self.game.spawn_ship()
        self.assertEqual(self.game.ship, ship)
