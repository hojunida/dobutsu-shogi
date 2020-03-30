import copy
import numpy as np

GAME_NOT_DONE = 0
GAME_WON = 1
GAME_DRAWN = 2

class Game():
	def __init__(self):
		self.p1_board = Board()
		self.p2_board = Board()
		self.p1 = Player()
		self.p2 = Player()

	def giveReward(self):
		result = self.p1.check_game_state()
		if result is not None:
			self.p1.feedReward(result)
			self.p2.feedReward(result*-1)
		else:
			result2 = self.p2.check_game_state()
			if result2 is not None:
				self.p2.feedReward(result2)
				self.p1.feedReward(result2*-1)

	def reset(self):
		self.p1_board = Board()
		self.p2_board = Board()
		self.p1 = Player()
		self.p2 = Player()

	def play(self, rounds=100):
		for i in range(rounds):
			# print(i)
			if i % 1000 == 0:
				print("Rounds {}".format(i))
			turns = 0
			while True:
				# print()
				# self.p1_board.print_board()
				# print("p1 bench")
				# self.p1_board.print_bench()
				# raw_input("Press Enter to continue...")
				# Player 1
				turns += 1
				positions = self.p1_board.find_all_next_move()
				p1_action = self.p1.chooseAction(positions, self.p1_board)
				# take action and upate board state
				self.p1_board.set_board_from_hash(p1_action)
				self.p2_board.set_flip_board_from_hash(p1_action)
				self.p1.addState(p1_action)
				# check board status if it is end
				if self.p1.check_game_state() is not None:
					# self.showBoard()
					# ended with p1 either win or draw
					# print(self.p1.check_game_state())
					# print(turns)
					# self.p1_board.print_board()
					# raw_input("Press Enter to continue...")
					self.giveReward()
					self.reset()
					break
				else:
					# Player 2
					# self.p2_board.print_flip_board()
					# print("p2 bench")
					# self.p2_board.print_bench()
					positions = self.p2_board.find_all_next_move()
					p2_action = self.p2.chooseAction(positions, self.p2_board)
					self.p2_board.set_board_from_hash(p2_action)
					self.p1_board.set_flip_board_from_hash(p2_action)
					self.p2.addState(p2_action)


					if self.p2.check_game_state() is not None:
						# self.showBoard()
						# ended with p2 either win or draw
						# print(self.p2.check_game_state()*-1)
						# print(turns)
						# self.p2_board.print_board()
						# raw_input("Press Enter to continue...")
						self.giveReward()
						self.reset()
						break
		print(self.p1.states_value)

		print(self.p2.states_value)

class Player():

	def __init__(self, exp_rate=0.3):
		self.states = []
		self.lr = 0.2
		self.exp_rate = exp_rate
		self.decay_gamma = 0.9
		self.states_value = {}  # state -> value

	def chooseAction(self, positions, current_board):
		if np.random.uniform(0, 1) <= self.exp_rate:
			# take random action
			idx = np.random.choice(len(positions))
			action = positions[idx]
		else:
			value_max = -999
			for p in positions:
				next_board = current_board
				next_board = p
				next_boardHash = self.getHash(next_board)
				value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
				# print("value", value)
				if value >= value_max:
					value_max = value
					action = p
		# print("{} takes action {}".format(self.name, action))
		return action

	def check_game_state(self): # 1 - won 0 - game drawn -1 game lost None - game not done
		if len(self.states) < 1:
			return None
		if "ML" not in self.states[-1]:
			return -1
		elif "EL" not in self.states[-1]:
			return 1
		if len(self.states) > 6 and self.states[-1] == self.states[-3] and self.states[-1] == self.states[-5] and self.states[-2] == self.states[-4] and self.states[-2] == self.states[-6]:
			return 0
		return None

	# at the end of game, backpropagate and update states value
	def feedReward(self, reward):
		for st in reversed(self.states):
			if self.states_value.get(st) is None:
				self.states_value[st] = 0
			self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
			reward = self.states_value[st]

	def check_game_finished(self):
		return {"done": self.check_game_state()}

	def addState(self, board_hash):
		self.states.append(board_hash)

	def getHash(self, board):
		combined = ""
		for i in range(len(board)):
			for j in range(len(board[0])):
				combined = combined + str(board[i][j])
		return combined

