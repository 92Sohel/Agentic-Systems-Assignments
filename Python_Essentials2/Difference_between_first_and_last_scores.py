class StudentPerformance:
    def __init__(self, scores):
        self.scores = scores

    def score_difference(self):
        try:
            if len(self.scores) == 0:
                raise ValueError

            first = self.scores[0]
            last = self.scores[-1]

            difference = last - first

            print("Difference between last and first score is:", difference)

        except ValueError:
            print("No scores available to calculate difference")


# Example Input
scores = [55, 65, 75, 85]

student = StudentPerformance(scores)
student.score_difference()