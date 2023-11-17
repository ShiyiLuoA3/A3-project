"""
Description: Implementation of Gobang (Five in a Row) board and basic functionality
"""

import collections  

chessMan = collections.namedtuple("chess", ["Name", "Value", "Color"]) #Chessman type
Point = collections.namedtuple("point", ["X", "Y"])  #Point type

offset = [(1, 0), (0, 1), (1, 1), (1, -1)]  #Offset of the four directions
#defining the chessman
BLACK_CHESSMAN = chessMan("Black", 1, (0, 0, 0))
WHITE_CHESSMAN = chessMan("White", 2, (255, 255, 255))

class Board:
    #Initialize the board
    def __init__(self, pointNumber):
        self._linePoints = pointNumber
        half = pointNumber // 2
        self._board = []
        #draw the board
        for i in range(half):
            row = [0] * (half - i) + [0] * (2 * i + 1) + [0] * (half - i)
            self._board.append(row)
        for i in range(half, -1, -1):
            row = [0] * (half - i) + [0] * (2 * i + 1) + [0] * (half - i)
            self._board.append(row)

    def _getBoard(self):
        return self._board
   
    board = property(_getBoard)  

    def is_inside_diamond(self,p, size): #check if the point is inside the diamond
        half_size = size // 2
        center = half_size
        relative_x = abs(p[0] - center)
        relative_y = abs(p[1] - center)

        return relative_x + relative_y <= half_size
    
    #Remove a piece at a given point
    def removeChess(self, point):
        if 0 <= point.Y < self._linePoints and 0 <= point.X < len(self._board[point.Y]):
            self._board[point.Y][point.X] = 0


    def ifDropChess(self, point):#check if the point is valid
        if (0 <= point.Y < self._linePoints and 
            0 <= point.X < len(self._board[point.Y]) and 
            self._board[point.Y][point.X] == 0 and
            self.is_inside_diamond((point.X, point.Y), self._linePoints)):#check if the point is inside the diamond
                return True
        else:
            return False

    
    def countDirection(self, point, value, offsetX, offsetY):#count the number of chessman in a row
        count = 1  
        
        for i in range(1, 5):#check the number of chessman in the positive direction
            x = point.X + i*offsetX
            y = point.Y + i*offsetY
            if 0 <= y < self._linePoints \
            and 0 <= x < len(self._board[point.Y]) \
            and value == self._board[y][x]:
                count += 1
            else:
                break

        for i in range(1, 5):#check the number of chessman in the negative direction
            x = point.X - i*offsetX
            y = point.Y - i*offsetY
            if 0 <= y < self._linePoints \
                and 0 <= x < len(self._board[point.Y]) \
                and value == self._board[y][x]:
                count += 1
            else:
                break
            
        judgeWin = (count >= 5)
        return judgeWin
    
    def win(self, point):#check if the player wins
        currentValue = self._board[point.Y][point.X]
        for offsetArray in offset:
            if self.countDirection(point, currentValue, 
                                   offsetArray[0], 
                                   offsetArray[1]):
                return True
            
    def dropChess(self, chessMan, point):#drop a chessman at a given point
        print(f"{chessMan.Name}({point.X}, {point.Y})")
        self._board[point.Y][point.X] = chessMan.Value
        if self.win(point):
            print(f"{chessMan.Name} wins!")
            return chessMan
