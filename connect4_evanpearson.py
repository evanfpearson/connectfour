# -*- coding: utf-8 -*-

""" 


EVAN FRANKIE PEARSON
9453469

============================
CONNECT FOUR COURSEWORK 2017
============================


""" 
from copy import deepcopy 
from random import sample

def saveGame(game):
    """
    Function writes data from the game dictionary in a format that can be
    understood by the loadGame() function.
    
    It saves the data to game.txt 
    """
    with open("game.txt", "wt", encoding="utf8") as g:
        g.write(str(game['player1']) + "\n")
        g.write(str(game['player2']) + "\n")
        g.write(str(game['who']) + "\n")
        for i in range(5):
            bd = []
            for j in range(7):   
                bd.append(str(game['board'][i][j]))
            g.write(",".join(bd) + "\n")
        bd = []
        for j in range(7):   
            bd.append(str(game['board'][5][j]))
        g.write(",".join(bd))
        
def newGame(player1,player2):  
    """   
    
    Function which returns the game dictionary
    The game dictionary gives us information about the current game:
        The names of the 2 players
        Whose turn is next
        The state of the board
        
    """
    game = {
            "player1": player1,
            "player2": player2,
            "who": 1,
            "board": [[0 for i in range(7)] for i in range(6)]
            }     
    return game  

def printBoard(board): # call using printBoard(newGame('p1','p2')['board'])
    """
    Prints the board aesthetically
    """
    letterBoard = [[] for i in range(6)]
    for i in range(6):
        for el in board[i]:
            if el == 0:
                letterBoard[i].append(" ")
            else:
                if el == 1:
                    letterBoard[i].append("X")
                else:
                    letterBoard[i].append("O")
    print("\n|1|2|3|4|5|6|7|")
    print("+-+-+-+-+-+-+-+")
    for i in range(6):
        print("|" + "|".join(letterBoard[i]) + "|")
    print("+-+-+-+-+-+-+-+\n")

def loadGame(): 
    """
    Opens the file game.txt which holds a saved game
    Returns the game dictionary of this game
    
    If the file is damaged, or in the wrong format, the program will raise an
    exception and the player will be notified.
    """
    with open("game.txt", mode = "rt", encoding = "utf8") as g:
        glist = g.readlines()

    sboard = []
    for i in range(3, 8):
        sboard.append(glist[i][:-1].split(","))
    sboard.append(glist[8].split(","))
    
    
    try:
        iboard = [[] for i in range(6)]
        for i in range(6):
            for j in range(7):
                iboard[i].append(int(sboard[i][j]))
        if len(glist[0][0:-1]) < 1 or len(glist[1][:-1]) < 1:
           raise ValueError("Players can not have names with length zero")
        for i in range(6):
            if len(iboard[i]) != 7:
                raise ValueError("The board has the wrong layout")
            for j in range(7):
                if iboard[i][j] not in (0,1,2):
                    raise ValueError("The board has the wrong layout")
        if int(glist[2]) not in (1,2):
            raise ValueError("The Game load has an error")
    except ValueError:
        print("You Can Not Load This Game. There is a File Error.")
        return False
    
    game = {
        "player1": glist[0][0:-1],
        "player2": glist[1][:-1],
        "who": int(glist[2]),
        "board": iboard
            }
    return game

def getValidMoves(board):
    """
    Takes the board status as a list of lists
    Returns a new list which indicates which columns our players can play with
    """
    validMoves = []
    for i in range(7):
        if board[0][i] == 0:
            validMoves.append(i)
    return validMoves

def makeMove(board,move,who):
    """
    Takes as input:
        A Board
        A column "move" 
        A player "who"
    places a disc for player "who" in column "move" and returns this game board
    """
    for i in range(6):
        if board[5-i][move] == 0:
            board[5-i][move] = who
            break
    return board

def hasWon(board, who):
    """
    Checks the board to see if player "who" has won the game.
    """
    win = False
    # Check if there are any vertical wins
    for i in range(3):
        for j in range(7):
            if (board[5-i][j], board[4-i][j], board[3-i][j], board[2-i][j]) == (who, who, who, who):
                win = True
                break
    # Check if there are any horizontal wins
    for i in range(6):
        for j in range(4):
            if (board[5-i][j], board[5-i][j+1], board[5-i][j+2], board[5-i][j+3]) == (who, who, who, who):
                win = True
                break
    # Check if there are any diagonal wins
    for i in range(3):
        for j in range(4):
            if (board[5-i][j], board[4-i][j+1], board[3-i][j+2], board[2-i][j+3]) == (who, who, who, who):
                win = True
                break
    # Check if there are any a-diagonal wins
    for i in range(3):
        for j in range(4):
            if (board[5-i][j+3], board[4-i][j+2], board[3-i][j+1], board[2-i][j]) == (who, who, who, who):
                win = True
                break
    return win

