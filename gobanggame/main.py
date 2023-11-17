
"""
Description:
Implementation of Gobang (Five in a Row) main function
"""
import math
import pygame 
pygame.display.init() 
import sys 
import pygame.gfxdraw
from board import Board, WHITE_CHESSMAN
from machine import Machine, BLACK_CHESSMAN, Point
from time import sleep


#define the board size
POINT_NUMBER = 15 
POINT_SIZE = 30 
INSIDE_WIDTH = 10 
OUTSIDE_WIDTH = 30 
BORDER_WIDTH = 5 
BORDER_LENGTH = POINT_SIZE * (POINT_NUMBER - 1) + 2 * INSIDE_WIDTH\
                +BORDER_WIDTH*2 
BOARD_START_PLACE = OUTSIDE_WIDTH + BORDER_WIDTH + INSIDE_WIDTH

SCREEN_HEIGHT = POINT_SIZE * (POINT_NUMBER - 1) + OUTSIDE_WIDTH * 2 + BORDER_WIDTH + INSIDE_WIDTH * 2  
SCREEN_WIDTH = SCREEN_HEIGHT + 200
TRIANGLE_SIZE = POINT_SIZE * 3 
ORANGE_COLOR = (255, 195, 87) # background color
RED_COLOR = (200, 30, 30) # text color
BLUE_COLOR = (30, 30, 200)# text color
BLACK_COLOR = (0, 0, 0) # text color
WHITE_COLOR = (255, 255, 255) 

PIECE_RADIUS_LEFT = POINT_SIZE//2 - 5 
PIECE_RADIUS_RIGHT = POINT_SIZE//2 + 5 


INFORMATION_PLACE = SCREEN_HEIGHT + 2*PIECE_RADIUS_RIGHT + 10


def printText(screen, font, x, y, text, textColor = (255, 255, 255)):
    screenText = font.render(text, True, textColor) 

    screen.blit(screenText, (x, y)) 
    

