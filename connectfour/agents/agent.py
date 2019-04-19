class Agent:
    def __init__(self, name):
        self.name = name
        self.id = ""

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        
        raise NotImplementedError

    def __repr__(self):
        return self.name


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
