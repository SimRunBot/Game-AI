
import numpy as np
import os.path
import matplotlib.pyplot as plt



def move_still_possible(S):
    return not (S[S==0].size == 0)


def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    S[xs[i],ys[i]] = p

    return S

# load player x probability matrix
x_prob_mat_loaded = np.load("./tictactoe_x_prob_mat.npy")

def move_probabilistic(S, p):
    xs, ys = np.where(S==0)
    # get index of highest learned win probability that is still free in current gameState
    max_prob_index = np.argmax(x_prob_mat_loaded[xs,ys])
    S[xs[max_prob_index],ys[max_prob_index]] = p

    return S


# evalutation function from lecture slides
def num_winning_lines(T, p):
    cs = np.sum(T, axis=0) * p # column sums
    rs = np.sum(T, axis=1) * p # row sums
    s1 = cs[cs==3].size
    s2 = rs[rs==3].size
    s3 = 0
    s4 = 0
    if np.sum(np.diag(T)) * p == 3:
        s3 = 1
        s4 = 0
    if np.sum(np.diag(np.rot90(T))) * p == 3:
        s4 = 1
    return s1 + s2 + s3 + s4

# evalutation function from lecture slides
def evaluate_game_state(S, p):
    T1 = np.copy(S)
    T1[T1==0] = p
    n1 = num_winning_lines(T1, p)

    T2 = np.copy(S)
    T2[T2==0] = -p
    n2 = num_winning_lines(T2, -p)

    return n1 - n2

def move_with_heuristic(S, p):

    xs,ys = np.where(S==0)
    next_moves = []
    for i in range(len(xs)):
        U = np.copy(S)
        U[xs[i],ys[i]] = p
        next_moves.append(U)


    next_moves_evaluated = []
    for move in next_moves:
        next_moves_evaluated.append(evaluate_game_state(move,p))

    best_move = np.argmax(next_moves_evaluated)


    return next_moves[best_move]

def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False



# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print (B)


def play_game(probability_strat=False, heuristic_strat=False):
    # initialize 3x3 tic tac toe board
    gameState = np.zeros((3,3), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True


    while move_still_possible(gameState) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        #print ('%s moves' % name)

        # let player o move at random
        if name=="o":

            gameState = move_at_random(gameState, player)

        # let player x move at random
        if name=="x" and (not play_with_heuristic_strat and not play_with_probability_strat):
            print("x moved randomly")
            gameState = move_at_random(gameState, player)

        # let player x move probabilistic
        if name=="x" and probability_strat:

            gameState = move_probabilistic(gameState,player)

        # let player x move with heuristic
        if name=="x" and heuristic_strat:
            gameState = move_with_heuristic(gameState,player)

        # print current game state
        # print_game_state(gameState)

        # evaluate game state
        if move_was_winning_move(gameState, player):
            # print ('player %s wins after %d moves' % (name, mvcntr))

            return name, gameState

        # switch player and increase move counter
        player *= -1
        mvcntr +=  1



    if noWinnerYet:
        #print ('game ended in a draw' )
        return "draw",gameState

def make_histogram(results,name,number_of_games,strat=""):
    x_won_games = [x[0] for x in results if x[0]=="x"]
    o_won_games = [x[0] for x in results if x[0]=="o"]
    draws = [x[0] for x in results if x[0]=="draw"]

    x = []
    x.extend(x_won_games)
    x.extend(o_won_games)
    x.extend(draws)

    plt.hist(x,bins=5)
    plt.title("results of "+str(number_of_games)+" games "+strat)
    plt.xlabel("player who won")
    plt.ylabel("Frequency")
    plt.savefig("./"+name+".png")

if __name__ == '__main__':
    # different tasks
    play_with_probability_strat = False
    play_with_heuristic_strat = True

    results = []
    number_of_games = 2000
    for i in range(number_of_games):
        res, res_gs = play_game(probability_strat=play_with_probability_strat,heuristic_strat=play_with_heuristic_strat)
        results.append((res,res_gs))


    # save probability matrices to numpy files if they dont exist yet
    if not os.path.exists("./tictactoe_x_prob_mat.npy"):

        # histogram before probabilistic strategy
        make_histogram(results,"histogram_before_probstrat",number_of_games)

        print("calculating probabilites")
        # save probabilities of position responsible for winning for each player
        x_prob_mat = np.zeros_like(results[0][1])
        o_prob_mat = np.zeros_like(results[0][1])


        # results is list of tuples. first element of tuple is the winner, second the corresponding gamestate
        for game in results:
            if game[0] == "x":
                # "x won the game"
                x,y = np.where(game[1]==1)
                for i in range(len(x)):
                    x_prob_mat[x[i]][y[i]] += 1.0

            if game[0] == "o":
                # "o won the game"
                x,y = np.where(game[1]==-1)
                for i in range(len(x)):
                    o_prob_mat[x[i]][y[i]] += 1.0
            if game[0] == "draw":
                # "nobody won the game"
                pass

        # normalizing probability matrices
        x_prob_mat = x_prob_mat/np.sum(x_prob_mat)
        o_prob_mat = o_prob_mat/np.sum(o_prob_mat)

        # saving to files
        np.save("./tictactoe_x_prob_mat",x_prob_mat)
        np.save("./o_prob_mat",o_prob_mat)

    if play_with_probability_strat:
        make_histogram(results,"histogram_using_probstrat",number_of_games,strat=" with probabilistic")

    if play_with_heuristic_strat:
        make_histogram(results,"histogram_using_heuristic",number_of_games,strat=" with heuristic")

    print("done")
    print(x_prob_mat_loaded)
    print(np.around(x_prob_mat_loaded,3))

