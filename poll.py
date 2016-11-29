import random
import statistics

# Each state below is describe as a tuple where the values represent
# (state population, proportion of support for a candidate, electoral votes)
# Population figures are based on 2010 census. The support for a candidate
# is fictitious.
#
# Source:
# http://www.thegreenpapers.com/Census10/HouseAndElectors.phtml

CALIFORNIA = (0.58, 55)
FLORIDA = (0.49 , 29)
NEW_YORK = (0.55, 29)
NORTH_CAROLINA = (0.48, 15)
SOUTH_CAROLINA = (0.44, 9)
TEXAS = (0.47, 38)
WYOMING = (0.39, 3)

states = [CALIFORNIA, FLORIDA, NEW_YORK, NORTH_CAROLINA,
          SOUTH_CAROLINA, TEXAS, WYOMING]


# Functions
def get_poll_result(state, sample_size):

    actual_in_favor = state[0]
    polled_in_favor = 0
    count = 0

    while count < sample_size:
        result = random.randrange(0, 100) / 100

        if result < actual_in_favor:
            polled_in_favor += 1

        count += 1

    return polled_in_favor / count


def get_avg(sample_list):
    pass

def get_range(sample_list):
    return 

def count_wins(sample_list):
    count = 0
    for result in sample_list:
        if result > 0.50:
            count += 1

    return count

def show_poll_stats(state, sample_list):
    expected = state[0]
    
    high = max(sample_list)
    low = min(sample_list)
    diff = high - low
    mean = sum(sample_list) / len(sample_list)
    st_dev = statistics.stdev(sample_list)
    wins = count_wins(sample_list)

    print("Expected: {}".format(expected))
    print("High: {}".format(high))
    print("Low: {}".format(low))
    print("Range: {}".format(diff))
    print("St. Dev: {}".format(st_dev))
    print("Mean: {}".format(mean))
    print("Predicted wins: {} / {}".format(wins, trials))

    moe = 1.96 * st_dev # 95% confidence
    
    count = 0
    for p in sample_list:
        if mean - moe < p < mean + moe:
            count += 1
            
    percent_within_two = count / trials
    
    print ("{} / {} trials within two SD of mean".format(count, trials))
    print ("{} is the proportion within two SD of mean".format(percent_within_two))
    print ("The margin of error is about {}.".format(moe))


# Simulation settings
poll_size = 1000
trials = 1000


# Test one state
print("Single state simulation...")
state = FLORIDA
expected = state[1]
results = []

for i in range(trials):
    r = get_poll_result(state, poll_size)
    results.append(r)

show_poll_stats(state, results)
print()

# Predict national election (1 trial)
print("National simulation...")
total_electoral_votes = 0
for s in states:
    total_electoral_votes += s[1]

electoral_votes_needed = total_electoral_votes // 2 + 1

print("Total electoral votes: {}".format(total_electoral_votes))
print("Electoral votes needed: {}".format(electoral_votes_needed))
print()

electoral_votes_earned = 0
for s in states:
    result = get_poll_result(s, poll_size)
    
    if result > 0.5:
        electoral_votes_earned += s[1]

print("{} / {} electoral votes are expected based on actual support.".format(electoral_votes_earned, total_electoral_votes))

if electoral_votes_earned >= electoral_votes_earned:
    print("The candidate will win.")
else:
    print("The candidate will to lose.")
print()


# Make many predictions of national election
predicted_wins = 0

for n in range(trials):
    electoral_votes_earned = 0
    
    for s in states:
        result = get_poll_result(s, poll_size)
        
        if result > 0.5:
             electoral_votes_earned += s[1]
             
    if electoral_votes_earned > electoral_votes_needed:
        predicted_wins += 1

print("A win was predicted in {} / {} trials.".format(predicted_wins, trials))

# Get 'actual' result
actual_electoral_votes_earned = 0

for s in states:
    if s[1] > 0.5:
        actual_electoral_votes_earned += s[1]

if actual_electoral_votes_earned >= electoral_votes_needed:
    print("The candidate will actually win with {} electoral votes.".format(actual_electoral_votes_earned))
else:
    print("The candidate will actually lose with {} electoral votes.".format(actual_electoral_votes_earned))


'''
to do...

Incorporate popular vote into the simulation (perhaps assume 50% turn out)
I need voter population in the data.
'''
