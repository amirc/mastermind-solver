from collections import Counter
from copy import deepcopy
import statistics
from CSP import CSP


def simple_extract(game_config, state, action):
    csp = CSP(game_config.slots, game_config.options)
    for guess, bulls, cows in state:
        csp.insert_guess(guess, bulls, cows)

    def positive_normalize(val, steps):
        return min(val, steps) / steps

    res = dict()

    # var on slots domain len
    # var_domain = statistics.variance([len(domain) for domain in csp._domains])

    # mean on slots domain len
    mean_domain = statistics.mean([len(domain) for domain in csp._domains])

    # mean on how many different vals in bull counter
    mean_bulls = statistics.mean([len(set(bull_slot.values())) for bull_slot in csp._bull_count])

    # var on how many different vals in bull counter
    var_bulls = statistics.variance([len(set(bull_slot.values())) for bull_slot in csp._bull_count])

    # mean on how many different vals in cow counter
    mean_cows = statistics.mean([len(set(cow_slot.values())) for cow_slot in csp._cow_count])

    # mean on how many different vals in cow counter
    var_cows = statistics.variance([len(set(cow_slot.values())) for cow_slot in csp._cow_count])

    guessed_times = Counter()
    for guess, bulls, cows in state:
        guessed_times.subtract(guess)

    unused_keys = len(set(range(game_config.options)).difference(set(guessed_times)))

    res[(action.__name__, 'unused_keys')] = positive_normalize(unused_keys, game_config.options)

    res[(action.__name__, 'mean_domain')] = positive_normalize(mean_domain, game_config.slots)
    res[(action.__name__, 'mean_bulls')] = positive_normalize(mean_bulls, game_config.options)
    res[(action.__name__, 'var_bulls')] = positive_normalize(var_bulls, game_config.options)
    res[(action.__name__, 'mean_cows')] = positive_normalize(mean_cows, game_config.options)
    res[(action.__name__, 'var_cows')] = positive_normalize(var_cows, game_config.options)
    if state:
        res[(action.__name__, 'bulls_last_turn')] = positive_normalize(state[-1][1], game_config.options)
        res[(action.__name__, 'cows_last_turn')] = positive_normalize(state[-1][2], game_config.options)

    res[(action.__name__, 'bias')] = 1

    return res


def correlation_extract(game_config, state, action):
    def get_state_statistics(csp):
        def positive_normalize(val, steps):
            return min(val, steps) / steps

        res = dict()

        # var on slots domain len
        # var_domain = statistics.variance([len(domain) for domain in csp._domains])

        # mean on slots domain len
        mean_domain = statistics.mean([len(domain) for domain in csp._domains])

        # mean on how many different vals in bull counter
        mean_bulls = statistics.mean([len(set(bull_slot.values())) for bull_slot in csp._bull_count])

        # var on how many different vals in bull counter
        var_bulls = statistics.variance([len(set(bull_slot.values())) for bull_slot in csp._bull_count])

        # mean on how many different vals in cow counter
        mean_cows = statistics.mean([len(set(cow_slot.values())) for cow_slot in csp._cow_count])

        # mean on how many different vals in cow counter
        var_cows = statistics.variance([len(set(cow_slot.values())) for cow_slot in csp._cow_count])

        res['mean_domain'] = positive_normalize(mean_domain, game_config.slots)
        res['mean_bulls'] = positive_normalize(mean_bulls, game_config.options)
        res['var_bulls'] = positive_normalize(var_bulls, game_config.options)
        res['mean_cows'] = positive_normalize(mean_cows, game_config.options)
        res['var_cows'] = positive_normalize(var_cows, game_config.options)

        return res

    def get_csp_for_state(any_state):
        tmp_csp = CSP(game_config.slots, game_config.options, 2)
        for guess, bulls, cows in any_state:
            tmp_csp.insert_guess(guess, bulls, cows)
        return tmp_csp

    def connect_guess(new_guess, new_bulls, new_cows):
        tmp_csp = deepcopy(cur_csp)
        tmp_csp.insert_guess(new_guess, new_bulls, new_cows)
        if not tmp_csp.generate_guess():
            return False, None
        return True, tmp_csp

    cur_csp = get_csp_for_state(state)

    next_guess = action(game_config, state)
    all_possible_states_csp = [connect_guess(next_guess, x, y)
                               for x in range(game_config.slots)
                               for y in range(game_config.slots)
                               if x + y < game_config.slots]

    stats = [get_state_statistics(state_csp) for possible, state_csp in all_possible_states_csp if possible]
    stats_by_param = {}
    for stat in stats:
        for name in stat.keys():
            if not stats_by_param.get(name):
                stats_by_param[name] = []
            stats_by_param[name].append(stat[name])

    res = {'bias': 1}

    for name in stats_by_param:
        res[name] = statistics.mean(stats_by_param[name])

    return res