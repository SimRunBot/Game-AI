import pygame
import numpy as np
import connect_four as c4



def draw_tokens(gameState):

    columns = len(gameState[0]) # 7
    rows = len(gameState) # 6
    radius = 50
    width = 0
    for i in range(rows):
        for j in range(columns):
            focus = gameState[i,j]
            x = 100 + j * 100
            y = 100 + i * 100
            if focus == 1:
                pygame.draw.circle(gameDisplay,blue,(x,y),radius,width)

            elif focus == -1:

                pygame.draw.circle(gameDisplay,red,(x,y),radius,width)

            else:

                pygame.draw.circle(gameDisplay,white ,(x,y),radius,width)

def draw_columns(gameState):

    columns = len(gameState[0]) # 7
    rows = len(gameState)


    for i in range(columns):
        x = 50 + i * 100
        y = 50
        width = 100
        height = width * rows
        pygame.draw.rect(gameDisplay, column_color, [x, y, width, height])

def move_by_user(gameState,player):
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # check for mouse click position, on which column it occured
                # use the column as input for placing the players token

                if mouse[0] >= 50 and mouse[0] <=150 and mouse[1] >= 50 and mouse[1] <= 650: # x and y boundaries of column 0
                    #"column 0")
                    if column_not_full(gameState,0):
                        place_token_in_column(gameState,0,player)
                        return True

                elif mouse[0] >= 150 and mouse[0] <=250 and mouse[1] >= 50 and mouse[1] <= 650:
                    #"column 1")
                    if column_not_full(gameState,1):
                        place_token_in_column(gameState,1,player)
                        return True

                elif mouse[0] >= 250 and mouse[0] <=350 and mouse[1] >= 50 and mouse[1] <= 650:
                    #"column 2")
                    if column_not_full(gameState,2):
                        place_token_in_column(gameState,2,player)
                        return True

                elif mouse[0] >= 350 and mouse[0] <=450 and mouse[1] >= 50 and mouse[1] <= 650:
                    #"column 3")
                    if column_not_full(gameState,3):
                        place_token_in_column(gameState,3,player)
                        return True

                elif mouse[0] >= 450 and mouse[0] <=550 and mouse[1] >= 50 and mouse[1] <= 650:
                    #"column 4")
                    if column_not_full(gameState,4):
                        place_token_in_column(gameState,4,player)
                        return True

                elif mouse[0] >= 550 and mouse[0] <=650 and mouse[1] >= 50 and mouse[1] <= 650:
                    #"column 5")
                    if column_not_full(gameState,5):
                        place_token_in_column(gameState,5,player)
                        return True

                elif mouse[0] >= 650 and mouse[0] <=750 and mouse[1] >= 50 and mouse[1] <= 650:
                    #"column 6")
                    if column_not_full(gameState,6):
                        place_token_in_column(gameState,6,player)
                        return True

            if event.type == pygame.KEYDOWN:
                # if q is pressed, quit game
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def place_token_in_column(gameState,column,player):

    selected_column = gameState[:,column]
    # get the index of the bottom most empty field
    fall_down_index = len(np.where(selected_column==0)[0]) - 1
    # fill field with player token
    gameState[fall_down_index, column] = player


def column_not_full(gameState,column):
    selected_column = gameState[:,column]
    return not (selected_column[selected_column==0].size == 0)


def game_loop():

    # user
    player = 1

    # loop variables
    gameover = False
    game_won = False
    game_start = True
    # our initial board is empty
    gameState = np.zeros((6,7))

    while not gameover:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameover = True
            # after game has ended, press r to reset
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()


        # background color
        gameDisplay.fill(background)
        # draw game board
        draw_columns(gameState)
        # draw tokens as circles
        # blue for player 1
        # red for player -1
        draw_tokens(gameState)
        if game_start:
            pygame.display.update()
            game_start = False



        # player simulation
        if c4.move_still_possible(gameState) and not game_won:

            # computer player
            if player == -1:
                # moves randomly
                c4.move_at_random(gameState,player)
                # check if move was winning move
                if c4.move_was_winning_move(gameState,player):

                    game_won = True

            # user player
            if player == 1:
                # loop to implement waiting on players move
                player_moved = False
                while not player_moved:

                    player_moved = move_by_user(gameState,player)

                if c4.move_was_winning_move(gameState,player):

                    game_won = True


            # swap player
            if not game_won:
                player *= -1

        # write winning message on board
        if game_won:
            winner = myfont.render("player " +str(player)+" won ", 1, black)
            gameDisplay.blit(winner, (100, 100))

            further_instructions = my_smaller_font.render("press R for another game or Q to quit",1,black)
            gameDisplay.blit(further_instructions,(100,200))

        # update display with drawn elements with 60 frames per second
        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":



    # color rgb vectors
    black = (0,0,0)
    white = (244,244,244)
    background = (241, 243, 246)
    blue = (51,153,255)
    red = (255, 51, 51)
    column_color = (255, 223, 136)



    pygame.init()

    # text font
    myfont = pygame.font.SysFont("Comic Sans MS", 72)
    my_smaller_font = pygame.font.SysFont("Comic Sans MS", 36)

    # window size
    display_width = 800
    display_height = 700
    gameDisplay = pygame.display.set_mode((display_width,display_height))

    pygame.display.set_caption('connect four')
    clock = pygame.time.Clock()

    game_loop()

    pygame.quit()
    quit()