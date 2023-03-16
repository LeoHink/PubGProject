import collections
import random
import simulations as sim

def get_match_indices_dict(dict, cheaters = False, cheaters_list = None):
    """
    a function that takes a dictionary with key "match" and returns a dictionary where each 
    key is a match and the values are the indices of the match in the dictionary. Can also be used 
    to get matches where cheating players are involved. If cheaters is set to True, and cheaters_list
    is supplied.
    """
    if cheaters == False:
        matches = collections.defaultdict(list)
        for index, value in enumerate(dict["match"]):
            matches[value].append(index)
        return matches
    else: 
        if type(cheaters_list) != set:
            cheaters_list = set(cheaters_list)
        matches = collections.defaultdict(list)
        cheating_matches = set()
        for index, user in enumerate(dict["killer"]):
            if user in cheaters_list:
                cheating_matches.add(dict["match"][index])
        for index, match in enumerate(dict["match"]):
            if match in cheating_matches:
                matches[match].append(index)
        return matches
 

def get_index(users, cheaters):
    """
    a function that takes a list of usually of users, and return the index of the user in the list.
    Primarily used to find the date of started cheating in the cheaters dict. 
    """
    for index, value in enumerate(users):
        if value in cheaters:
            return index


def get_cheaters_index(users, cheaters):
    """
    a function that takes a list of cheaters and returns a dictionary
    of cheater and indeces of that cheater in the list
    """
    if type(cheaters) != set:
        cheaters = set(cheaters)

    indices = set()
    
    for index, value in enumerate(users):
        if value in cheaters:
            indices.add(index)
    return indices



def get_num_cheaters(users_dict, cheaters_dict, shuffle = False):
    """
    A function that returns the number of cheaters on each team 
    in each match and returns the aggregate number of teams with 1, 2, 3, or 4 cheaters. Also can 
    randomly shuffle the teams, to see whether the real observation is different to a random simulation.
    shuffle is set to False by default.
    """

    num_cheaters = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    cheaters_list = set(cheaters_dict["user"])
    match_indices = get_match_indices_dict(users_dict)
    for match, index in match_indices.items():
        user_id = [users_dict["user"][i] for i in index]
        team_id = [users_dict["team"][i] for i in index]
        if shuffle == True:
            random.shuffle(team_id)
        match_count = collections.defaultdict(int)
        non_cheaters = []
        for user_id, team_id in zip(user_id, team_id):
            if user_id in cheaters_list:
                match_count[team_id] += 1
            else:
                non_cheaters.append(team_id)
        for count in match_count.values():
            num_cheaters[count] += 1
    
        num_cheaters[0] += len(set(non_cheaters)-set(match_count.keys()))
    return num_cheaters



def imitation_cheaters(kills_dict, cheaters_dict, shuffle = False):
    """
    a function that takes the kills dict and cheaters dict and returns the number of cheaters 
    that started cheating after being killed by another cheater. If shuffle is set to True, the
    function will also randomly change the fates of players in the game to simulate a random 
    environment. 
    """
    immitation_cheater = []
    cheaters = set(cheaters_dict["user"])
    # get matches where cheaters are involved, for efficiency.
    matches = get_match_indices_dict(kills_dict, cheaters = True, cheaters_list = cheaters)
    for match, indices in matches.items():
        killers = [kills_dict["killer"][i] for i in indices]
        victims = [kills_dict["victim"][i] for i in indices]
        toks = [kills_dict["tok"][i] for i in indices]
        if shuffle == True:
            players = killers + victims
            suffled_players = sim.shuffle_map2(players)
            killers = suffled_players[:len(killers)]
            victims = suffled_players[len(killers):]
        for k, v, t in zip(killers, victims, toks):
            if k in cheaters and v in cheaters: 
                index_dtc_k = get_index(cheaters_dict["user"], k)
                index_dtc_v = get_index(cheaters_dict["user"], v)
                dtc_k = cheaters_dict["dtc"][index_dtc_k]
                dtc_v = cheaters_dict["dtc"][index_dtc_v]
            else:
                continue
            if dtc_k < t and dtc_v > t:
                immitation_cheater.append(v)
            else:
                continue
    return len(immitation_cheater)


def observation_cheaters(kills_dict, cheaters_dict, shuffle = False):
    """
    a function that takes the kills dict and cheaters dict and returns the number of cheaters 
    that started cheating after observing a cheater kill in a match. If shuffle is set to True, the
    function will also randomly change the fates of players in the game to simulate a random 
    environment
    """    
    observations_cheater = []
    cheaters = set(cheaters_dict["user"])
    # get matches where cheaters are involved, for efficiency.
    matches = get_match_indices_dict(kills_dict, cheaters = True, cheaters_list = cheaters)
    for match, indices in matches.items():
        killers = [kills_dict["killer"][i] for i in indices]
        victims = [kills_dict["victim"][i] for i in indices]
        toks = [kills_dict["tok"][i] for i in indices]
        if shuffle == True:
            players = killers + victims
            suffled_players = sim.shuffle_map2(players)
            killers = suffled_players[:len(killers)]
            victims = suffled_players[len(killers):]
        zipped_list = zip(toks, killers, victims)
        ts_zipped_list = sorted(zipped_list, key = lambda x: x[0])
        inter_cheater_dict = collections.defaultdict(int)
        index = 0
        victims_after_3 = []
        for t, k, v in ts_zipped_list:
            if k in cheaters:
                dtc_k = cheaters_dict["dtc"][get_index(cheaters_dict["user"], k)]
                if  dtc_k < t:
                    inter_cheater_dict[k] += 1
                    index += 1    
                    if inter_cheater_dict[k] == 3:
                        break
                else:
                    index += 1
            else:
                index += 1
                continue
              
        victims_after_3 = ts_zipped_list[index:]

        for t, k, v in victims_after_3:
            if v in cheaters:
                dtc_v = cheaters_dict["dtc"][get_index(cheaters_dict["user"], v)]
                if dtc_v > t:
                    observations_cheater.append(v)
            else:
                continue
    return len(set(observations_cheater))

