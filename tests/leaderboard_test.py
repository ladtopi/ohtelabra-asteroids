import unittest

from db import Database
from leaderboard import Leaderboard, LeaderboardEntry


class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.leaderboard = Leaderboard(self.db)

    def test_add_entry_accepts_leaderboard_entry(self):
        entry = LeaderboardEntry("test", 100, 10)
        try:
            self.leaderboard.add_entry(entry)
        except Exception:
            self.fail("add_entry raised an exception")

    def test_get_top_10_returns_list_of_leaderboard_entries(self):
        entries = [
            LeaderboardEntry("test1", 100, 10),
            LeaderboardEntry("test2", 101, 20),
            LeaderboardEntry("test3", 102, 30),
        ]
        for entry in entries:
            self.leaderboard.add_entry(entry)
        top_10 = self.leaderboard.get_top_list()

        self.assertCountEqual(top_10, entries)

    def test_get_top_10_returns_list_of_leaderboard_entries_in_descending_score_order(self):
        entries = [
            LeaderboardEntry("test1", 100, 20),
            LeaderboardEntry("test2", 101, 0),
            LeaderboardEntry("test3", 102, 30),
        ]
        for entry in entries:
            self.leaderboard.add_entry(entry)
        top_10 = self.leaderboard.get_top_list()

        self.assertEqual(top_10, sorted(
            entries, key=lambda e: e.score, reverse=True))
