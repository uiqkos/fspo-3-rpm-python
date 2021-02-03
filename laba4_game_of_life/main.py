import pygame
from GameOfLife import GameOfLife

# game = GameOfLife(*(20, 20), height=640)
# print(list(map(print, game.curr_generation)))
# print(game.get_neighbours((1, 1)))
# game.is_max_generations_exceeded


game1 = GameOfLife.from_file('./patterns/72p6h2v0.cells.txt', max_generations=100)
game1.run()

game2 = GameOfLife.from_file('./patterns/55p9h3v0.cells.txt', max_generations=100)
game2.run()

game3 = GameOfLife.from_file('./patterns/achimsp11.cells.txt', max_generations=100)
# game3.save('./patterns/test.cells.txt')
game3.run()

# game4 = GameOfLife.from_file('./patterns/5enginecordership.cells.txt', max_generations=100)
# # # game4.play_pause()
# game4.run()

game5 = GameOfLife.from_file('./patterns/ak94.cells.txt', max_generations=500)
game5.run()

game6 = GameOfLife.from_file('./patterns/94p27.1.cells.txt')
game6.run()