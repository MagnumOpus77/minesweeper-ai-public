# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		self.rowDimension = colDimension
		self.colDimension = rowDimension
		self.totalMines = totalMines
		self.totalFlagged = 0
		self.totalUncovered = 0
		self.x = startX # x = col coordinate, y = row coordinate
		self.y = startY
		self.uncoverQueue = []
		self.flagQueue = []

		# init board
		self.board = [[None for i in range(rowDimension)] for j in range(colDimension)]

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	# def getRow(self, y: int):
	# 	return -y
	
	# def getCol(self, x: int):
	# 	return x-1
	
	def getNumberOfFlaggedNeighbors(self, x, y):
		"""
			returns number of flagged neighbors
		"""
		count = 0
		row = x
		col = y

		for r in range(row-1, row+2):
			for c in range(col-1, col+2):
				if r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] == -1: # -1 represents a mine (we can change if we want)
					count += 1

		return count
	
	def getNumberOfCoveredUnmarkedNeighbors(self, x, y):
		count = 0
		row = x
		col = y
		# print(self.board)
		for r in range(row-1, row+2):
			for c in range(col-1, col+2):
				if not (r == x and c == y) and r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] == None: # None represents covered tiles in self.board
					count += 1
		return count
	
	def getCoveredUnmarkedNeighbors(self, x, y):
		""" 
			returns list of (x, y) of uncovered unmarked neighbors
		"""
		neighbors = []
		row = x
		col = y
		# print(self.board)
		for r in range(row-1, row+2):
			for c in range(col-1, col+2):
				if not (r == x and c == y) and r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] == None: # None represents covered tiles in self.board
					neighbors.append((r, c))
		return neighbors
	
	def getEffectiveLabel(self, x, y):
		return self.board[x][y] - self.getNumberOfFlaggedNeighbors(x, y)
	
	def printBoard(self):
		for row in self.board:
			print(row)

	def checkForZeroEffectiveLabelsInNeighbors(self, x, y):
		"""
			If neighbor has zero effective label, add any uncovered neighbors to uncover queue
		"""
		if self.board[x][y] != None and self.getEffectiveLabel(x, y) == 0:
			coveredUnmarkedNeighbors = self.getCoveredUnmarkedNeighbors(x, y)
			if (len(coveredUnmarkedNeighbors) > 0):
				self.uncoverQueue.extend(coveredUnmarkedNeighbors[:])
				# print(self.uncoverQueue)

	def checkForMinesInNeighbors(self, x, y):
		if self.getEffectiveLabel(x, y) == self.getNumberOfCoveredUnmarkedNeighbors(x, y):
			coveredUnmarkedNeighbors = self.getCoveredUnmarkedNeighbors(x, y)
			if len(coveredUnmarkedNeighbors) > 0:
				# print("mine found")
				self.flagQueue.extend(coveredUnmarkedNeighbors)

	def getAction(self, number: int) -> Action:

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		self.board[self.x][self.y] = number # update board with uncovered number
		# print(f"LAST MOVE AT X: {self.x}, Y: {self.y}")
		# self.printBoard()
		# if effective label = 0, then uncover all neighbors
		if number == -1:
			for r in range(self.x-1, self.x+2):
				for c in range(self.y-1, self.y+2):
					if not(r == self.x and c == self.y) and r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] != None:
						self.checkForZeroEffectiveLabelsInNeighbors(r, c)

		if self.getEffectiveLabel(self.x, self.y) == 0:
			# print("if effective label = 0")
			coveredUnmarkedNeighbors = self.getCoveredUnmarkedNeighbors(self.x, self.y)
			# print("uncoveredUnmarkedNeighbors:", uncoveredUnmarkedNeighbors)
			if (len(coveredUnmarkedNeighbors) > 1):
				self.uncoverQueue.extend(coveredUnmarkedNeighbors[1:])
			if (len(coveredUnmarkedNeighbors) > 0):
				self.totalUncovered += 1
				self.x = coveredUnmarkedNeighbors[0][0]
				self.y = coveredUnmarkedNeighbors[0][1]
				
				self.board[self.x][self.y] = -2

				for r in range(self.x-1, self.x+2):
					for c in range(self.y-1, self.y+2):
						if not(r == self.x and c == self.y) and r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] != None:
							self.checkForMinesInNeighbors(r, c)
							# self.checkForZeroEffectiveLabelsInNeighbors(r,c)
				# self.checkForZeroEffectiveLabelsInNeighbors(self.x, self.y)
				# print(f"NEXT MOVE X: {self.x}, Y: {self.y}\n")
				return Action(AI.Action.UNCOVER, coveredUnmarkedNeighbors[0][0], coveredUnmarkedNeighbors[0][1])
		
		# if effective label = number of uncovered unmarked neighbors, then all uncovered unmarked neighbors are mines
		if self.getEffectiveLabel(self.x, self.y) == self.getNumberOfCoveredUnmarkedNeighbors(self.x, self.y):
			# print("if effective label = # of uncovered")
			coveredUnmarkedNeighbors = self.getCoveredUnmarkedNeighbors(self.x, self.y)
			if len(coveredUnmarkedNeighbors) > 1:
				self.flagQueue.extend(coveredUnmarkedNeighbors[1:])
			# print(f"curr x: {self.x}, y: {self.y}")
			if len(coveredUnmarkedNeighbors) > 0:
				self.totalFlagged += 1
				self.x = coveredUnmarkedNeighbors[0][0]
				self.y = coveredUnmarkedNeighbors[0][1]
				self.board[self.x][self.y] = -1
				for r in range(self.x-1, self.x+2):
					for c in range(self.y-1, self.y+2):
						if not(r == self.x and c == self.y) and r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] != None:
							self.checkForZeroEffectiveLabelsInNeighbors(r, c)
							self.checkForMinesInNeighbors(r, c)
				# print(f"flag x: {self.x}, y: {self.y}")
				return Action(AI.Action.FLAG, coveredUnmarkedNeighbors[0][0], coveredUnmarkedNeighbors[0][1])
		
		# UNCOVER a spot that we have in our uncover queue
		if self.uncoverQueue:
			# print("if uncoverQueue", set(self.uncoverQueue))
			while self.uncoverQueue:
				x, y = self.uncoverQueue.pop(0)
				# print("popped: ", x, y)
				if self.board[x][y] == None:
					self.totalUncovered += 1
					self.x, self.y = x, y
					self.board[self.x][self.y] = -2
					for r in range(self.x-1, self.x+2):
						for c in range(self.y-1, self.y+2):
							if not(r == self.x and c == self.y) and r >= 0 and r < len(self.board) and c >= 0 and c < len(self.board[0]) and self.board[r][c] != None:
								self.checkForMinesInNeighbors(r, c)
					return Action(AI.Action.UNCOVER, x, y)
		
		# FLAG a spot we have in our flag queue
		if self.flagQueue:
			# print("if flagQueue")\
			while self.flagQueue:
				x, y = self.flagQueue.pop(0)
				if self.board[x][y] == None:
					self.totalFlagged += 1
					self.x, self.y = x,y
					# print("flag")
					return Action(AI.Action.FLAG, x, y)

		# LEAVE if we have uncovered all spots that are not mines
		if self.totalUncovered == (self.rowDimension * self.colDimension) - self.totalMines:
			self.printBoard()
			return Action(AI.Action.LEAVE)
		
		# print(f"X: {self.x}, Y: {self.y}")
		# print(f"Uncover Q: {self.uncoverQueue}")
		# print(f"Flag Q: {self.flagQueue}")
		# self.printBoard()

		return Action(AI.Action.LEAVE)
		
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
