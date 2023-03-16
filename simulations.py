import random
import collections
import numpy as np
import observations as obs


def simulate_cheating_teams(users_dict, cheaters_list, iters):
    """
    a function that takes the team_id dictionary, cheaters list, and match_indices dictionary and the number 
    of iterations, and then creates a random allocation of team_ids to see how many cheaters per team. 
    Returns a dictionary of the number of teams with 0, 1, 2, 3, or 4 cheaters in each iteration.
    """
    output = {0:[], 1:[], 2:[], 3:[], 4:[]}
    for _ in range(iters):
        inter = obs.get_num_cheaters(users_dict, cheaters_list, shuffle = True)
        for key, value in inter.items():
            output[key].append(value)
            
    return output

def means_and_std(values):
    """
    A function that takes the output of randomization and returns the mean and 
    standard deviation of the number of teams with 0, 1, 2, 3, or 4 cheaters.
    """
    mean_std = (np.mean(values), 
        np.array([np.mean(values) - 1.96*(np.std(values)/np.sqrt(len(values))), 
        np.mean(values) + 1.96*(np.std(values)/np.sqrt(len(values)))]))
    return mean_std

    
def simulation_teams(dict):
    """
    A function that takes the output of simulate_cheating_teams and returns the mean and standard 
    deviation of the number of teams with 0, 1, 2, 3, or 4 cheaters.
    """
    output = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for key, value in dict.items():
        x = means_and_std(value)
        print(f"Number of teams with {key} cheaters: Mean = {round(x[0], 3)}, 95% CI = {np.around(x[1], 3)}")
        output[key] = means_and_std(value)
    return output

def shuffle_map2(og_list):
    """
    A function that randomly shuffles a list, but maps the random assignment to the original list. So
    every element in the original list is mapped to a random element in the shuffled list.
    """
     # creates a dictionary where key is the original element and value is the shuffled element.
    value_map = collections.defaultdict(list) 
    used_values = set()
    to_choose = list(set(og_list))
    for val in og_list: 
        if val not in value_map.keys():
            x = random.choice(to_choose)
            value_map[val] = x
            used_values.add(x)
            to_choose.remove(x)
        else:
            continue
    shuffled_list = [value_map[val] for val in og_list]
    return shuffled_list


def simulation_imitation(kills_dict, cheaters_dict, iters):
    """
    A function that takes the kill dictionary and cheaters index and outputs how many players we're killed by an active cheater. 
    """
    immitation_random = []

    for _ in range(iters):
        immitation_random.append(obs.imitation_cheaters(kills_dict, cheaters_dict, shuffle = True))
    x = means_and_std(immitation_random)
    print(f"Mean: {x[0]}, 95% CI:{np.around(x[1], 3)}") 
    return means_and_std(immitation_random)


def simulation_observation(kills_dict, cheaters_dict, iters):
    """
    A function that takes the kill dictionary and cheaters index and outputs how many
    players we're killed by an active cheater. 
    """
    immitation_random = []

    for _ in range(iters):
        immitation_random.append(obs.observation_cheaters(kills_dict, cheaters_dict, shuffle = True))
    x = means_and_std(immitation_random)
    print(f"Mean: {x[0]}, 95% CI:{np.around(x[1], 3)}") 
    return means_and_std(immitation_random)