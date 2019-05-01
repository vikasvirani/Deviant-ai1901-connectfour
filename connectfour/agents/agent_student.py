from connectfour.agents.computer_player import RandomAgent
from time import gmtime
import copy
import random
import math

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4
        self.count = 0

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        valid_moves = board.valid_moves()
        vals = []
        moves = []
        self.count += 1
        #random.shuffle(list(valid_moves))

        for move in valid_moves:
            board_test = copy.deepcopy(board)
            next_state_test = board_test.next_state(self.id % 2 + 1, move[1])
            if next_state_test.winner() != 0:
                return move
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            if next_state.winner() != 0:
                return move
            vals.append( self.dfMiniMax(next_state, 1,-math.inf, math.inf) )

        #print(vals)
        #random.shuffle(list(vals))
        max_count = vals.count(max(vals))
        max_index = []

        if max_count > 1:
            for i in range(len(vals)):
                if vals[i] == max(vals):
                    max_index.append(i)

            bestMove = moves[max_index[int(max_count/2)]]
        else:
            bestMove = moves[vals.index( max(vals) )]

        return bestMove

    def dfMiniMax(self, board, depth, alpha, beta):
        # Goal return column with maximized scores of all possible next states

        if  board.terminal() is False:
            if board.winner() == self.id:
                return 1
            elif board.winner() == self.id % 2 + 1:
                return -1
        else:
            return 0

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board, depth)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        #random.shuffle(list(valid_moves))

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1, alpha, beta) )

            if depth % 2 == 1:
                beta = min(min(vals), beta)
                if alpha >= beta:
                    break
            else:
                alpha = max(alpha, max(vals))
                if alpha >= beta:
                    break

        #print(vals)
        #print("Player :"+ str(depth % 2))
        #print(str(self.count))
        max_count = vals.count(max(vals))
        max_index = []
        min_count = vals.count(min(vals))
        min_index = []

        if depth % 2 == 1:
            if min_count > 1:
                for i in range(len(vals)):
                    if vals[i] == min(vals):
                        min_index.append(i)

                bestVal = vals[min_index[int(min_count/2)]]
            else:
                bestVal = min(vals)
        else:
            if max_count > 1:
                for i in range(len(vals)):
                    if vals[i] == max(vals):
                        max_index.append(i)

                bestVal = vals[max_index[int(max_count/2)]]
            else:
                bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board, depth):

        #cStart=time()

        #nbmove = self.count + (depth/2)

        my_fours = self.checkStreak(board, 4, self.id)
        my_threes = self.checkStreak(board, 3, self.id)
        my_twos = self.checkStreak(board, 2, self.id)
        opp_fours = self.checkStreak(board, 4,  self.id % 2 + 1)
        opp_threes = self.checkStreak(board, 3, self.id % 2 + 1)
        opp_twos = self.checkStreak(board, 2, self.id % 2 + 1)

        final_score = ((((my_fours*196) + (my_threes*9) + (my_twos*1)) - ((opp_fours*196) + (opp_threes*9) + (opp_twos*1)))/5000)
        # + (22-nbmove)/18)/2
        #time()-cStart

        return final_score

    def checkStreak(self, board, streak, turn):
        count = 0

        count += self._check_rows(board, streak, turn)
        count += self._check_columns(board, streak, turn)
        count += self._check_diagonals(board, streak, turn)

        # return the sum of streaks of length 'streak'
        return count

    def _check_rows(self, board, streak, turn):
        count = 0
        for row in range(board.height):
            for j in range(0, board.width - board.num_to_connect + 1):
                same_count = 0
                curr = turn
                for k in range(0, board.num_to_connect):
                    if board.board[row][j+k] != (turn % 2 + 1):
                        if board.board[row][j+k] == curr:
                            same_count += 1
                    else:
                        same_count = 0
                        break
                if same_count == streak:
                    count += 1
        return count

    def _check_columns(self, board, streak, turn):
        count = 0
        for i in range(board.width):
            for j in range(board.height - board.num_to_connect + 1):
                same_count = 0
                curr = turn
                for k in range(0, board.num_to_connect):
                    if board.board[j+k][i] != (turn % 2 + 1):
                        if board.board[j+k][i] == curr:
                            same_count += 1
                    else:
                        same_count = 0
                        break
                if same_count == streak:
                    count += 1
        return count

    def _check_diagonals(self, board, streak, turn):
        count = 0
        boards = [
            board.board,
            [row[::-1] for row in copy.deepcopy(board.board)]
        ]

        for b in boards:
            for i in range(board.width - streak + 1):
                for j in range(board.height - streak + 1):
                    if i > 0 and j > 0:  # would be a redundant diagonal
                        continue

                    # (j, i) is start of diagonal
                    same_count = 0
                    curr = turn
                    k, m = j, i
                    while k < board.height - board.num_to_connect and m < board.width - board.num_to_connect:
                        for l in range(0, board.num_to_connect):
                            if b[k+l][m+l] != (turn % 2 + 1):
                                if b[k+l][m+l] == curr:
                                    same_count += 1
                            else:
                                same_count = 0
                                break
                        if same_count == streak:
                            count += 1
                        k += 1
                        m += 1
        return count
