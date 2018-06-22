import numpy as np
import matplotlib.pyplot as plt
import os.path

def move_still_possible(S):
    #only need to look at top row
    top_row = S[0,:]
    return not (top_row[top_row==0].size == 0)


def move_at_random(S, p):
    #only need to look at top row
    top_row = S[0,:]
    xs = np.where(top_row==0)
    #get random column
    i = np.random.permutation(xs[0])[0]
    # take the bottom most index for simulating the player token falling down
    fall_down_index = len(np.where(S[:,i]==0)[0]) - 1
    S[fall_down_index, i] = p

    return S

def move_was_winning_move(S, p):

    cols = len(S[0])
    rows = len(S)


    # check horizontal lines
    #row_counter = 6 # for printing of winning row
    for row in S:
        #row_counter -= 1
        # get indices of players tokens in this row
        indices = np.where(row==p)[0]
        # if atleast 4 of players tokens are placed in this row, win is possible
        if len(indices) >= 4:

            # check if indices of tokens are a winning combination, i.e. next to each other
            for i in range(len(indices)-3):

                if indices[i]+1 == indices[i+1] and indices[i+1]+1 == indices[i+2] and indices[i+2]+1 == indices[i+3] :
                    #print("horizontal win")
                    #print("row : " +str(row_counter))
                    return True

    # check vertical lines
    for j in range(len(S[0])):
        # get indices of players tokens in this column
        column = S[:,j]
        indices = np.where(column==p)[0]
        # if atleast 4 of players tokens are placed in this column, win is possible
        if len(indices) >= 4:
            # check if indices of tokens are a winning combination, i.e. next to each other
            for i in range(len(indices)-3):
                if indices[i]+1 == indices[i+1] and indices[i+1]+1 == indices[i+2] and indices[i+2]+1 == indices[i+3] :
                    #print("vertical win")
                    #print("column : " +str(j))
                    return True

    # diagonal
    # check \ diagonals
    for x in range(cols - 4):

        for y in range(rows - 2):

            if S[x,y] == p and S[x+1][y+1] == p and S[x+2][y+2] == p and S[x+3][y+3] == p:
                #print("diagonal \\ win")
                return True

    # check / diagonals
    for x in range(rows - 3):

        for y in range(3, cols):

            if S[x,y] == p and S[x+1][y-1] == p and S[x+2][y-2] == p and S[x+3][y-3] == p:
                #print("diagonal / win")
                return True

    # no winning move
    return False

def play_game_for_stats():

    player = 1
    gameState = np.zeros((6,7), dtype=int)


    while move_still_possible(gameState) :

        gameState = move_at_random(gameState,player)

        if move_was_winning_move(gameState, player):

            return player, gameState

        player *= -1

    return "draw", gameState


def make_histogram(results,name,number_of_games):

    player1_won_games = [str(x[0]) for x in results if str(x[0])=="1"]
    player2_won_games = [str(x[0]) for x in results if str(x[0])=="-1"]
    draws = [x[0] for x in results if x[0]=="draw"]

    x = []
    x.extend(player1_won_games)
    x.extend(player2_won_games)
    x.extend(draws)

    # histogram
    plt.hist(x,bins=5)
    plt.title("results of "+str(number_of_games)+" games of connect four with players playing randomly")
    plt.xlabel("player who won")
    plt.ylabel("Frequency")
    plt.savefig("./"+name+".png")

def get_stats():

    if not os.path.exists("./connect_four_x_prob_mat.npy"):

        number_of_games = 1000
        results = []
        for i in range(number_of_games):
            winner, final_gs = play_game_for_stats()
            results.append((winner,final_gs))

        # save histogram of game out comes
        make_histogram(results,"connect_four_histogram_random_move",number_of_games)

        print("calculating probabilites")
        # save probabilities of position responsible for winning for player 1
        connect_four_x_prob_mat = np.zeros_like(results[0][1])

        # results is list of tuples. first element of tuple is the winner, second the corresponding gamestate
        for game in results:
            if str(game[0]) == "1":
                # "player 1 won the game"
                # get indices of player 1 tokens
                x,y = np.where(game[1]==1)
                # add the positions to probability matrix
                for i in range(len(x)):
                    connect_four_x_prob_mat[x[i]][y[i]] += 1.0

        # normalizing probability matrix
        connect_four_x_prob_mat = connect_four_x_prob_mat/np.sum(connect_four_x_prob_mat)
        # saving to files
        np.save("./connect_four_x_prob_mat",connect_four_x_prob_mat)


if __name__ == "__main__":

    get_stats()
    print("done")
    cf_x_prob_mat = np.load("connect_four_x_prob_mat.npy")
    print(cf_x_prob_mat)
    print(np.around(cf_x_prob_mat,3))





