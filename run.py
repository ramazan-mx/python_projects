import argparse
from maze_generator import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="Rows count")
    parser.add_argument("m", help="Columns count")
    parser.add_argument("generation_type", help="Select DFS or MST algorithm generation type")
    parser.add_argument("graphics", help="Select console or gui display type")
    args = parser.parse_args()
    maze_ = Maze(int(args.n), int(args.m))
    generator_ = Generator()
    maze_ = generator_.generate(maze_, args.generation_type)
    view_ = View(maze_)
    view_.draw(args.graphics, "no")
    view_.draw(args.graphics, "yes")


if __name__ == "__main__":
    main()