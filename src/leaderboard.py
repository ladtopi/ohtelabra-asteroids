
from dataclasses import dataclass


@dataclass
class LeaderboardEntry:
    name: str
    score: int
    bullets_used: int

    @staticmethod
    def from_score(name, score):
        return LeaderboardEntry(name, score.score, score.bullets_used)


class Leaderboard:
    def __init__(self, db):
        self._db = db

    def add_entry(self, entry):
        self._db.exec("INSERT INTO leaderboard (name, score, bullets) VALUES (?, ?, ?)",
                      entry.name, entry.score, entry.bullets_used)

    def get_top_10(self):
        return [LeaderboardEntry(*entry) for entry in self._db.fetchall(
            "SELECT name, score, bullets FROM leaderboard ORDER BY score DESC LIMIT 10")]
