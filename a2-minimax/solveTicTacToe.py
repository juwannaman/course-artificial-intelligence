# tic-tac-toe
import random
import numpy as np
import sys

class TicTacToe:
	"""docstring for TicTacToe"""
	# tic-tac-toe board
	board = [
				[".",".","."],
				[".",".","."],
				[".",".","."]
				]
    # tic-tac-toe movement guide
	moveKey = [
				["0","1","2"],
				["3","4","5"],
				["6","7","8"]
				]
	# initial step		
	step = 0

	def __init__(self):
		self.aiAction()
		

	def showBoard(self):
		print "Board:", "\t\t\t\t\t", "MoveKey:"
		print self.board[0], "\t\t\t", self.moveKey[0]
		print self.board[1], "\t\t\t", self.moveKey[1]
		print self.board[2], "\t\t\t", self.moveKey[2]
		
	def aiAction(self):
		print "AI TURN!"
		self.step += 1

		# if it's the first move
		if self.step == 1:
			self.board[1][1] = "X"
			print "AI takes action ", 1*3 + 1
		# if it's not the first move
		else:
			# choose in recommended moves
			legal = self.evaluationFunction()
			choose = random.randint(0, len(legal)-1)
			row, col = legal[choose]
			self.board[row][col] = "X"
			print "AI takes action ", row*3 + col

		self.showBoard()
		if(self.isLose()): 
			print "AI Lose!"
			sys.exit()
		self.playerAction()


	def playerAction(self):
		self.step += 1

		# input move
		playerMoveStr = input('YOU TURN! Enter your move: ')
		playerMove = int(playerMoveStr)
		playerRow = playerMove / 3
		playerCol = playerMove % 3
		moveTuple = (playerRow, playerCol)
		legal = self.legalMoves()

		# if the cell is chosen
		while (moveTuple not in legal):
			print "Already chosen, select again"
			playerMoveStr = input('YOU TURN! Enter your move: ')
			playerMove = int(playerMoveStr)
			playerRow = playerMove / 3
			playerCol = playerMove % 3
			moveTuple = (playerRow, playerCol)

		# replace as "X"
		self.board[playerRow][playerCol] = "X"
		self.showBoard()
		if(self.isLose()): 
			print "You Lose!"
			sys.exit()
		self.aiAction()

	def isLose(self):
		winningCondition = [[(0,0),(0,1),(0,2)],
							[(1,0),(1,1),(1,2)],
							[(2,0),(2,1),(2,2)],
							[(0,0),(1,0),(2,0)],
							[(0,1),(1,1),(2,1)],
							[(0,2),(1,2),(2,2)],
							[(0,0),(1,1),(2,2)],
							[(0,2),(1,1),(2,0)]]
		
		setPlay = set([(ix,iy) for ix, row in enumerate(self.board) for iy, i in enumerate(row) if i == "X"])
		for win in winningCondition:
			if len(set(win).intersection(setPlay)) == 3:
				return True
		return False

	def legalMoves(self):
		legalCell = [(ix,iy) for ix, row in enumerate(self.board) for iy, i in enumerate(row) if i == "."]
		return legalCell

	def evaluationFunction(self):
		# number of rows AI can win - number of rows I can win
		winningCondition = [[(0,0),(0,1),(0,2)],
							[(1,0),(1,1),(1,2)],
							[(2,0),(2,1),(2,2)],
							[(0,0),(1,0),(2,0)],
							[(0,1),(1,1),(2,1)],
							[(0,2),(1,2),(2,2)],
							[(0,0),(1,1),(2,2)],
							[(0,2),(1,1),(2,0)]]
		
		setPlay = set([(ix,iy) for ix, row in enumerate(self.board) for iy, i in enumerate(row) if i == "X"])
		legalSet = set(self.legalMoves())

		for win in winningCondition:
			difference = (set(win).difference(set(win).intersection(setPlay)))
			if len(difference) == 1:
				legalSet = legalSet.difference(difference)
				
		legalList = list(legalSet)

		return legalList


if __name__ == "__main__":
	tic = TicTacToe()