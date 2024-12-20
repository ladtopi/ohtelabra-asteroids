
from dataclasses import dataclass


@dataclass
class LeaderboardEntry:
    name: str
    score: int
    bullets_used: int


class Leaderboard:
    def __init__(self, db):
        self._db = db

    def add_entry(self, entry):
        self._db.exec("INSERT INTO leaderboard (name, score, bullets) VALUES (?, ?, ?)",
                      entry.name, entry.score, entry.bullets_used)

    def get_top_list(self):
        return [LeaderboardEntry(*entry) for entry in self._db.fetchall(
            "SELECT name, score, bullets FROM leaderboard ORDER BY score DESC LIMIT 5")]
