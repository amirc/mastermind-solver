from random import shuffle
from random import choice
from collections import Counter
import functools
from copy import copy


# How to use:
# problem = CSP(3,5)
# problem.insert_guess([1,2,3], 2, 1)
# print ("Best solution " + str(problem.generate_guess()) + "?") # output: [1,4,3]
from Mastermind import Game


class CSP:
    def __init__(self, slots, options):
        self._domains = [list(range(options)) for i in range(slots)]
        self._guesses = list()
        self._slots = slots
        self._options = options

    def insert_guess(self, guess, bulls, cows):
        self._guesses += [(guess, bulls, cows)]
        if not bulls:
            if not cows:
                # TODO: maybe to delete this guess from guesses
                for i in range(self._slots):
                    for domain in self._domains:
                        if i in domain:
                            domain.remove(i)
            else:
                for i in range(self._slots):
                    if guess[i] in self._domains[i]:
                        self._domains[i].remove(guess[i])

        if cows + bulls == self._slots:
            possible = set(guess)
            for i in range(self._slots):
                new_domain = [x for x in possible if x in self._domains[i]]
                self._domains[i] = new_domain

    def generate_guess(self):
        assignment = self._csp_rec({}, list(range(self._slots)))

        answer = []
        for i in range(self._slots):
            answer.append(assignment[i])

        return answer

    def _csp_rec(self, partial_sol, remaining):
        # Return the assignment if it is a full assignment.
        if not remaining:
            return partial_sol

        to_fill = self._choose_var(remaining)
        vals = self._order_val(to_fill)

        for val in vals:
            tmp_sol = copy(partial_sol)
            tmp_sol[to_fill] = val
            if self._is_sol_valid(tmp_sol):
                tmp_remaining = copy(remaining)
                tmp_remaining.remove(to_fill)
                tmp_res = self._csp_rec(tmp_sol, tmp_remaining)
                if tmp_res:
                    return tmp_res

        return False

    def _is_sol_valid(self, sol):
        empty_slots = self._slots - len(sol)
        code = [-1] * self._slots

        for k in sol:
            code[k] = sol[k]

        game = Game(self._slots, self._options, code)

        for guess, org_bulls, org_cows in self._guesses:
            guess, res_bulls, res_cows = game.check_guess(guess)

            bulls_dist = org_bulls - res_bulls
            if bulls_dist < 0 or bulls_dist > empty_slots:
                return False

            tmp_empty_slots = empty_slots - bulls_dist

            cows_dist = org_cows - res_cows

            if (cows_dist < 0 or cows_dist > tmp_empty_slots) and (bulls_dist == 0 or cows_dist + bulls_dist < 0):
                return False

        return True

    def _choose_var(self, remaining):
        sorted_rem = sorted(remaining, key=lambda x: len(self._domains[x]))
        return sorted_rem[0]

    def _order_val(self, slot):
        domain = self._domains[slot]
        exact_count = Counter()
        near_count = Counter()

        for val in domain:
            exact_count[val] = 0
            near_count[val] = 0

        #TODO: To make this calculation once for all vals or to make it depended on current solution
        for guess in self._guesses:
            if guess[1]:
                exact_count[guess[0][slot]] += 1

            if guess[2]:
                to_update = set(guess[0])
                to_update.remove(guess[0][slot])
                near_count.update(to_update)

        # Send to helper which sorts by exact matches and near matches
        return sorted(domain, key=functools.cmp_to_key(lambda x, y: self._comp(x, y, exact_count, near_count)))

    #TODO: make static(?):
    def _comp(self, val1, val2, exact_count, near_count):
        exact_diff = exact_count[val2] - exact_count[val1]
        near_diff = near_count[val2] - near_count[val1]

        if exact_diff:
            return exact_diff

        if near_diff:
            return near_diff

        return choice([-1, 1])