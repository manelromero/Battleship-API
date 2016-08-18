from random import randint


board = []
positions = []
success = 0

while success < 100:
	already_in_board = False
	letter = randint(1,10)
	number = randint(1,10)
	for element in board:
		if letter == element[0] and number == element[1]:
			already_in_board = True
	if already_in_board == False:
		board.append([letter, number])
		positions.append(chr(64 + letter) + str(number))
		success += 1

print positions

