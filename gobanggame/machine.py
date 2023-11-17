
"""
Description: Implementation of the machine class for Gobang (Five in a Row) human vs machine gameplay.
"""
from board import BLACK_CHESSMAN, Point, offset
import random

class Machine:
    # Initialization
    def __init__(self, pointNumber, chessMan):
        self._pointNumber = pointNumber  # Number of points on the board
        self._my = chessMan  # Current player's chess piece
        self._rival = BLACK_CHESSMAN  # Opponent's chess piece
        # Initialize board, setting all elements to 0
        self._board = [[0] * pointNumber for i in range(pointNumber)]
    
    # Get the opponent's move
    def getRivalDrop(self, point):
        self._board[point.Y][point.X] = self._rival.Value
        
    
    # Determine the state of the chess piece two steps away in a given direction (Self: 1, Opponent: 2, Empty: 0)
    def getPiece(self, point, offsetX, offsetY, TorF):
        x = point.X + offsetX  
        y = point.Y + offsetY 
        if 0 <= x < self._pointNumber and 0 <= y < self._pointNumber:  # Check if the coordinates are within board limits
            if self._board[y][x] == self._my.Value:  # If the square has a piece of the current player
                return 1  
            elif self._board[y][x] == self._rival.Value:  # If the square has a piece of the opponent
                return 2 
            else:  # If the square is empty
                if TorF:  # Whether to continue checking or not
                    # Skip this square if it's the second time encountering an empty square
                    return self.getPiece(Point(x, y), offsetX, offsetY, False)
                else:
                    return 0  # Indicate that there's no piece within two squares in this direction
        else:
            return 0

    # Calculate the score (weight) for a direction
        

    def is_inside_diamond(self,p, size):
        half_size = size // 2
        center = half_size
        relative_x = abs(p[0] - center)
        relative_y = abs(p[1] - center)

        return relative_x + relative_y <= half_size



    def getDirectionScore(self, point, offsetX, offsetY):
        countSelf = 0 
        countOpposite = 0  
        spaceSelf = None  
        spaceOpposite = None  
        blockSelf = 0 
        blockOpposite = 0 

        # 1 indicates self's piece, 2 indicates opponent's piece, 0 indicates no piece
        flagPositive = self.getPiece(point, offsetX, offsetY, True)
        # Continue with the logic if there exists a piece in the direction specified by the offset
        if flagPositive != 0:
            for i in range(1, 6): # Loop to determine how many pieces are connected in that direction
                x = point.X + i * offsetX 
                y = point.Y + i * offsetY 
                # calculate the score (weight) for a direction
                if 0 <= x < self._pointNumber and 0 <= y < self._pointNumber:
                    if flagPositive == 1: 
                        if self._board[y][x] == self._my.Value: 
                            countSelf += 1 
                            if spaceSelf is False: 
                                spaceSelf = True  
                        elif self._board[y][x] == self._rival.Value: 
                            blockOpposite += 1 
                            break 
                        else: #If no piece exists in the square
                            if spaceSelf is None: 
                                spaceSelf = False 
                            else:
                                break   
                    elif flagPositive == 2: #check if the square has a piece of the opponent
                        if self._board[y][x] == self._my.Value:
                            blockOpposite += 1 
                            break 
                        elif self._board[y][x] == self._rival.Value: 
                            countOpposite += 1
                            if spaceOpposite is False: 
                                spaceOpposite = True 
                        else:
                            if spaceOpposite is None: 
                                spaceOpposite = False 
                            else:
                                break 
                else: # If the square is outside the board
                    if flagPositive == 1: 
                        blockSelf += 1 
                    elif flagPositive == 2: 
                        blockOpposite += 1 

        if spaceSelf is False:  # If there's no piece in the direction
            spaceSelf = None 
        if spaceOpposite is False: 
            spaceOpposite = None

        # Invert the X and Y increments in the set offset and repeat the above operation.
        flagNegative = self.getPiece(point, -offsetX, -offsetY, True)
        if flagNegative != 0:
            for i in range(1, 6):
                x = point.X - i * offsetX
                y = point.Y - i * offsetY

                if not self.is_inside_diamond(Point(x, y), self._pointNumber):
                    break

                if 0 <= x < self._pointNumber and 0 <= y < self._pointNumber:
                    if flagNegative == 1:
                        if self._board[y][x] == self._my.Value:
                            countSelf += 1
                            if spaceSelf is False:
                                spaceSelf = True
                        elif self._board[y][x] == self._rival.Value:
                            blockOpposite += 1
                            break
                        else:
                            if spaceSelf is None:
                                spaceSelf = False
                            else:
                                break   
                    elif flagNegative == 2:
                        if self._board[y][x] == self._my.Value:
                            blockOpposite += 1
                            break
                        elif self._board[y][x] == self._rival.Value:
                            countOpposite += 1
                            if spaceOpposite is False:
                                spaceOpposite = True
                        else:
                            if spaceOpposite is None:
                                spaceOpposite = False
                            else:
                                break
                else:
                    if flagNegative == 1:
                        blockSelf += 1
                    elif flagNegative == 2:
                        blockOpposite += 1
        '''
        Weighted value division:
        (Your side's four consecutive pieces > enemy's four consecutive pieces) > (Your side's three consecutive pieces without blocking > enemy's three consecutive pieces without blocking) > (Your side's three consecutive pieces with one block && your side's two consecutive pieces without blocking)
        >(enemy's three consecutive pieces have a block & & enemy's two consecutive pieces have no block) > (your side's two consecutive pieces have a block > enemy's two consecutive pieces have a block)
        No spaces > with spaces, both cases should be in the same order of magnitude (immediately after the brackets)
        Priority quantization 8 10 80 100 800 1000 8000 10000 five groups 
        '''
        score = 0 # Initialize weight value to determine priority of the move
        if countSelf == 4: # If there are four consecutive pieces for self
            score = 10000 # Priority reference note
        elif countOpposite == 4: # If there are four consecutive pieces for the opponent
            score = 8000 # Priority reference note
        elif countSelf == 3: # If there are three consecutive pieces for self
            if blockSelf == 0: # If three consecutive pieces for self are unblocked
                score = 1000 # Priority reference note
            elif blockSelf == 1: # If one out of three consecutive pieces for self is blocked
                score = 100 # Priority reference note
            else:
                score = 0 # Lowest priority
        elif countOpposite == 3: # If there are three consecutive pieces for the opponent
            if blockOpposite == 0: # If three consecutive pieces for the opponent are unblocked
                score = 800 # Priority reference note
            elif blockOpposite == 1: # If one out of three consecutive pieces for the opponent is blocked
                score = 80 # Priority reference note
            else: 
                score = 0 # Lowest priority
        elif countSelf == 2: # If there are two consecutive pieces for self
            if blockSelf == 0: # If two pieces for self are unblocked
                score = 100 # Priority reference note
            elif blockSelf == 1: # If one out of two pieces for self is blocked
                score = 80 # Priority reference note
            else:
                score = 0 # Lowest priority
        elif countOpposite == 2: # If there are two consecutive pieces for the opponent
            if blockOpposite == 0: # If two pieces for the opponent are unblocked
                score = 10 # Priority reference note
            elif blockOpposite == 1: # If one out of two pieces for the opponent is blocked
                score = 8 # Priority reference note
            else: 
                score = 0 # Priority is zero
        elif countSelf == 1: # If there's only a single piece for self
            score = 10 # Priority reference note
        elif countOpposite == 1: # If there's only a single piece for the opponent
            score = 8 # Priority reference note
        else:
            score = 0 # Lowest priority

        if spaceSelf or spaceOpposite: # If there are spaces within consecutive pieces for self or opponent
            score /= 2 # Reduce the priority

        return score # Return the priority

    
    # Calculate the score (weight) for a given point
    def getPointScore(self, point):
        score = 0
        for i in offset: 
            score += self.getDirectionScore(point, i[0], i[1])
        return score
    
    # machine drop
    def machineDrop(self):
        point = None 
        score = 0

        for i in range(self._pointNumber):
            for j in range(self._pointNumber):
                if self._board[j][i] == 0 and self.is_inside_diamond(Point(i, j), self._pointNumber):
                    scoreTemp = self.getPointScore(Point(i, j)) 
                    # If the priority of the current position is higher than the previous one, update the priority and position
                    if scoreTemp > score: 
                        score = scoreTemp
                        point = Point(i, j)
                    elif scoreTemp == score and scoreTemp > 0:
                        radius = random.randint(0, 100)
                        if radius % 2 == 0:
                            point = Point(i, j)
        self._board[point.Y][point.X] = self._my.Value 
        return point 