def inList(L1, L2):
    """
    Takes two lists.
    If both lists have the same elements, independent of order, the function 
    returns True. 
    If not, the function returns False.
    """
    inLst = False
    for el in L1:
        if el in L2:
            L2.remove(el)
        else: 
            break
    if len(L2) == 0:
        inLst = True
    
    return inLst

def hasThreeV(board, who, move):
    """
    Takes a possible future board, the possible move
    and who made the move as an input.
    
    It tells us if that move leads to a situation with 3 pieces in a row
    vertically.
    """
    threeV = False
    y = 0
    for i in range(1,6):
        if board[5-i][move] == 0:
            y = 6-i
            break
    if y < 4:
        for i in range(3):
            if (board[y][move], board[y+1][move], board[y+2][move]) == (who, who, who):
                threeV = True
    return threeV

def hasThreeH(board, who, move):
    """
    Checks the board to see if player "who" has three horizontal pieces
    within 4 spaces after making the specified move.
    """
    threeH = False
    # find y-co-ordinate
    y = 0
    for i in range(1,6):
        if board[5-i][move] == 0:
            y = 6-i
            break
    for i in range(4):
        if (move in range(i,i+3)) and inList([board[y][i], board[y][i+1], board[y][i+2], board[y][i+3]], [0, who, who, who]):
            threeH = True
    return threeH

def hasThreeD(board, who, move):
    """
    Checks the board to see if player "who" has three diagonal pieces
    within 4 spaces after making the specified move.
    """
    threeD = False
    # find y-co-ordinate
    y = 0
    for i in range(1,6):
        if board[5-i][move] == 0:
            y = 6-i
            break
    for i in range(4):
        for j in range(3,6):
            if (move, y) in [(i+k, j-k) for k in range(4)] and inList([board[j][i], board[j-1][i+1], board[j-2][i+2], board[j-3][i+3]], [0, who, who, who]):
                threeD = True
            if (move, y) in [(i-k, j-k) for k in range(4)] and inList([board[j][6-i], board[j-1][5-i], board[j-2][4-i], board[j-3][3-i]], [0, who, who, who]):
                threeD = True
    return threeD
      
def suggestMove1(board, who):
    """
    Analyses all possible moves on the board for player "who"
    
    if there is a move which can immediately win for "who" or can stop an
    immediate loss for "who" then this move is chosen.
    
    otherwise, a random move is chosen.
    """                
    move = sample(getValidMoves(board),1)[0] # Chooses random move incase there is no obvious win/loss
    
    opp = 1
    if who == 1: opp = 2

    for el in getValidMoves(board):
        whoMove = makeMove(deepcopy(board), el, who)
        oppMove = makeMove(deepcopy(board), el, opp)
        if hasWon(whoMove,who):
            move = el
            break
        else:
            if hasWon(oppMove,opp):
                move = el
    
    return move

