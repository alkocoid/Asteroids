import json

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.leaderboard = []
        self.leaderboard = self.load_leaderboard()

    def add_points(self, points):
        self.score += points

    def reset(self):
        self.score = 0

    def submit_score(self, name):
        self.leaderboard.append((name, self.score))
        self.leaderboard.sort(key=lambda entry: entry[1], reverse=True)
        self.leaderboard = self.leaderboard[:10]
        self.save_leaderboard()
    
    def save_leaderboard(self, path="leaderboard.json"):
        with open(path, "w") as f:
            json.dump(self.leaderboard, f)

    def load_leaderboard(self, path="leaderboard.json"):
        try:
            with open(path) as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        
    def is_high_score(self):
        if len(self.leaderboard) < 10:
            return True
        return self.score > self.leaderboard[-1][1]