import random
import copy
from optparse import OptionParser
import util
import numpy as np
import random

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        solutionCounter = 0
        lectureCase = [[]]
        if lectureExample:
            lectureCase = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "q", ".", ".", ".", "."],
            ["q", ".", ".", ".", "q", ".", ".", "."],
            [".", "q", ".", ".", ".", "q", ".", "q"],
            [".", ".", "q", ".", ".", ".", "q", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ]
        for i in range(0,numberOfRuns):
            if self.search(Board(lectureCase), verbose).getNumberOfAttacks() == 0:
                solutionCounter+=1
        print "Solved:",solutionCounter,"/",numberOfRuns

    def search(self, board, verbose):
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print "iteration ",i
                print newBoard.toString()
                print newBoard.getCostBoard().toString()
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks) = newBoard.getBetterBoard()
            i+=1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [["." for i in range(0,8)] for j in range(0,8)]
        for i in range(0,8):
            tmpSquareArray[random.randint(0,7)][i] = "q"
        return tmpSquareArray
          
    def toString(self):
        s = ""
        for i in range(0,8):
            for j in range(0,8):
                s += str(self.squareArray[i][j]) + " "
            s += "\n"
        return s + "# attacks: "+str(self.getNumberOfAttacks())

    def getCostBoard(self):
        costBoard = copy.deepcopy(self)
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        #TODO: put your code here...
        attackCounts = self.getNumberOfAttacks()
        board = self.squareArray
        costBoard = self.getCostBoard().squareArray
        # print costBoard

        # find the min attack position in the board
        minAttack = min(min(cost) for cost in costBoard)
        print "minAttack: ", minAttack

        minAttackList = []
        
        # if Attacks = 0, return
        if self.getNumberOfAttacks() == 0:
            return (self, self.getNumberOfAttacks())

        # queens position and min attack position
        queenList = self.findElements("q")
        minAttackList = self.findElements(minAttack)
        
        # choose one target
        targetRow, targetCol = minAttackList[random.randint(0,len(minAttackList)-1)]
        
        # choose queen
        queenRow, queenCol = 0, 0
        for queen in queenList:
            if queen[1] == targetCol:
                queenRow = queen[0]
                queenCol = queen[1]

        # swap
        self.squareArray[targetRow][targetCol] = "q"
        self.squareArray[queenRow][queenCol] = "."

        return (self, self.getNumberOfAttacks())

    def findElements(self, element):
        cordiList = []
        for r in range(0,8):
            for c in range(0,8):
                if self.getCostBoard().squareArray[r][c] == element:
                    cordiList.append(( r , c ))

        return cordiList


    def getNumberOfAttacks(self):
        #TODO: put your code here...

        ## will attack each other, Queen at (i,j) (k,l)
        ## 1. i = k (same row)
        ## 2. j = l (same column)
        ## 3. |i-k| = |j-l| (diagnal)

        ## the position of 8 queens
        attackCounts = 0
        queenList = []
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    queenList.append( ( r,c ) )

        row, col = zip(*queenList)
        rowList = list(row)
        colList = list(col)

        ## number of queens in the same row
        attackRow = 0
        for i in range(0,7):
            for j in range(i+1,8):
                if rowList[j] == rowList[i]:
                    attackRow = attackRow + 1

        ## number of queens in the same column
        attackCol = 0
        for i in range(0,7):
            for j in range(i+1,8):
                if colList[j] == colList[i]:
                    attackCol = attackCol + 1

        ## number of queens in the same diagonal
        attackDiag = 0
        for i in range(0,7):
            for j in range(i+1,8):
                if abs(rowList[j] - rowList[i]) == abs(colList[j] - colList[i]):
                    attackDiag = attackDiag + 1

        attackCounts = attackRow + attackCol + attackDiag

        return attackCounts

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(0)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)