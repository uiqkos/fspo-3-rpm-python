import pygame
import random

from copy import deepcopy


class Color:
    Black = (0, 0, 0)
    White = (255, 255, 255)
    Blue = (0, 0, 255)
    Green = (0, 255, 0)


class Button:
    def __init__(self, rect, color, action):
        self.rect = rect
        self.color = color
        self.action = action


class GameOfLife:
    def __init__(self, rows, cols, name='Game of Life', width=640, height=640, cell_size=None, speed=10, randomize=True, max_generations=None):

        self.name = name

        # Размеры окна
        self.width = width
        self.height = height

        # Создание нового окна
        self.screen_size = width, height + 20
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость игры
        self.speed = speed

        if cell_size is None:
            self.cell_size = self.height // rows
        else:
            self.cell_size = cell_size

        # Размер сетки
        self.rows, self.cols = rows, cols

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)

        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

        self.buttons = {
            'play_pause': Button(pygame.Rect((0, height, 20, 20)), Color.Blue, lambda game: game.play_pause()),
            'clear_button': Button(pygame.Rect((20, height, 20, 20)), Color.Green, lambda game: game.clear_grid())
        }

        self.grid_rect = pygame.Rect((0, 0, self.cell_size * self.rows, self.cell_size * self.cols))
        self.pause = False

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(
                    # screen
                    self.screen,
                    # color
                    Color.Black if self.curr_generation[row][col] else Color.White,
                    # rect
                    (
                        # x
                        col * self.cell_size,
                        # y
                        row * self.cell_size,
                        # height
                        self.cell_size,
                        # width
                        self.cell_size
                    )
                )

    def draw_buttons(self):
        for button in self.buttons.values():
            pygame.draw.rect(self.screen, button.color, button.rect)

    def draw_iterations(self):
        text_surface = self.font.render(f'Iteration: {self.generations} / {self.max_generations}', False, Color.Black)
        self.screen.blit(text_surface, (40, self.height - 5))

    def clear_screen(self):
        self.screen.fill(Color.White)

    def clear_grid(self):
        self.curr_generation = deepcopy(self.create_grid(randomize=False))

    def play_pause(self):
        self.pause = not self.pause

    def run(self) -> None:
        pygame.init()

        clock = pygame.time.Clock()
        pygame.display.set_caption(self.name)
        self.screen.fill(pygame.Color('white'))

        mouse_key_pressed = False
        mouse_pos = None
        prev_grid_pos = None
        motion_color = None

        running = True

        while running:

            if not self.pause:
                self.step()

            if self.max_generations is not None and self.generations == self.max_generations:
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_key_pressed = True
                    mouse_pos = event.pos

                    for button in self.buttons.values():
                        if button.rect.collidepoint(mouse_pos):
                            button.action(self)

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_key_pressed = False
                    motion_color = None

                if event.type == pygame.MOUSEMOTION and mouse_key_pressed:
                    mouse_pos = event.pos
                    grid_pos = int(mouse_pos[1] / self.cell_size), int(mouse_pos[0] / self.cell_size)

                    if self.grid_rect.collidepoint(mouse_pos):
                        if prev_grid_pos != grid_pos:
                            x, y = grid_pos

                            if motion_color is None:
                                motion_color = not self.curr_generation[x][y]

                            self.curr_generation[x][y] = motion_color
                            prev_grid_pos = x, y

                    continue

                if mouse_key_pressed and self.grid_rect.collidepoint(mouse_pos):
                    x, y = int(mouse_pos[1] / self.cell_size), int(mouse_pos[0] / self.cell_size)
                    self.curr_generation[x][y] = not self.curr_generation[x][y]
                    prev_grid_pos = x, y

            self.clear_screen()
            self.draw_grid()
            self.draw_iterations()
            self.draw_buttons()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize=False):
        if randomize:
            return [
                random.choices([0, 1], k=self.cols)
                for row in range(self.rows)
            ]

        # return [[0] * self.cols] * self.rows
        return [[0]*self.cols for row in range(self.rows)]

    def get_neighbours(self, cell):
        neighbours = []

        for row in range(
            cell[0] - 1 if cell[0] > 0 else 0,
            cell[0] + 2 if cell[0] < self.rows - 1 else self.rows
        ):
            for col in range(
                cell[1] - 1 if cell[1] > 0 else 0,
                cell[1] + 2 if cell[1] < self.cols - 1 else self.cols
            ):
                if (row, col) != cell:
                    neighbours.append(self.curr_generation[row][col])

        return neighbours

    def get_next_generation(self):
        next_generation = deepcopy(self.curr_generation)

        for row in range(self.rows):
            for col in range(self.cols):
                if self.curr_generation[row][col]:
                    next_generation[row][col] &= sum(self.get_neighbours((row, col))) in (2, 3)
                else:
                    next_generation[row][col] ^= sum(self.get_neighbours((row, col))) == 3

        return next_generation

    def step(self):
        self.generations += 1
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations < self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation == self.prev_generation

    @staticmethod
    def from_file(filename, *init_args, **init_kwargs):
        file = open(filename, 'r')

        converters = {
            'str': str,
            'int': int
        }

        game_params = {
            'randomize': False
        }

        lines = file.readlines()
        index = 0

        for index, line in enumerate(lines):
            if line[0] == '!':
                continue

            if line[0] == '#':
                items = lines[index][1:].split()

                for item in items:
                    param_name, param_type, param_value = item.replace(':', '=').split('=')
                    game_params[param_name] = converters[param_type](param_value)

                continue

            break

        max_len = len(max(lines[index:], key=lambda s: len(s)))
        pattern = []
        for line in lines[index:]:
            if line == '\n':
                pattern.append([0] * max_len)
                continue

            pattern.append(list(map(lambda cell: 0 if cell == '.' else 1, '{:.<{}}'.format(line[:-1], max_len))))

        pattern_rows = len(pattern)
        pattern_cols = len(pattern[0])

        game = GameOfLife(*init_args, **init_kwargs, **game_params)

        offset_vertical = game.rows - pattern_rows
        offset_horizontal = game.cols - pattern_cols

        for row_index, pattern_row in zip(range(offset_horizontal // 2, offset_horizontal // 2 + pattern_rows), pattern):
            game.curr_generation[row_index][offset_vertical // 2 : offset_vertical // 2 + pattern_cols] = pattern_row

        return game

    def save(self, filename):
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'w')
        file.write(f'# name:str={self.name} rows:int={self.rows} cols:int={self.cols} \n')
        file.write('\n'.join([''.join(map(lambda cell: '.' if cell == 0 else 'O', row)) for row in self.curr_generation]))
        file.write('\n')
