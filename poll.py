#!/usr/bin/python3

import random
import statistics

# Each state below is describe as a dict where the values represent the
# proportion of support for a fictitious candidate and the number of electoral
# votes that state has.
#
# Source: http://www.thegreenpapers.com/Census10/HouseAndElectors.phtml


# States, this should be in a JSON file!
california = {'proportion': 0.58, 'electoral_votes': 55}
florida = {'proportion': 0.49, 'electoral_votes': 29}
new_york = {'proportion': 0.55, 'electoral_votes': 29}
north_carolina = {'proportion': 0.48, 'electoral_votes': 15}
south_carolina = {'proportion': 0.44, 'electoral_votes': 9}
texas = {'proportion': 0.46, 'electoral_votes': 38}
wyomoing = {'proportion': 0.41, 'electoral_votes': 3}

states = [california, florida, new_york, north_carolina, south_carolina, texas, wyomoing]


# Functions
def voter_in_favor(population_proportion, precision=10000):
    value = random.randrange(0, precision) / precision

    return value < population_proportion


def get_poll_result(population_proportion, sample_size):
    count = 0

    for _ in range(sample_size):
        if voter_in_favor(population_proportion):
            count += 1

    return count / sample_size


def get_total_electoral_votes(states):
    count = 0

    for state in states:
        count += state['electoral_votes']

    return count

def get_electoral_votes_needed(available_electoral_votes):
    return available_electoral_votes / 2 + 1


def get_actual_election_result(states, verbose=True):
    total_electoral_votes = get_total_electoral_votes(states)
    electoral_votes_needed = get_electoral_votes_needed(total_electoral_votes)

    electoral_votes_earned = 0

    for state in states:
        if state['proportion'] > 0.5:
            electoral_votes_earned += state['electoral_votes']

    if electoral_votes_earned >= electoral_votes_needed:
        win = True
    else:
        win = False

    if verbose:
        print("{} of {} electoral votes are needed.".format(electoral_votes_needed, total_electoral_votes))
        if win:
            print("The candidate will actually win with {} electoral votes.".format(electoral_votes_earned))
        else:
            print("The candidate will actually lose with {} electoral votes.".format(electoral_votes_earned))

    return win


def get_national_election_prediction(states, sample_size, verbose=True):
    total_electoral_votes = 0
    electoral_votes_won = 0

    for state in states:
        population_proportion = state['proportion']
        total_electoral_votes += state['electoral_votes']

        if get_poll_result(population_proportion, sample_size) > 0.5:
            electoral_votes_won += state['electoral_votes']

    electoral_votes_needed = total_electoral_votes // 2 + 1

    if electoral_votes_won >= electoral_votes_needed:
        win = True
    else:
        win = False

    if verbose:
        print("Total electoral votes: {}".format(total_electoral_votes))
        print("Electoral votes needed: {}".format(electoral_votes_needed))
        print("Electoral votes won: {}".format(electoral_votes_won))
        if win:
            print("The predicted result is a win")
        else:
            print("The predicted result is a loss")

    return win


# Show actual election Results
win = get_actual_election_result(states)
print(win)
print()


# Simulation settings
poll_size = 1000
trials = 1000

# Test one voter
print("Single voter simulation...")
test_proportion = 0.53
print("Results:")
print(voter_in_favor(test_proportion))
print(voter_in_favor(test_proportion))
print(voter_in_favor(test_proportion))
print(voter_in_favor(test_proportion))
print(voter_in_favor(test_proportion))
print()


# Test one state
print("Single state simulation...")
expected = florida['proportion']
print("Expected: {}".format(expected))
print("Poll size: {}".format(poll_size))
print("Results:")
print(get_poll_result(expected, poll_size))
print(get_poll_result(expected, poll_size))
print(get_poll_result(expected, poll_size))
print(get_poll_result(expected, poll_size))
print(get_poll_result(expected, poll_size))
print()


# Simulate multiple polls of one states
print("Single state simulation (multiple polls)...")
expected = florida['proportion']

results = []
for i in range(trials):
    sample_proportion = get_poll_result(expected, poll_size)
    results.append(sample_proportion)

low = min(results)
high = max(results)
diff = high - low
mean = statistics.mean(results)
standard_deviation = statistics.stdev(results)
margin_of_error = 1.96 * standard_deviation # this is an estimate to show emperical rule works

count_within_moe = 0
for r in results:
    if expected - margin_of_error <= r <= expected + margin_of_error:
        count_within_moe += 1

percent_within_moe = count_within_moe / trials

print("Results:")
print("Expected: {}".format(expected))
print("Poll size: {}".format(poll_size))
print("Trials: {}".format(trials))
print("Low: {}".format(low))
print("High: {}".format(high))
print("Range: {}".format(diff))
print("Mean: {}".format(mean))
print("Standard Deviation: {}".format(standard_deviation))
print("Margin of Error (estimate): {}".format(margin_of_error))
print("Count within Margin of Error: {}".format(count_within_moe))
print("Percent within Margin of Error: {}".format(percent_within_moe))
print()


# Predict national election (1 trial)
print("National simulation (1 trial)...")
win_predicted = get_national_election_prediction(states, poll_size)
print(win_predicted)
print()

# Predict many national elections
win_count = 0

for n in range(trials):
    win = get_national_election_prediction(states, poll_size, False)

    if win:
        win_count += 1

win_probability = win_count / trials
print("National simulation (many trials)...")
print("Poll size: {}".format(poll_size))
print("Trials: {}".format(trials))
print("Results:")
print("A win was predicted in {} of {} national polls".format(win_count, trials))
print("The estimated probability that the candidate will win is {}.".format(win_probability))
