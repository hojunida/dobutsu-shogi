class Player():

	def __init__(self):
		self.bench = []

	def add_piece_to_bench(self, piece):
		self.bench.append(piece)

	def remove_piece_from_bench(self, piece):
		self.bench.remove(piece)

	def print_bench(self):
		bench_string_list = ""
		if len(self.bench) >= 1:
			for i in range(len(self.bench)):
				bench_string_list = bench_string_list + self.bench[i] + ", " 
			print(bench_string_list[:-2])
		else:
			print()
class Board():

	def __init__(self):
		self.board = [["EG","EL","EE"], ["--","EC","--"], ["--","MC","--"], ["ME","ML","MG"]] #refactor initialization value
		self.valid_moves = {
			"EC": [(1, 0)],
			"EG": [(1, 0), (-1, 0), (0, 1), (0, -1)],
			"EL": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)],
			"EE": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
			"EH": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1)],
			"MC": [(-1,0)],
			"MG": [(1, 0), (-1, 0), (0, 1), (0, -1)],
			"ML": [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)],
			"ME": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
			"MH": [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1)]
		}
		self.last_six_moves = []
		self.player = Player()

	def print_board(self):
		print('_'*15)
		for i in range(len(self.board)):
			row = '| '
			for j in range(len(self.board[0])):
				row = row + str(self.board[i][j]) + " | "
			print(row)
			print('_'*15)

	def board_to_string(self):
		return {"board": self.board, "enemy": self.flip_board()}

	def check_in_board(self, row, col):
		return row >= 0 and row < 4 and col >= 0 and col < 3

	def lion_in_check(self):
		for (x,y) in self.find_unsafe_spaces():
			if self.board[x][y] == "ML":
				return True
		return False

	def find_valid_spaces(self, row, col):
		piece = self.board[row][col]
		if piece != "--":
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
			if piece == "MC" and new_row == 0:
				piece = "MH"
			if replacing_piece == "--":
				self.board[old_row][old_col] = "--"
				self.board[new_row][new_col] = piece
			else:
				if replacing_piece == "EH":
					replacing_piece = "EC"
				if replacing_piece == "EL":
					print("game won by taking lion")
					return
				self.player.add_piece_to_bench("M" + replacing_piece[1:])
				self.board[old_row][old_col] = "--"
				self.board[new_row][new_col] = piece
		else:
			print("this is not a valid move")

		for i in range(len(self.board[0])):
			if self.board[0][i] == "ML" and not self.lion_in_check():
				print("game won by promoting lion")

		if len(self.last_six_moves) < 6:
			self.last_six_moves.append((old_row, old_col, new_row, new_col))
		else:
			del self.last_six_moves[0]
			self.last_six_moves.append((old_row, old_col, new_row, new_col))

		if len(self.last_six_moves) == 6 and self.last_six_moves[0] == self.last_six_moves[2] and self.last_six_moves[0] == self.last_six_moves[4] and self.last_six_moves[1] == self.last_six_moves[3] and self.last_six_moves[1] == self.last_six_moves[5]:
			print("game ends in a draw")



	def place_piece(self, piece, new_row, new_col):
		if piece in self.player.bench and self.board[new_row][new_col] == "--":
			self.board[new_row][new_col] = piece
			self.player.remove_piece_from_bench(piece)
		else:
			print("this is not a valid placement")

	def set_board(self, new_board):
		self.board = new_board

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


# if __name__ == "__main__":
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

	



