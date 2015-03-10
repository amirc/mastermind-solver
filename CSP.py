from random import shuffle
from random import choice
from collections import Counter
import functools


def csp(slots, options, guesses):
    domains = [range(slots) for i in range(options)]

    # Check unary constraints
    for guess in guesses:
        if not guess[1]:
            if not guess[2]:
                for i in range(slots):
                    for domain in domains:
                        if i in domain:
                            domain.remove(i)
                continue
            for i in range(slots):
                if guess[0][i] in domains[i]:
                    domains[i].remove(guess[0][i])

    assignment = csp_rec(slots, guesses, domains, {}, range(slots))
    answer = []
    for i in range(slots):
        answer.append(assignment[i])

    return answer


def csp_rec(slots, guesses, domains, partial, remaining):
    # Return the assignment if it is a full assignment.
    if not remaining:
        return partial

    to_fill = choose_var(remaining, domains)
    vals = order_val(to_fill, domains[to_fill], guesses)

    for val in vals:
        print(val)


def choose_var(remaining, domains):
    sorted_rem = sorted(remaining, key=lambda x: len(domains[x]))
    return sorted_rem[0]


def comp(val1, val2, exact_count, near_count):
    exact_diff = exact_count[val2] - exact_count[val1]
    near_diff = near_count[val2] - near_count[val1]

    if exact_diff:
        return exact_diff

    if near_diff:
        return near_diff

    return choice([-1, 1])


def order_val(slot, domain, guesses):
    exact_count = Counter()
    near_count = Counter()

    for val in domain:
        exact_count[val] = 0
        near_count[val] = 0

    for guess in guesses:
        if guess[1]:
            exact_count[guess[0][slot]] += 1

        if guess[2]:
            to_update = set(guess[0])
            to_update.remove(guess[0][slot])
            near_count.update(to_update)

    # Send to helper which sorts by exact matches and near matches
    return sorted(domain, key = functools.cmp_to_key(lambda x, y: comp(x, y, exact_count, near_count)))