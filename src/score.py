class Score:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.bullets_used = 0

    def award_pts(self, points):
        self.score += points

    def use_bullet(self):
        self.bullets_used += 1

    def __eq__(self, other):
        if isinstance(other, Score):
            return self.score == other.score
        if isinstance(other, int):
            return self.score == other
        return False

    def __str__(self):
        return str(self.score)