class Board():

	def __init__(self):
		self.board = [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]] #refactor initialization value
		self.valid_moves = {
			# "EC": [(1, 0)],
			# "EG": [(1, 0), (-1, 0), (0, 1), (0, -1)],
			# "EL": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)],
			# "EE": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
			# "EH": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1)],
			"MC": [(-1,0)],
			"MG": [(1, 0), (-1, 0), (0, 1), (0, -1)],
			"ML": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)],
			"ME": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
			"MH": [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1)]
		}
		self.last_six_moves = []
		self.done = GAME_NOT_DONE
		self.bench = []

	def matrix_to_array(self, matrix): # only for this specific 3x2 matrix
		array = matrix[0]
		array.extend(matrix[1])
		return array

	def array_to_matrix(self,array): # only for this specific 3x2 matrix
		if len(array) > 3:
			return [array[:3], array[3:]]
		else:
			return [array, []]

	def add_piece_to_bench(self, piece):
		self.bench.append(piece)

	def remove_piece_from_bench(self, index):
		if len(self.bench) >= index:
			del self.bench[index]

	# def remove_piece_from_bench(self,piece):
	# 	array = self.matrix_to_array(self.bench)
	# 	if piece in array:
	# 		array.remove(piece)
	# 	else:
	# 		print("removing a piece not in bench??")
	# 	self.bench = self.array_to_matrix(array)

	def print_bench(self):
		print(self.bench)

	def print_board(self):
		print('_'*15)
		for i in range(len(self.board)):
			row = '| '
			for j in range(len(self.board[0])):
				row = row + str(self.board[i][j]) + " | "
			print(row)
			print('_'*15)

	def print_flip_board(self):
		board = self.flip_board()
		print('_'*15)
		for i in range(len(board)):
			row = '| '
			for j in range(len(board[0])):
				row = row + str(board[i][j]) + " | "
			print(row)
			print('_'*15)

	def getHash(self, board):
		combined = ""
		for i in range(len(board)):
			for j in range(len(board[0])):
				combined = combined + str(board[i][j])
		return combined

	def board_to_string(self, prefix):
		return {prefix+"Board": self.board, prefix+"Bench": self.bench}

	def check_in_board(self, row, col):
		return row >= 0 and row < 4 and col >= 0 and col < 3

	def lion_in_check(self):
		for (x,y) in self.find_unsafe_spaces():
			if self.board[x][y] == "ML":
				return True
		return False

	def return_bench(self):
		return {"bench": self.bench}

	def find_all_next_move(self):
		res = []
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] != "--":
					valid_spaces = self.find_valid_spaces(i,j)
					for (row, col) in valid_spaces:
						res.append(self.pretend_move(i,j,row,col))
		
		empty_spaces = self.find_empty_spaces()

		for i in range(len(self.bench)):
			for (row, col) in empty_spaces:
				res.append(self.pretend_place(i,row,col))

			  
		res = list(set(res))
		if self.getHash(self.board) in res:
			res.remove(self.getHash(self.board))
		return res

	def find_valid_spaces(self, row, col):
		piece = self.board[row][col]
		if piece != "--" and piece in self.valid_moves.keys():
			valid_spaces = [(x+row, y+col) for (x,y) in self.valid_moves[piece]]
			valid_spaces = [(x,y) for (x,y) in valid_spaces if self.check_in_board(x,y)]
			valid_spaces = [(x,y) for (x,y) in valid_spaces if self.board[x][y] not in ["MG", "MH", "MC", "ML", "ME"]] # needs to include logic for enemy piece if used for such purpose

			# taken out so that lion can be captured
			# if piece == "ML":
			# 	valid_spaces = [(x,y) for (x,y) in valid_spaces if (x,y) not in self.find_unsafe_spaces()]

			# if self.lion_in_check():
			# 	old_board = [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]] #refactor initialization value
			# 	for i in range(len(self.board)):
			# 		for j in range(len(self.board[0])):
			# 			old_board[i][j] = self.board[i][j]

			# 	space_to_remove = []

			# 	for (x,y) in valid_spaces:
			# 		self.move_piece_no_check(row, col, x, y)
			# 		if self.lion_in_check():
			# 			space_to_remove.append((x,y))
			# 		for i in range(len(self.board)):
			# 			for j in range(len(self.board[0])):
			# 				self.board[i][j] = old_board[i][j]

			# 	valid_spaces = [(x,y) for (x,y) in valid_spaces if (x,y) not in space_to_remove]

			return valid_spaces
		else:
			return []

	def find_empty_spaces(self):
		empty_spaces = []
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] == "--":
					empty_spaces.append((i,j))
		return empty_spaces
					

	def find_unsafe_spaces(self):
		unsafe_spaces = []
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] in ["EG", "EH", "EC", "EL", "EE"]:
					space_in_range = [(x+i, y+j) for (x,y) in self.valid_moves[self.board[i][j]]]
					space_in_range = [(x,y) for (x,y) in space_in_range if self.check_in_board(x,y)]
					unsafe_spaces.extend(space_in_range)
		unsafe_spaces = list(set(unsafe_spaces))
		return unsafe_spaces

	def move_piece_no_check(self, old_row, old_col, new_row, new_col):
		piece = self.board[old_row][old_col]
		replacing_piece = self.board[new_row][new_col]
		
		if piece == "MC" and new_row == 0:
			piece = "MH"
		if replacing_piece == "--":
			self.board[old_row][old_col] = "--"
			self.board[new_row][new_col] = piece
		else:
			if replacing_piece == "EH":
				replacing_piece = "EC"
			self.board[old_row][old_col] = "--"
			self.board[new_row][new_col] = piece

	def move_piece(self, old_row, old_col, new_row, new_col):
		piece = self.board[old_row][old_col]
		replacing_piece = self.board[new_row][new_col]
		if (new_row, new_col) in self.find_valid_spaces(old_row, old_col):
			if piece == "MC" and new_row == 0 and replacing_piece != "EL":
				piece = "MH"
			if replacing_piece == "--":
				self.board[old_row][old_col] = "--"
				self.board[new_row][new_col] = piece
			else:
				if replacing_piece == "EH":
					replacing_piece = "EC"
				if replacing_piece == "EL":
					self.done = GAME_WON # print("game won by taking lion")
				self.add_piece_to_bench("M" + replacing_piece[1:])
				self.board[old_row][old_col] = "--"
				self.board[new_row][new_col] = piece
		else:
			print("this is not a valid move")

		# for i in range(len(self.board[0])):
		# 	if self.board[0][i] == "ML" and not self.lion_in_check():
		# 		self.done = GAME_WON # print("game won by promoting lion")

		if len(self.last_six_moves) < 6:
			self.last_six_moves.append((old_row, old_col, new_row, new_col))
		else:
			del self.last_six_moves[0]
			self.last_six_moves.append((old_row, old_col, new_row, new_col))

		if len(self.last_six_moves) == 6 and self.last_six_moves[0] == self.last_six_moves[2] and self.last_six_moves[0] == self.last_six_moves[4] and self.last_six_moves[1] == self.last_six_moves[3] and self.last_six_moves[1] == self.last_six_moves[5]:
			self.done = GAME_DRAWN

	def place_piece(self, bench_index, new_row, new_col):
		piece = self.bench[bench_index]
		if (piece in self.bench[0] or piece in self.bench[1]) and self.board[new_row][new_col] == "--":
			self.board[new_row][new_col] = piece
			self.remove_piece_from_bench(bench_index)
		else:
			print((piece in self.bench[0] or piece in self.bench[1]))
			print("this is not a valid placement")

	def pretend_move(self,old_row, old_col, new_row, new_col):
		piece = self.board[old_row][old_col]
		replacing_piece = self.board[new_row][new_col]
		pretend_board = copy.deepcopy(self.board)
		if (new_row, new_col) in self.find_valid_spaces(old_row, old_col):
			if piece == "MC" and new_row == 0 and replacing_piece != "EL":
				piece = "MH"
			if replacing_piece == "--":
				pretend_board[old_row][old_col] = "--"
				pretend_board[new_row][new_col] = piece
			else:
				if replacing_piece == "EH":
					replacing_piece = "EC"
				if replacing_piece == "EL":
					self.done = GAME_WON # print("game won by taking lion")
				pretend_board[old_row][old_col] = "--"
				pretend_board[new_row][new_col] = piece
		return self.getHash(pretend_board)
		# for i in range(len(self.board[0])):
		# 	if self.board[0][i] == "ML" and not self.lion_in_check():
		# 		self.done = GAME_WON # print("game won by promoting lion")

	def pretend_place(self, bench_index, new_row, new_col):
		piece = self.bench[bench_index]
		pretend_board = copy.deepcopy(self.board)
		if (piece in self.bench[0] or piece in self.bench[1]) and self.board[new_row][new_col] == "--":
			pretend_board[new_row][new_col] = piece
		return self.getHash(pretend_board)



	def set_board(self, new_board):
		self.board = copy.deepcopy(new_board)

	def set_board_from_hash(self, new_board_hash): #assuming only correct lenght of hashstring

		# print(self.getHash(self.board))
		# print(new_board_hash)
		diff = self.find_diff(self.getHash(self.board), new_board_hash)

		if(len(diff) == 2): #placing
			first = diff[0]/2
			piece = new_board_hash[diff[0]:(diff[1]+1)]
			bench_index = -1
			if piece in self.bench:
				bench_index = self.bench.index(piece)
				self.place_piece(bench_index, first//3, first%3)
			else:
				print("bug af")

		elif(len(diff) == 3 or len(diff) == 4): #moving
			first = diff[0]/2
			second = diff[2]/2
			if len(diff) == 3: #special case that the last letter overlaps (i.e. ME eating EE)
				if diff[1]- diff[0] != 1:
					first = diff[0]/2
					second = diff[1]/2
			if "M" in self.board[first//3][first%3]:
				self.move_piece(first//3, first%3, second//3, second%3)
			else:
				self.move_piece(second//3, second%3, first//3, first%3)

		# self.print_board()


	def set_flip_board_from_hash(self, new_board_hash):
		# self.set_board_from_hash(new_board_hash)

		new_board = copy.deepcopy(self.board)
		idx = 0
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				new_board[i][j] = new_board_hash[idx:idx+2]
				idx+=2
		self.board = copy.deepcopy(new_board)

		self.board = self.flip_board()

	def flip_board(self):
		new_board = [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]] #prob should differ intialization of board
		# flip the perspective first
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				new_board[i][j] = self.board[len(self.board)-(i+1)][len(self.board[0])-(j+1)]
		# flip the pieces
		for i in range(len(new_board)):
			for j in range(len(new_board[0])):
				if new_board[i][j][0] == "M":
					new_board[i][j] = "E" + new_board[i][j][1:]
				elif new_board[i][j][0] == "E":
					new_board[i][j] = "M" + new_board[i][j][1:]	
		return new_board

	def find_diff(self, old_board_hash, new_board_hash):
		res = []
		for i in range(24):
			if old_board_hash[i] != new_board_hash[i]:
				res.append(i)
		return res


if __name__ == "__main__":
	new_game = Game()
	new_game.play(rounds=10000)
# 	player_board = Board()
# 	player_board.move_piece(3,2,2,2)
# 	enemy_board = Board()
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(2,1,1,1)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,1,3,2)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(1,1,0,1)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,2,3,1)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.place_piece("MC", 1, 1)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,0,2,1)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(3,1,2,1)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,1,3,2)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(2,1,1,2)
# 	player_board.set_board(enemy_board.flip_board())

