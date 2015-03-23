from collections import Counter
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

