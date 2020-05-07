import numpy as np
import pandas as pd

class ScoreChart:
    """ScoreChart is an object that's basically a pandas dataframe
    rows are rounds, columns are players"""

    def __init__(self, list_of_players):
        zeros = np.zeros(len(list_of_players), int)
        zeros = np.array([zeros])
        players_names = [player.name for player in list_of_players]
        self.dataframe = pd.DataFrame(index=["Round 1"], data=zeros, columns=players_names)

    def update_scores(self, rounds, list_of_players):
        """Adds scores from last round in the score chart"""
        scores = [player.score() for player in list_of_players]
        scores = np.array([scores])
        # score_chart = self.dataframe
        if rounds == 1:
            self.dataframe.iloc[0] = scores
            self.compute_totals_scores()
        else:
            new_row_scores = pd.DataFrame(index=["Round {}".format(rounds)], data=scores, columns=self.dataframe.columns)
            self.dataframe = self.dataframe.drop(index="Totals")
            self.dataframe = pd.concat([self.dataframe, new_row_scores])
            self.compute_totals_scores()

    def compute_totals_scores(self):
        """sums up the scores of everyplayer an stores it in the final line"""
        final_scores = [sum(self.dataframe[player]) for player in self.dataframe.columns]
        final_scores = np.array([final_scores])
        total_row = pd.DataFrame(index=["Totals"], data=final_scores, columns=self.dataframe.columns)
        self.dataframe = pd.concat([self.dataframe, total_row])
        print("Here's the Scores' Chart !!!")
        print(self.dataframe)

    def determine_winner(self):
        """Determines the winner using
        score chart's last line"""
        final_scores = self.dataframe.loc["Totals"]
        winner = final_scores.idxmin()
        print("\nThe winner is : {} !!!".format(winner.upper()))