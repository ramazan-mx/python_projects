from .cell import Cell
from .maze import Maze
from .generator import Generator
from .solver import Solver

import colorama
from colorama import Fore, Back, Style

import os


class View:
    _maze = Maze()

    def __init__(self, maze_=Maze()):
        self._maze = maze_

    @property
    def maze(self):
        return self._maze

    @maze.setter
    def maze(self, value):
        self._maze = value

    def maze_to_string(self, with_path="yes"):
        def sym(t):
            if t == "b":
                return "#"
            elif t == "e":
                return " "
            elif t == "p":
                return "@"
            elif t == "f":
                return "$"

        path = []
        if with_path == "yes":
            solver_ = Solver(self._maze)
            path = solver_.solve()

        walls = {"top": [[-1, 0], [-1, 1]],
                 "left": [[0, -1], [1, -1]],
                 "bot": [[2, 0], [2, 1]],
                 "right": [[0, 2], [1, 2]],
                 }
        cell_inner = [[0, 0], [0, 1],
                      [1, 0], [1, 1],
                      ]

        size = self._maze.size
        output = [["#" for i in range(size[1] * 4 + 2)] for i in range(size[0] * 4 + 2)]

        map = self._maze.map
        for i in range(len(path) - 1):
            cell_ = path[i]
            neighbour_ = path[i + 1]
            type_ = cell_.neighbour_type(neighbour_)
            out_cell_i = 2 + 4 * cell_[0]
            out_cell_j = 2 + 4 * cell_[1]
            out_n_i = 2 + 4 * neighbour_[0]
            out_n_j = 2 + 4 * neighbour_[1]
            for wall in walls:
                for move in walls[wall]:
                    if not getattr(cell_, "wall_" + wall) and wall != type_:
                        output[out_cell_i + move[0]][out_cell_j + move[1]] = sym("e")
            for move in cell_inner:
                output[out_cell_i + move[0]][out_cell_j + move[1]] = sym("p")
            for move in walls[type_]:
                output[out_cell_i + move[0]][out_cell_j + move[1]] = sym("p")
            type_ = neighbour_.neighbour_type(cell_)
            for wall in walls:
                for move in walls[wall]:
                    if not getattr(neighbour_, "wall_" + wall) and wall != type_:
                        output[out_n_i + move[0]][out_n_j + move[1]] = sym("e")
            for move in cell_inner:
                output[out_n_i + move[0]][out_n_j + move[1]] = sym("p")
            for move in walls[type_]:
                output[out_n_i + move[0]][out_n_j + move[1]] = sym("p")
            if i != 0:
                neighbour_ = path[i - 1]
                type_ = cell_.neighbour_type(neighbour_)
                for move in walls[type_]:
                    output[out_cell_i + move[0]][out_cell_j + move[1]] = sym("p")

        out_begin_i = 2 + 4 * self._maze.begin[0]
        out_begin_j = 2 + 4 * self._maze.begin[1]
        out_end_i = 2 + 4 * self._maze.end[0]
        out_end_j = 2 + 4 * self._maze.end[1]
        for move in cell_inner:
            output[out_begin_i + move[0]][out_begin_j + move[1]] = sym("f")
            output[out_end_i + move[0]][out_end_j + move[1]] = sym("f")

        for i in range(size[0]):
            for j in range(size[1]):
                cell = self._maze[i, j]
                if cell not in path:
                    out_i = 2 + 4 * i
                    out_j = 2 + 4 * j
                    for move in cell_inner:
                        output[out_i + move[0]][out_j + move[1]] = " "
                    for wall in walls:
                        if not getattr(cell, "wall_" + wall):
                            for move in walls[wall]:
                                output[out_i + move[0]][out_j + move[1]] = " "
        output_string = ""
        for line in output:
            output_string += "".join(line) + "\n"
        return output_string

    def draw_console(self, with_path):
        def border():  # border
            prefix = Fore.WHITE + Back.WHITE
            postfix = Style.RESET_ALL
            return prefix + "\u2B1B" + postfix

        def empty():  # empty
            prefix = Fore.BLACK + Back.BLACK
            postfix = Style.RESET_ALL
            return prefix + "\u2B1B" + postfix

        def path():  # path
            prefix = Fore.GREEN + Back.GREEN
            postfix = Style.RESET_ALL
            return prefix + "\u2B1B" + postfix

        def begin_finish():  # begin/finish
            prefix = Fore.BLUE + Back.BLUE
            postfix = Style.RESET_ALL
            return prefix + "\u2B1B" + postfix

        colorama.init()

        maze_string = self.maze_to_string(with_path)
        beautiful_maze_string = ""
        for symbol in maze_string:
            if symbol == "#":
                beautiful_maze_string += border()
            elif symbol == ' ':
                beautiful_maze_string += empty()
            elif symbol == '@' and with_path == "yes":
                beautiful_maze_string += path()
            elif symbol == '$':
                beautiful_maze_string += begin_finish()
            elif symbol == "\n":
                beautiful_maze_string += symbol

        print(beautiful_maze_string)

    def draw_graphics(self, with_path):
        pass

    def draw(self, type_="console", path_="yes"):
        if type_ == "console":
            self.draw_console(path_)
        else:
            self.draw_graphics(path_)

    def load(self, path):
        file_ = None
        try:
            file_ = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError("There's no such labyrinth file")
        lines = file_.readlines()
        n = (len(lines) - 2) // 4
        m = (len(lines[0]) - 2) // 4
        self._maze = Maze(n, m)
        walls = {"top": [-1, 1],
                 "left": [0, -1],
                 "bot": [2, 0],
                 "right": [1, 2],
                 }

        for i in range(n):
            for j in range(m):
                current_cell = Cell(n=n, m=m, i=i, j=j)
                c_i = 2 + 4 * i
                c_j = 2 + 4 * j
                for wall in walls:
                    move_i = c_i + walls[wall][0]
                    move_j = c_j + walls[wall][1]
                    setattr(current_cell, "wall_" + wall, "#" == lines[move_i][move_j])
                self._maze[i, j] = current_cell

    def save(self, path):
        output_string = self.maze_to_string()
        if "labyrinths" not in os.listdir(path):
            os.mkdir(path + "labyrinths")
        labyrinths = os.listdir(path + "labyrinths")
        count = 1
        for filename in labyrinths:
            if filename.startswith("labyrinth"):
                count += 1
        file_ = open(path + "labyrinths/labyrinth" + str(count) + ".txt", "w")
        file_.write(output_string)
        file_.close()
