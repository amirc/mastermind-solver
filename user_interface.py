from CSP import CSP
from Mastermind import Game
from random import choice

print("Welcome to the Mastermind player.")

legal = False

while not legal:
	legal = True
	slots_str = input("Please enter the number of slots: ")
	options_str = input("Please enter the number of options: ")

	try:
		slots = int(slots_str)
		options = int(options_str)
		assert(slots > 0 and options > 0)

	except:
		print("Please enter only positive integers.")
		legal = False

play_again = True

print("All guesses must be non-negative integers smaller than the number of options.")
print("The elements in your input should be separated by spaces.")
print("There should be exactly as many integers as slots.")
print("Good luck!\n")

print("Tossing a coin.")

first = choice([-1,1])

if first == 1:
	print("You won the coin toss.\n")

else:
	print("I won the coin toss.\n")

while play_again:

	game = Game(slots,options)
	csp = CSP(slots,options)

	game_finished = False

	if first == 1:
		print("You're going to go first this time.\n")

		while not game_finished:

			legal_guess = False

			while not legal_guess:
				legal_guess = True
				user_guess_string = input("Please input a guess: ")
				guess_string_list = user_guess_string.split(' ')
				guess = []

				try:
					assert(len(guess_string_list) == slots)
					for number in guess_string_list:
						to_add = int(number)
						assert(to_add in range(options))
						guess.append(to_add)

				except:
					legal_guess = False
					print("All guesses must be non-negative integers smaller than the number of options.")
					print("The integers should be separated by spaces.")
					print("There should exactly as many integers as slots.\n")

			result = game.check_guess(guess)

			print("You got ", result[1], " bulls and ", result[2], "cows.\n")

			if result[1] == slots:
				print("Congratulations! You won.\n")
				game_finished = True

			if not game_finished:
				
				comp_guess = csp.generate_guess()

				if not comp_guess:
					print("One of your previous responses was wrong.\n We need to restart the game.\n")
					break

				message = "My guess is:"

				for num in comp_guess:
					message += (' ' + str(num))

				print(message)

				legal_result = False

				while not legal_result:
					legal_result = True
					bulls_string = input("Please input the number of bulls: ")
					cows_string = input("Please input the number of cows: ")
					print("")

					try:
						bulls = int(bulls_string)
						cows = int(cows_string)
						assert(bulls in range(slots + 1) and cows in range(slots + 1) and (bulls + cows) in range(slots + 1))

					except:
						legal_result = False
						print("The number of cows and number of bulls has to be legal.")
						print("Any number you count as a bull cannot be counted as a cow and vice-versa.")
						print("The bulls and cows should be separated by spaces.")
						print("There should exactly two integers.\n")

				if bulls == slots:
					print("Hurray, I won!\n")
					game_finished = True

				if not game_finished:
					csp.insert_guess(comp_guess, bulls, cows)

	else:
		print("I'm going to go first this time.\n")

		while not game_finished:

			legal_guess = False

			comp_guess = csp.generate_guess()

			if not comp_guess:
				print("One of your previous responses was wrong.\n We need to restart the game.\n")
				break

			message = "My guess is:"

			for num in comp_guess:
				message += (' ' + str(num))

			print(message)

			legal_result = False

			while not legal_result:
				legal_result = True
				bulls_string = input("Please input the number of bulls: ")
				cows_string = input("Please input the number of cows: ")
				print("")

				try:
					bulls = int(bulls_string)
					cows = int(cows_string)
					assert(bulls in range(slots + 1) and cows in range(slots + 1) and (bulls + cows) in range(slots + 1))

				except:
					legal_result = False
					print("The number of cows and number of bulls has to be legal.")
					print("Any number you count as a bull cannot be counted as a cow and vice-versa.")
					print("The bulls and cows should be separated by spaces.")
					print("There should exactly two integers.\n")

			if bulls == slots:
				print("Hurray, I won!\n")
				game_finished = True

			if not game_finished:
				csp.insert_guess(comp_guess, bulls, cows)

				while not legal_guess:
					legal_guess = True
					user_guess_string = input("Please input a guess: ")
					guess_string_list = user_guess_string.split(' ')
					guess = []

					try:
						assert(len(guess_string_list) == slots)
						for number in guess_string_list:
							to_add = int(number)
							assert(to_add in range(options))
							guess.append(to_add)

					except:
						legal_guess = False
						print("All guesses must be non-negative integers smaller than the number of options.")
						print("The integers should be separated by spaces.")
						print("There should exactly as many integers as slots.\n")

				result = game.check_guess(guess)

				print("You got ", result[1], " bulls and ", result[2], "cows.\n")

				if result[1] == slots:
					print("Congratulations! You won.\n")
					game_finished = True
				
	first *= -1

	legal_answer = False

	while not legal_answer:
		answer = input("Would you like to play another game? Y/N ")
		print("")

		if answer == 'Y' or answer == 'y':
			legal_answer = True

		elif answer == 'N' or answer == 'n':
			legal_answer = True
			play_again = False

		else:
			print("Oops, please enter either 'Y' or 'N'.\n")

print("Thank you for playing!\n")