# draw the board
def drawBoard(screen):
    screen.fill(ORANGE_COLOR)  
    #draw the horizontal lines
    for i in range(POINT_NUMBER):
        # calculate the distance from the current row to the center
        distance_from_center = abs(POINT_NUMBER // 2 - i)
        start_x = BOARD_START_PLACE + distance_from_center * POINT_SIZE
        end_x = BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER - 1) - distance_from_center * POINT_SIZE

        pygame.draw.line(screen, BLACK_COLOR,
                         (start_x, BOARD_START_PLACE + POINT_SIZE * i),
                         (end_x, BOARD_START_PLACE + POINT_SIZE * i),
                         1)

    # draw the vertical lines
    for j in range(POINT_NUMBER):
        distance_from_center = abs(POINT_NUMBER // 2 - j)
        start_y = BOARD_START_PLACE + distance_from_center * POINT_SIZE
        end_y = BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER - 1) - distance_from_center * POINT_SIZE

        pygame.draw.line(screen, BLACK_COLOR,
                         (BOARD_START_PLACE + POINT_SIZE * j, start_y),
                         (BOARD_START_PLACE + POINT_SIZE * j, end_y),
                         1)

    # Plotting Heavenly Elements and Star Places
    for i in (3, 7, 11):
        for j in (3, 7, 11):
            # Skip the black dots at the specific coordinates
            if (i == 3 and j == 3) or (i == 11 and j == 11):
                continue

            if i == j:
                if i == 7:
                    radius = 3  # Heavenly Elements
                else:
                    radius = 2  # Star Places

                pygame.gfxdraw.aacircle(screen,
                                        BOARD_START_PLACE + POINT_SIZE * i,
                                        BOARD_START_PLACE + POINT_SIZE * j,
                                        radius, BLACK_COLOR)

                pygame.gfxdraw.filled_circle(screen,
                                            BOARD_START_PLACE + POINT_SIZE * i,
                                            BOARD_START_PLACE + POINT_SIZE * j,
                                            radius, BLACK_COLOR)
    #draw the border
    top_point = (BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER // 2), BOARD_START_PLACE)
    bottom_point = (BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER // 2), BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER - 1))
    left_point = (BOARD_START_PLACE, BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER // 2))
    right_point = (BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER - 1), BOARD_START_PLACE + POINT_SIZE * (POINT_NUMBER // 2))

    pygame.draw.polygon(screen, BLACK_COLOR, [top_point, right_point, bottom_point, left_point], BORDER_WIDTH)
            
# draw the chess
def drawChess(screen, Point, pieceColor):

    pygame.gfxdraw.aacircle(screen, BOARD_START_PLACE + POINT_SIZE * Point.X,
                            BOARD_START_PLACE + POINT_SIZE * Point.Y, 
                            PIECE_RADIUS_LEFT, pieceColor)

    pygame.gfxdraw.filled_circle(screen, BOARD_START_PLACE + POINT_SIZE * Point.X,
                            BOARD_START_PLACE + POINT_SIZE * Point.Y, 
                            PIECE_RADIUS_LEFT, pieceColor)


def drawChessInformation(screen, pos, color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], PIECE_RADIUS_RIGHT, color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], PIECE_RADIUS_RIGHT, color)
    

def getNextRunner(currentRunner):
    if currentRunner == BLACK_CHESSMAN: # if the current player is black, then the next player is white
        return WHITE_CHESSMAN
    else: 
        return BLACK_CHESSMAN

# draw the information panel
def drawInfomation(screen, font, currentRunner, 
                   SumOfBlackWin, SumOfWhiteWin):

    drawChess(screen, (SCREEN_HEIGHT + PIECE_RADIUS_RIGHT,
                       BOARD_START_PLACE + PIECE_RADIUS_RIGHT),
                        BLACK_CHESSMAN.pieceColor)

    drawChess(screen, (SCREEN_HEIGHT + PIECE_RADIUS_RIGHT,
                       BOARD_START_PLACE + PIECE_RADIUS_RIGHT),
                        WHITE_CHESSMAN.pieceColor)

    printText(screen, font, INFORMATION_PLACE, BOARD_START_PLACE + 3,
              "player1", BLUE_COLOR)
    printText(screen, font, INFORMATION_PLACE, 
              BOARD_START_PLACE + PIECE_RADIUS_RIGHT + 3,
              "player2", BLUE_COLOR)

# convert the mouse click position to the position on the board
def getClick(clickPlace): 
    placeX = clickPlace[0] - BOARD_START_PLACE 
    placeY = clickPlace[1] - BOARD_START_PLACE 
    if placeX < -INSIDE_WIDTH or placeY < -INSIDE_WIDTH: # if the click is outside the board
        return None
    x = placeX // POINT_SIZE 
    y = placeY // POINT_SIZE
    
    # if the click is on the border of the board, then the position is the center of the board
    if placeX % POINT_SIZE > PIECE_RADIUS_LEFT: 
        x += 1
    if placeY % POINT_SIZE > PIECE_RADIUS_LEFT:
        y += 1
    if x >= POINT_NUMBER or y >= POINT_NUMBER: 
        return None
    return Point(x, y) 
    
# main function
def main():
    history = []

    pygame.init() # initialize the pygame module
    # set the window size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # set the window title
    pygame.display.set_caption("GoBang Game")
    pygame.font.init()
    font=pygame.font.SysFont("SimHei", 72) 
    fontSmall = pygame.font.SysFont("SimHei", 42)
    fontSmallText = pygame.font.SysFont("SimHei", 18)
    textWidth, textHeight = font.size("One side wins") 
    # Print the initial menu
    screen.fill(ORANGE_COLOR)  # Fill the background color
    printText(screen, fontSmall, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4, 
                      "Game Rules", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+100, 
                      "This Gobang game includes PvP and PvE modes", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+130, 
                      "Press 'Q' to switch to PvP mode, press 'E' to switch to PvE mode", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+160, 
                      "Press 'Z'to undo the chess move ", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+190, 
                      "Wish you a pleasant gaming experience!!!", BLACK_COLOR)
    printText(screen, fontSmallText, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//4+210, 
                      "Note: This screen will automatically disappear after 5 seconds", BLACK_COLOR)
    pygame.display.flip()  # Update the screen
    sleep(5)

              
    
    board = Board(POINT_NUMBER) 
    currentRunner = BLACK_CHESSMAN # player1 is black
    winner = None 
    computer = Machine(POINT_NUMBER, WHITE_CHESSMAN) #AI#
    
    blackWinCount = 0
    whiteWinCount = 0
    
    gameType = 1 # gameType = 1 means PvE, gameType = 0 means PvP
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # if the user clicks x to close the window
                pygame.quit() 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # reset the game when the user presses Enter
                    if winner is not None: 
                        winner = None 
                        currentRunner = BLACK_CHESSMAN 
                        board = Board(POINT_NUMBER) 
                        if gameType == 1:
                            computer = Machine(POINT_NUMBER, WHITE_CHESSMAN)
                if event.key == pygame.K_q: #set the game mode to PvP when the user presses Q
                    gameType = 0
                    winner = None 
                    currentRunner = BLACK_CHESSMAN 
                    board = Board(POINT_NUMBER) 
                if event.key == pygame.K_e: #set the game mode to PvE when the user presses E
                    gameType = 1
                    winner = None 
                    currentRunner = BLACK_CHESSMAN 
                    board = Board(POINT_NUMBER)
                    computer = Machine(POINT_NUMBER, WHITE_CHESSMAN) 
                if event.key == pygame.K_z:  # press Z to undo the chess move
                    if history:
                        lastMove, lastRunner = history.pop()  
                        board.removeChess(lastMove)  
                        currentRunner = lastRunner  
                        winner = None  
            elif gameType == 1 and event.type == pygame.MOUSEBUTTONDOWN: # PvE mode, press the mouse to play
                if winner is None:
                    pressArray = pygame.mouse.get_pressed() 
                    if pressArray[0] or pressArray[2]: 
                        clickPlace = pygame.mouse.get_pos() # get the current mouse position
                        clickPoint = getClick(clickPlace) 
                        if clickPoint is not None: 
                            if board.ifDropChess(clickPoint): # check if the position is valid
                                winner = board.dropChess(currentRunner, clickPoint)
                                history.append((clickPoint, currentRunner)) # check if the player wins
                                if winner is None: 
                                    currentRunner = getNextRunner(currentRunner) 
                                    computer.getRivalDrop(clickPoint) 
                                    machinePoint = computer.machineDrop() 
                                    winner = board.dropChess(currentRunner, machinePoint) 
                                    history.append((machinePoint, currentRunner))
                                    if winner is not None: # if the player wins
                                        whiteWinCount += 1 
                                    currentRunner = getNextRunner(currentRunner)
                                else:
                                    blackWinCount += 1 # number of wins for black
                            else:
                                print("The position you clicked on already has pieces")
                        else:
                            print("You clicked outside the board area")
            elif gameType == 0 and event.type == pygame.MOUSEBUTTONDOWN: # PvP mode, press the mouse to play
                if winner is None:
                    pressArray = pygame.mouse.get_pressed() 
                    if pressArray[0] or pressArray[2]: 
                        clickPlace = pygame.mouse.get_pos() 
                        clickPoint = getClick(clickPlace) 
                        if clickPoint is not None: 
                            if board.ifDropChess(clickPoint):
                                winner = board.dropChess(currentRunner, clickPoint) 
          
                                if currentRunner == BLACK_CHESSMAN: 
                                    currentRunner = WHITE_CHESSMAN
                                else:
                                    currentRunner = BLACK_CHESSMAN
                                if winner is not None: 
                                    if winner is WHITE_CHESSMAN:
                                        whiteWinCount += 1 
                                    elif winner is BLACK_CHESSMAN:
                                        blackWinCount += 1
                            else:
                                print("The position you clicked on already has pieces")
                        else:
                            print("You clicked outside the board area")
        
        drawBoard(screen) 
        
        for y, row in enumerate(board.board):  # Iterate through the rows of the board represented as an array
            for x, column in enumerate(row):  # Iterate through the elements of each point in the array representing the board
                if column == BLACK_CHESSMAN.Value:  # If the value at column x is a black piece, draw a black piece
                    drawChess(screen, Point(x, y), BLACK_CHESSMAN.Color)
                elif column == WHITE_CHESSMAN.Value:  # If it's a white piece, draw a white piece
                    drawChess(screen, Point(x, y), WHITE_CHESSMAN.Color)
        if gameType == 1:
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 150, 
                      "Player vs Computer", BLACK_COLOR)
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 130, 
                      "Press 'Q' to Player vs Player", BLACK_COLOR)
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 110, 
                      "Press 'Z' to undo the chess move", BLACK_COLOR)
        elif gameType == 0:
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 130, 
                      "Player vs Player", BLACK_COLOR)
            printText(screen, fontSmallText, SCREEN_WIDTH - 220,
                      SCREEN_HEIGHT - 110, 
                      "Press 'E' to Player vs Computer", BLACK_COLOR)
        # Draw black and white pieces in the information panel
        drawChessInformation(screen, (SCREEN_WIDTH - PIECE_RADIUS_RIGHT - 160, 
                                      BOARD_START_PLACE + 20), BLACK_COLOR)
        drawChessInformation(screen, (SCREEN_WIDTH - PIECE_RADIUS_RIGHT - 160, 
                                      BOARD_START_PLACE + 20 + PIECE_RADIUS_RIGHT*3), WHITE_COLOR)
        # Display the number of wins for each color
        printText(screen, fontSmallText, SCREEN_WIDTH - 200,
                      SCREEN_HEIGHT - 80, 
                      "Number of wins for Black: "+str(blackWinCount), BLACK_COLOR)
        printText(screen, fontSmallText, SCREEN_WIDTH - 200,
                      SCREEN_HEIGHT - 50, 
                      "Number of wins for White: "+str(whiteWinCount), BLACK_COLOR)
        if winner:
            # Display the winner and how to start a new round at the center of the screen
            printText(screen, font, (SCREEN_WIDTH - textWidth)//2,
                      (SCREEN_HEIGHT - textHeight)//2, 
                      winner.Name + " wins", RED_COLOR)
            printText(screen, fontSmall, 
                      (SCREEN_WIDTH - textWidth)//2 - 0.25*textWidth,
                      (SCREEN_HEIGHT - textHeight)//2 + textHeight*1.5, 
                      "Press Enter to start a new game", RED_COLOR)         
            # Display the winner in the information panel
            if winner == WHITE_CHESSMAN:
                printText(screen, fontSmall, INFORMATION_PLACE,
                          BOARD_START_PLACE + PIECE_RADIUS_RIGHT*3, 
                          "Winner", BLUE_COLOR)
            else:
                printText(screen, fontSmall, INFORMATION_PLACE, BOARD_START_PLACE, 
                          "Winner", BLUE_COLOR)
        else:  # Display the current player's turn in the information panel
            if gameType == 0:
                if currentRunner == BLACK_CHESSMAN:
                    printText(screen, fontSmall, INFORMATION_PLACE, BOARD_START_PLACE, 
                          "Making a move", BLUE_COLOR)
                else:
                    printText(screen, fontSmall, INFORMATION_PLACE,
                          BOARD_START_PLACE + PIECE_RADIUS_RIGHT*3, 
                          "Making a move", BLUE_COLOR)
            elif gameType == 1:
                printText(screen, fontSmall, INFORMATION_PLACE, BOARD_START_PLACE, 
                          "Player", BLUE_COLOR)
                printText(screen, fontSmall, INFORMATION_PLACE,
                          BOARD_START_PLACE + PIECE_RADIUS_RIGHT*3, 
                          "Computer", BLUE_COLOR)

                
           
        pygame.display.flip() # refresh the screen

if __name__ == "__main__":
    main()