def suggestMove2(board, who):
    """
    Analyses all possible moves on the board for player "who"
    
    if there is a move which can immediately win for "who" or can stop an
    immediate loss for "who" then this move is chosen.
    
    otherwise, it checks if a move can stop dangers or possible attacks and
    will choose its next move accordingly.
    """
    bestMoves = [0,1,1,3,1,1,0]

    opp = 1
    if who == 1: opp = 2
    
    for el in getValidMoves(board):
        whoMove = makeMove(deepcopy(board), el, who) #returns board, with who in column el
        oppMove = makeMove(deepcopy(board), el, opp) #returns board, with opp in column el
        validWhoMoves = getValidMoves(whoMove) # valid moves when a disc is placed in column "move"
        if hasWon(whoMove, who):
            bestMoves[el] += 100 

        if hasWon(oppMove, opp):
            bestMoves[el] += 50

        if hasThreeH(oppMove, opp, el):
            bestMoves[el] += 2.5
        
        if hasThreeH(whoMove, who, el):
            bestMoves[el] += 2
        
        if hasThreeV(whoMove,who, el):
            bestMoves[el] += 2
        
        if hasThreeV(oppMove, opp, el):
            bestMoves[el] += 2.5
                     
        if hasThreeD(whoMove, who, el):
            bestMoves[el] += 2
        
        if hasThreeD(oppMove, opp, el):
            bestMoves[el] += 2.5
           
        if el in validWhoMoves: 
            if hasWon(makeMove(deepcopy(whoMove), el, who), who):
                bestMoves[el] -= 15
                if hasThreeV:
                    bestMoves[el] += 13
            if hasWon(makeMove(deepcopy(whoMove), el, opp), opp):
                bestMoves[el] -= 45
            
            if hasThreeD(makeMove(deepcopy(whoMove), el, who), who, el):
                bestMoves[el] -= 2
        
            if hasThreeD(makeMove(deepcopy(whoMove), el, opp), opp, el):
                bestMoves[el] -= 2.5

            if hasThreeH(makeMove(deepcopy(whoMove), el, who), who, el):
                bestMoves[el] -= 2
        
            if hasThreeH(makeMove(deepcopy(whoMove), el, opp), opp, el):
                bestMoves[el] -= 2.5          
    bestQual = -50
    bestMove = 0
    #print(bestMoves)
    for i in range(7):
        if bestMoves[i] >= bestQual:
            if i in getValidMoves(board):
                bestMove = i
                bestQual = bestMoves[i]
    return bestMove     
 
# ------------------- Main function --------------------

def play():
    """      
    Play function utilises all functions already written.

    Begins by requesting the names of the players by input.
        These inputs cannot be empty strings
        If either of the inputs is 'C', then that player will be the computer
    
    ================
    THE GAME BEGINS
    ================
    
    The function prints the board before each turn.
    
    The function asks the player to make a move.
        The player's disk will be placed in the requested column
        if the player inputs an incorrect column or string, they will be asked for another input.
        if the player types "s" or "S", the game will be saved
        
    
    """     
    print("*"*55)     
    print("***"+" "*9+"WELCOME TO EVAN'S CONNECT FOUR!"+" "*9+"***")     
    print("*"*55,"\n")     
    print("Enter the players' names:\nType 'C' to play against an easy computer\nType 'H' to play against a harder computer\nType 'L' to load a saved game.\n")    
    
    # Player name inputs
    
    player1 = (input("Player 1: ")).title()
    while player1 == "" or (player1 == "L" and loadGame() == False):
        player1 = input("Player 1: ").title()
    if player1 == "L":
        game = loadGame()
    else:
        player2 = input("Player 2: ").title()
        while player2 == "":
            player2 = input("Player 2: ").title()
        game = newGame(player1, player2)
        
    # Setting up board, who and opponent
    player1, player2, board, who = game['player1'], game['player2'], game['board'], game['who']
    printBoard(board)
    
    name1 = player1 + " ~~ X ~~"
    if player1 == "C" or player1 == "H": name1 = "Computer ~~ X ~~"
        
    name2 = player2 + " ~~ O ~~"
    if player2 == "C" or player2 == "H": name2 = "Computer ~~ O ~~"
    
    players = [player1, player2]
    names = [name1, name2]
    #Making Moves
    while True: # loop breaks when there is a winner
        if len(getValidMoves(board)) == 0:
            print("There is no winner!")
            break
        if players[who-1] == "H":
            hMove = suggestMove2(board, who)
            makeMove(board, hMove, who)
            print("The {} placed a disk in column {}".format(names[who-1], hMove + 1))
            printBoard(board)
            
        else:
            if players[who-1] == "C":
                cMove = suggestMove1(board, who)
                makeMove(board, cMove, who)
                print("The {} placed a disk in column {}".format(names[who-1], cMove + 1))
                printBoard(board)
            else:
                # Steps to take if player is non-computer
                while True: # loop breaks after a valid input
                    entry = input(names[who-1] + " Where would you like to move? ")
                    try:
                        move = int(entry) - 1
                        if move in getValidMoves(board):
                            makeMove(board, move, who)
                            break
                        else:
                            print("That is not a valid move")
                    except ValueError:
                        if entry.lower() == 's':
                            saveGame(game)
                            print("Game Saved!")
                        else:
                            print("That is not a valid move")
                printBoard(board)
    
        if hasWon(board, who): # If there is a winner break the loop
            print(names[who-1] + " Wins!!!!!")
            break
        else: # go back to the start of the loop, it's the other players turn
            if who == 1: who += 1
            else: who -= 1
# the following allows your module to be run as a program 
if __name__ == '__main__' or __name__ == 'builtins':
    play() 