# 	# draw route

# 	player_board.move_piece(3,2,3,1)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(1,2,2,1)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,1,3,2)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(2,1,1,2)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,2,3,1)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(1,2,2,1)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,1,3,2)
# 	enemy_board.set_board(player_board.flip_board())
# 	enemy_board.move_piece(2,1,1,2)
# 	player_board.set_board(enemy_board.flip_board())
# 	player_board.move_piece(3,2,3,1)
# 	enemy_board.set_board(player_board.flip_board())
	
# 	# lion promotion route
# 	# player_board.move_piece(2,1,1,2)
# 	# enemy_board.set_board(player_board.flip_board())
# 	# enemy_board.move_piece(1,2,0,2)


# 	# lion capture route

# 	# player_board.move_piece(2,2,1,2)
# 	# enemy_board.set_board(player_board.flip_board())
# 	# enemy_board.move_piece(3,0,2,1)
# 	# player_board.set_board(enemy_board.flip_board())
# 	# player_board.move_piece(1,2,1,1)
# 	# enemy_board.set_board(player_board.flip_board())
# 	# enemy_board.move_piece(3,2,2,2)
# 	# player_board.set_board(enemy_board.flip_board())
# 	# player_board.move_piece(1,1,1,0)
# 	# enemy_board.set_board(player_board.flip_board())
# 	# enemy_board.move_piece(1,2,2,2)
# 	# player_board.set_board(enemy_board.flip_board())
# 	# player_board.move_piece(2,1,1,0)

# 	# player_board.print_board()
# 	enemy_board.print_board()



# 	player_board.player.print_bench()
# 	enemy_board.player.print_bench()

	



