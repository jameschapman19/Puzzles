import itertools

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from baseball.solution import simulate_inning


def evaluate_batting_orders(prob_single, prob_home_run, simulations=50000):
    """
    Evaluate all possible positions for the two sluggers in the batting order.
    :param prob_single: Probability of getting a single for a contact hitter.
    :param prob_home_run: Probability of getting a home run for the sluggers.
    :param simulations: Number of games to simulate for each slugger positions combination.
    :return: The optimal positions for the sluggers and average runs for each combination.
    """
    best_positions = (0, 0)
    best_average_runs = 0
    average_runs_combinations = []

    # Iterate over all possible combinations of two slugger positions
    for slugger_positions in itertools.combinations(range(9), 2):
        batting_order = [False] * 9
        for pos in slugger_positions:
            batting_order[pos] = True

        total_runs = 0
        # Simulate nine innings for a number of games
        for _ in range(simulations):
            for _ in range(9):
                total_runs += simulate_inning(batting_order, prob_single, prob_home_run)

        average_runs = total_runs / simulations
        average_runs_combinations.append((slugger_positions, average_runs))

        if average_runs > best_average_runs:
            best_average_runs = average_runs
            best_positions = slugger_positions

    # Create a matrix to represent the heatmap
    average_runs_matrix = np.zeros((9, 9))
    for combination, avg_runs in average_runs_combinations:
        average_runs_matrix[combination[0], combination[1]] = avg_runs
        average_runs_matrix[combination[1], combination[0]] = avg_runs

    return best_positions, average_runs_matrix


# Parameters
prob_single = 1 / 3
prob_home_run = 1 / 10
simulations = 50000

# Get the best positions for the sluggers and average runs for each combination
best_positions, average_runs_matrix = evaluate_batting_orders(prob_single, prob_home_run, simulations)

print(f"The best positions for the sluggers are: {best_positions[0] + 1} and {best_positions[1] + 1}")

# Create a heatmap
sns.heatmap(average_runs_matrix, annot=True, cmap='YlGnBu')
plt.xlabel('Slugger 1 Position', weight='bold', fontsize=10)
plt.ylabel('Slugger 2 Position', weight='bold', fontsize=10)
plt.title('Average Runs Scored over Nine Innings', wrap=True, weight='bold', fontsize=12)
plt.xticks(np.arange(9) + 0.5, np.arange(1, 10), weight='bold', fontsize=8)
plt.yticks(np.arange(9) + 0.5, np.arange(1, 10), weight='bold', fontsize=8)
plt.tight_layout()
plt.show()