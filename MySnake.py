import os
import random
import sys
from collections import deque

import pygame


CELL_SIZE = 24
BOARD_WIDTH = 25
BOARD_HEIGHT = 20
BOARD_LEFT = 24
BOARD_TOP = 92
SCREEN_WIDTH = BOARD_LEFT * 2 + BOARD_WIDTH * CELL_SIZE
SCREEN_HEIGHT = BOARD_TOP + BOARD_HEIGHT * CELL_SIZE + 24
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"

BACKGROUND = (10, 16, 28)
PANEL = (20, 31, 48)
GRID = (27, 42, 62)
TEXT = (236, 242, 248)
MUTED_TEXT = (145, 163, 182)
PLAYER_HEAD = (88, 220, 118)
PLAYER_BODY = (42, 169, 91)
COMPUTER_HEAD = (83, 160, 245)
COMPUTER_BODY = (45, 106, 191)
FOOD = (248, 92, 82)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("사람 대 기계 - 8비트 뱀 게임")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        font_name = FONT_PATH if os.path.exists(FONT_PATH) else pygame.font.match_font("malgungothic")
        self.font = pygame.font.Font(font_name, 25)
        self.small_font = pygame.font.Font(font_name, 19)
        self.title_font = pygame.font.Font(font_name, 30)
        self.reset()

    def reset(self):
        center_y = BOARD_HEIGHT // 2
        self.player = [(5, center_y), (4, center_y), (3, center_y)]
        self.computer = [(BOARD_WIDTH - 6, center_y), (BOARD_WIDTH - 5, center_y), (BOARD_WIDTH - 4, center_y)]
        self.player_direction = (1, 0)
        self.next_player_direction = self.player_direction
        self.computer_direction = (-1, 0)
        self.food = self.new_food()
        self.player_score = 0
        self.computer_score = 0
        self.game_over = False
        self.result = ""
        self.paused = False
        self.move_timer = 0

    def new_food(self):
        occupied = set(self.player + self.computer)
        empty_cells = [
            (x, y)
            for y in range(BOARD_HEIGHT)
            for x in range(BOARD_WIDTH)
            if (x, y) not in occupied
        ]
        return random.choice(empty_cells) if empty_cells else None

    def set_player_direction(self, direction):
        if direction[0] + self.player_direction[0] != 0 or direction[1] + self.player_direction[1] != 0:
            self.next_player_direction = direction

    def neighbors(self, cell):
        x, y = cell
        return [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]

    def is_inside(self, cell):
        x, y = cell
        return 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT

    def choose_computer_direction(self):
        if self.food is None:
            return self.computer_direction

        blocked = set(self.computer[1:] + self.player)
        queue = deque([(self.computer[0], [])])
        visited = {self.computer[0]}
        while queue:
            cell, path = queue.popleft()
            if cell == self.food and path:
                first_step = path[0]
                return (first_step[0] - self.computer[0][0], first_step[1] - self.computer[0][1])
            for neighbor in self.neighbors(cell):
                if neighbor in visited or neighbor in blocked or not self.is_inside(neighbor):
                    continue
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        choices = [
            direction
            for direction in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if direction[0] + self.computer_direction[0] != 0
            and direction[1] + self.computer_direction[1] != 0
            and self.is_inside((self.computer[0][0] + direction[0], self.computer[0][1] + direction[1]))
            and (self.computer[0][0] + direction[0], self.computer[0][1] + direction[1]) not in blocked
        ]
        return random.choice(choices) if choices else self.computer_direction

    def next_head(self, snake, direction):
        return (snake[0][0] + direction[0], snake[0][1] + direction[1])

    def update(self):
        self.player_direction = self.next_player_direction
        self.computer_direction = self.choose_computer_direction()
        player_head = self.next_head(self.player, self.player_direction)
        computer_head = self.next_head(self.computer, self.computer_direction)
        player_grows = player_head == self.food
        computer_grows = computer_head == self.food

        player_body = self.player if player_grows else self.player[:-1]
        computer_body = self.computer if computer_grows else self.computer[:-1]
        player_crashed = not self.is_inside(player_head) or player_head in player_body or player_head in computer_body
        computer_crashed = not self.is_inside(computer_head) or computer_head in computer_body or computer_head in player_body
        if player_head == computer_head:
            player_crashed = True
            computer_crashed = True

        if player_crashed or computer_crashed:
            self.game_over = True
            if player_crashed and computer_crashed:
                self.result = "무승부!"
            elif player_crashed:
                self.result = "기계 승리!"
            else:
                self.result = "사람 승리!"
            return

        self.player.insert(0, player_head)
        self.computer.insert(0, computer_head)
        if player_grows:
            self.player_score += 10
        else:
            self.player.pop()
        if computer_grows:
            self.computer_score += 10
        else:
            self.computer.pop()
        if player_grows or computer_grows:
            self.food = self.new_food()

    def speed(self):
        return min(14, 7 + (self.player_score + self.computer_score) // 80)

    def handle_events(self):
        directions = {
            pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_r and self.game_over:
                self.reset()
            elif event.key == pygame.K_p and not self.game_over:
                self.paused = not self.paused
            elif not self.game_over and not self.paused and event.key in directions:
                self.set_player_direction(directions[event.key])
        return True

    def draw_text(self, text, position, font, color=TEXT):
        self.screen.blit(font.render(text, True, color), position)

    def cell_rect(self, cell, inset=2):
        x, y = cell
        return pygame.Rect(
            BOARD_LEFT + x * CELL_SIZE + inset,
            BOARD_TOP + y * CELL_SIZE + inset,
            CELL_SIZE - inset * 2,
            CELL_SIZE - inset * 2,
        )

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.draw_text("8비트 뱀 게임", (BOARD_LEFT, 14), self.title_font)
        self.draw_text(f"사람  {self.player_score:04d}", (BOARD_LEFT, 51), self.font, PLAYER_HEAD)
        self.draw_text(f"기계  {self.computer_score:04d}", (SCREEN_WIDTH - 145, 51), self.font, COMPUTER_HEAD)
        self.draw_text("방향키/WASD: 이동   P: 일시정지   ESC: 종료", (BOARD_LEFT, 78), self.small_font, MUTED_TEXT)

        board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, PANEL, board_rect)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                pygame.draw.rect(self.screen, GRID, self.cell_rect((x, y), 0), 1)

        if self.food is not None:
            food_rect = self.cell_rect(self.food, 4)
            pygame.draw.rect(self.screen, FOOD, food_rect)
            pygame.draw.rect(self.screen, (255, 177, 91), food_rect.inflate(-8, -8))
        self.draw_snake(self.player, PLAYER_HEAD, PLAYER_BODY, self.player_direction)
        self.draw_snake(self.computer, COMPUTER_HEAD, COMPUTER_BODY, self.computer_direction)

        if self.paused:
            self.draw_overlay("일시정지", "P 키를 눌러 계속")
        elif self.game_over:
            self.draw_overlay(self.result, "R 키를 눌러 다시 시작")
        pygame.display.flip()

    def draw_snake(self, snake, head_color, body_color, direction):
        for index, segment in enumerate(snake):
            color = head_color if index == 0 else body_color
            pygame.draw.rect(self.screen, color, self.cell_rect(segment, 2))
            if index == 0:
                self.draw_eyes(segment, direction)

    def draw_eyes(self, head, direction):
        x, y = head
        center_x = BOARD_LEFT + x * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_TOP + y * CELL_SIZE + CELL_SIZE // 2
        if direction[0]:
            eye_x = center_x + direction[0] * 5
            for offset in (-5, 5):
                pygame.draw.rect(self.screen, BACKGROUND, (eye_x, center_y + offset - 1, 3, 3))
        else:
            eye_y = center_y + direction[1] * 5
            for offset in (-5, 5):
                pygame.draw.rect(self.screen, BACKGROUND, (center_x + offset - 1, eye_y, 3, 3))

    def draw_overlay(self, title, subtitle):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 8, 16, 185))
        self.screen.blit(overlay, (0, 0))
        title_surface = self.title_font.render(title, True, TEXT)
        subtitle_surface = self.font.render(subtitle, True, FOOD)
        center_x = SCREEN_WIDTH // 2
        self.screen.blit(title_surface, title_surface.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 18)))
        self.screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(center_x, SCREEN_HEIGHT // 2 + 22)))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            elapsed = self.clock.tick(60)
            if not self.paused and not self.game_over:
                self.move_timer += elapsed
                move_interval = 1000 // self.speed()
                if self.move_timer >= move_interval:
                    self.move_timer -= move_interval
                    self.update()
            self.draw()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    SnakeGame().run()
