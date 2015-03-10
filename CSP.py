from random import shuffle
from random import choice
from collections import Counter

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

	assignmnet = cspRec(slots, guesses, domains, {}, range(slots))
	answer = []
	for i in range(slots):
		answer.append(assignment[i])

	return answer

def cspRec(slots, guesses, domains, partial, remaining):

	# Return the assignment if it is a full assignment.
	if not remaining:
		return partial

	toFill = chooseVar(remaining, domains)
	vals = orderVal(toFill, domains[toFill], guesses)

	for val in vals:
		

def chooseVar(remaining, domains):
	
	sortedRem = sorted(remaining, key = lambda x: len(domains[x]))
	return sortedRem[0]

def comp(val1, val2, exactCount, nearCount):

	exactDiff = exactCount[val2] - exactCount[val1]
	nearDiff = nearCount[val2] - nearCount[val1]
	
	if exactDiff:
		return exactDiff

	if nearDiff:
		return nearDiff

	return choice([-1,1])


def orderVal(slot, domain, guesses):
	exactCount = Counter()
	nearCount = Counter()

	for val in domain:
		exactCount[val] = 0
		nearCount[val] = 0

	for guess in guesses:
		if guess[1]:
			exactCount[guess[0][slot]] += 1

		if guess[2]:
			toUpdate = set(guess[0])
			toUpdate.remove(guess[0][slot])
			nearCount.update(toUpdate)

	# Send to helper which sorts by exact matches and near matches
	return sorted(domain, cmp = lambda x,y: comp(x,y,exactCount,nearCount))








