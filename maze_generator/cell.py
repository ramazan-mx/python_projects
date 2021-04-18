class Cell:
    walls_ = [True, True, True, True]
    maze_size_ = (0, 0)
    position_ = (0, 0)

    @staticmethod
    def if_exists(arguments, variable):
        if variable in arguments:
            return int(arguments[variable])
        return 0

    def __init__(self, **kwargs):
        arguments = dict(kwargs)
        self.maze_size_ = (Cell.if_exists(arguments, "n"),
                           Cell.if_exists(arguments, "m"))
        self.position_ = (Cell.if_exists(arguments, "i"),
                          Cell.if_exists(arguments, "j"))
        self.walls_ = [True, True, True, True]

    def __int__(self):
        return self.position_[0] * self.maze_size_[1] + self.position_[1]

    def __getitem__(self, index):
        return self.position_[index]

    def __setitem__(self, index, value):
        self.position_[index] = value

    def __eq__(self, other_cell):
        return self.maze_size_ == other_cell.maze_size_ and self.position_ == other_cell.position_

    def __neq__(self, other_cell):
        return not (self == other_cell)

    @property
    def position(self):
        return self.position_

    @property
    def maze_size(self):
        return self.maze_size_

    @property
    def wall_top(self):
        return self.walls_[0]

    @property
    def wall_left(self):
        return self.walls_[1]

    @property
    def wall_bot(self):
        return self.walls_[2]

    @property
    def wall_right(self):
        return self.walls_[3]

    @position.setter
    def position(self, value):
        self.position_ = value

    @maze_size.setter
    def maze_size(self, value):
        self.maze_size_ = value

    @wall_top.setter
    def wall_top(self, value):
        self.walls_[0] = value

    @wall_left.setter
    def wall_left(self, value):
        self.walls_[1] = value

    @wall_bot.setter
    def wall_bot(self, value):
        self.walls_[2] = value

    @wall_right.setter
    def wall_right(self, value):
        self.walls_[3] = value

    def is_top(self, other_cell):
        return self.position_[0] - 1 == other_cell.position[0]

    def is_left(self, other_cell):
        return self.position_[1] - 1 == other_cell.position[1]

    def is_bot(self, other_cell):
        return self.position_[0] + 1 == other_cell.position[0]

    def is_right(self, other_cell):
        return self.position_[1] + 1 == other_cell.position[1]

    def neighbour_type(self, other_cell):
        if self.is_top(other_cell):
            return "top"
        if self.is_left(other_cell):
            return "left"
        if self.is_bot(other_cell):
            return "bot"
        if self.is_right(other_cell):
            return "right"