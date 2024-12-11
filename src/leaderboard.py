class LeaderboardEntry:
    def __init__(self, name, score, bullets_used):
        self.name = name
        self.score = score
        self.bullets_used = bullets_used

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    def __str__(self):
        return f"{self.name}: {self.score}"


class Leaderboard:
    def __init__(self):
        self.leaderboard = []

    def submit_score(self, name, score):
        self.leaderboard.append(LeaderboardEntry(
            name, score.score, score.bullets_used))
        self.leaderboard.sort(reverse=True)

    def get_top_10(self):
        return self.leaderboard[:10]

    def __str__(self):
        return "\n".join(str(entry) for entry in self.leaderboard)
