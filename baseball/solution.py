import random
import matplotlib.pyplot as plt
import matplotlib.style as style
from numba import jit

def simulate_batter(is_slugger, prob_single, prob_home_run):
    """
    Simulate the result of a batter.
    :param is_slugger: Whether the batter is the home run slugger or not.
    :param prob_single: Probability of getting a single for a contact hitter.
    :param prob_home_run: Probability of getting a home run for the slugger.
    :return: Number of bases advanced.
    """
    if is_slugger:
        return 4 if random.random() < prob_home_run else 0
    else:
        return 1 if random.random() < prob_single else 0

def simulate_inning(batting_order, prob_single, prob_home_run):
    """
    Simulate an inning with the given batting order.
    :param batting_order: A list representing the batting order.
    :param prob_single: Probability of getting a single for a contact hitter.
    :param prob_home_run: Probability of getting a home run for the slugger.
    :return: Total runs scored in the inning.
    """
    bases = [False] * 3
    runs = 0
    outs = 0
    batter_index = 0

    while outs < 3:
        bases_advanced = simulate_batter(batting_order[batter_index], prob_single, prob_home_run)

        # Handle home run separately
        if bases_advanced == 4:
            runs += sum(bases) + 1
            bases = [False] * 3
        else:
            # Move runners
            for i in range(2, -1, -1):
                if bases[i]:
                    if i + bases_advanced > 2:
                        runs += 1
                    else:
                        bases[i + bases_advanced] = True
                    bases[i] = False

            # Place the batter on base if he hit a single
            if bases_advanced == 1:
                bases[0] = True
            else:
                outs += 1

        # Move to the next batter
        batter_index = (batter_index + 1) % 9

    return runs

def evaluate_batting_orders(prob_single, prob_home_run, simulations=50000):
    """
    Evaluate all possible positions for the slugger in the batting order.
    :param prob_single: Probability of getting a single for a contact hitter.
    :param prob_home_run: Probability of getting a home run for the slugger.
    :param simulations: Number of innings to simulate for each slugger position.
    :return: The optimal position for the slugger.
    """
    best_position = 0
    best_average_runs = 0

    for slugger_position in range(9):
        batting_order = [False] * 9
        batting_order[slugger_position] = True
        total_runs = 0

        for _ in range(simulations):
            total_runs += simulate_inning(batting_order, prob_single, prob_home_run)

        average_runs = total_runs / simulations
        if average_runs > best_average_runs:
            best_average_runs = average_runs
            best_position = slugger_position

    return best_position + 1

def evaluate_batting_orders(prob_single, prob_home_run, simulations=50000):
    """
    Evaluate all possible positions for the slugger in the batting order.
    :param prob_single: Probability of getting a single for a contact hitter.
    :param prob_home_run: Probability of getting a home run for the slugger.
    :param simulations: Number of innings to simulate for each slugger position.
    :return: The optimal position for the slugger and average runs for each position.
    """
    best_position = 0
    best_average_runs = 0
    average_runs_list = []

    for slugger_position in range(9):
        batting_order = [False] * 9
        batting_order[slugger_position] = True
        total_runs = 0

        for _ in range(simulations):
            total_runs += simulate_inning(batting_order, prob_single, prob_home_run)

        average_runs = total_runs / simulations
        average_runs_list.append(average_runs)

        if average_runs > best_average_runs:
            best_average_runs = average_runs
            best_position = slugger_position

    return best_position + 1, average_runs_list

# Parameters
prob_single = 1 / 3
prob_home_run = 1 / 10
simulations = 2000000

# Get the best position for the slugger and average runs for each position
best_position, average_runs_list = evaluate_batting_orders(prob_single, prob_home_run, simulations)

# Plotting the results with FiveThirtyEight style
style.use('fivethirtyeight')
plt.plot(range(1, 10), average_runs_list, marker='o')
plt.xlabel('Slugger Position in Lineup')
plt.ylabel('Average Runs Scored')
plt.title('Average Runs Scored for Each Slugger Position',wrap=True)
plt.axvline(x=best_position, color='r', linestyle='--', label=f'Optimal Position: {best_position}')
plt.xticks(range(1, 10))
plt.legend()
plt.tight_layout()
plt.show()

print(f"The best position for the slugger is: {best_position}")