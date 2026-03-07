class StudentScores:
    def __init__(self, scores):
        self.scores = scores

    def highest_last_two(self):
        try:
            if len(self.scores) < 2:
                raise ValueError

            last = self.scores[-1]
            second_last = self.scores[-2]

            highest = max(last, second_last)

            print("Highest score among last two is:", highest)

        except ValueError:
            print("Not enough scores to find highest value")


# Example Input
scores = [45, 67, 89, 72]

student = StudentScores(scores)
student.highest_last_two()