import pygame
import sys
import random
import os

# Constants
WIDTH = 600
HEIGHT = 500
FPS = 60
BALL_RADIUS = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BLOCK_HEIGHT = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
score_file = "top_scores2.txt"


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.top_scores_x, self.top_scores_y = self.mid_w, self.mid_h + 50  # Updated line
        self.exit_x, self.exit_y = self.mid_w, self.mid_h + 70  # Updated line
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Top Scores", 20, self.top_scores_x, self.top_scores_y)  # Updated line
            self.game.draw_text("Exit", 20, self.exit_x, self.exit_y)  # Updated line
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.top_scores_x + self.offset, self.top_scores_y)  # Updated line
                self.state = 'Top Scores'  # Updated line
            elif self.state == 'Top Scores':  # Updated line
                self.cursor_rect.midtop = (self.exit_x + self.offset, self.exit_y)  # Updated line
                self.state = 'Exit'  # Updated line
            elif self.state == 'Exit':  # Updated line
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exit_x + self.offset, self.exit_y)  # Updated line
                self.state = 'Exit'  # Updated line
            elif self.state == 'Top Scores':  # Updated line
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Exit':  # Updated line
                self.cursor_rect.midtop = (self.top_scores_x + self.offset, self.top_scores_y)  # Updated line
                self.state = 'Top Scores'  # Updated line

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Top Scores':  # Updated line
                self.game.curr_menu = self.game.topscores  # Updated line
            elif self.state == 'Exit':  # Updated line
                self.game.curr_menu = self.game.exit  # Updated line
            self.run_display = False

class TopScores(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Top scores'
        self.top_scores = self.load_top_scores()

    def print_top_scores(self, screen):
        self.game.draw_text("TOP 3 SCORES", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)

        for i, top_score in enumerate(self.top_scores[:3], 1):
            self.game.draw_text(f"{i} {top_score}", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + i * 30)

    def save_top_scores(self):
        with open(score_file, 'w') as file:
            for top_score in self.top_scores:
                file.write(f"{top_score}\n")

    def load_top_scores(self):
        if os.path.exists(score_file):
            with open(score_file, 'r') as file:
                return [int(line.strip()) for line in file]
        else:
            return [0, 0, 0]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.print_top_scores(self.game.display)  # Use the print_top_scores method
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False




class Exit(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "No"
        self.yesx, self.yesy = self.mid_w, self.mid_h + 30
        self.nox, self.noy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.yesx + self.offset, self.yesy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Exit Game?', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Yes", 20, self.yesx, self.yesy)
            self.game.draw_text("No", 20, self.nox, self.noy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == 'No':
                self.cursor_rect.midtop = (self.yesx + self.offset, self.yesy)
                self.state = 'Yes'
            else:
                self.cursor_rect.midtop = (self.nox + self.offset, self.noy)
                self.state = 'No'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Yes':
                pygame.quit()
                sys.exit()
            elif self.state == 'No':
                self.game.curr_menu = self.game.main_menu
            self.run_display = False

class Ball:
    def __init__(self, radius, speed, initial_position):
        self.radius = radius
        self.speed = speed
        self.position = initial_position
        self.direction = [1, -1]

    def move(self):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]

class Paddle:
    def __init__(self, width, height, speed, initial_position):
        self.width = width
        self.height = height
        self.speed = speed
        self.position = initial_position

    def move_left(self):
        if self.position[0] > 0:
            self.position[0] -= self.speed

    def move_right(self):
        if self.position[0] + self.width < WIDTH:
            self.position[0] += self.speed

class Block:
    def __init__(self, num_cols, row, col):
        self.width = WIDTH // num_cols
        self.height = BLOCK_HEIGHT
        self.position = [col * self.width, row * self.height]

class Game:
    def __init__(self, paddle, ball, blocks):
        self.DISPLAY_W, self.DISPLAY_H = 600, 500
        self.paddle = paddle
        self.ball = ball
        self.blocks = blocks
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.top_scores_menu = TopScores(self)

    def detect_collision(self, dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.position[0] + ball.radius - rect.position[0]
        else:
            delta_x = rect.position[0] + rect.width - ball.position[0] + ball.radius
        if dy > 0:
            delta_y = ball.position[1] + ball.radius - rect.position[1]
        else:
            delta_y = rect.position[1] + 1 - ball.position[1] + ball.radius

        if abs(delta_x - delta_y) < 1:
            ball.direction[0], ball.direction[1] = -ball.direction[0], -ball.direction[1]
        elif delta_x > delta_y:
            ball.direction[1] = -ball.direction[1]
        elif delta_y > delta_x:
            ball.direction[0] = -ball.direction[0]

    def update_game(self):
        # Ball movement
        self.ball.move()

        # Collision left/right
        if self.ball.position[0] < self.ball.radius or self.ball.position[0] > WIDTH - self.ball.radius:
            self.ball.direction[0] = -self.ball.direction[0]

        # Collision top
        if self.ball.position[1] < self.ball.radius:
            self.ball.direction[1] = -self.ball.direction[1]

        # Collision paddle
        if (
                self.paddle.position[0] <= self.ball.position[0] <= self.paddle.position[0] + self.paddle.width
                and self.ball.position[1] == HEIGHT - PADDLE_HEIGHT - self.ball.radius
        ):
            self.detect_collision(self.ball.direction[0], self.ball.direction[1], self.ball, self.paddle)

        # Collision blocks
        for block in self.blocks[:]:
            if (
                    block.position[0] <= self.ball.position[0] <= block.position[0] + block.width
                    and block.position[1] <= self.ball.position[1] <= block.position[1] + block.height
            ):
                self.detect_collision(self.ball.direction[0], self.ball.direction[1], self.ball, block)
                self.blocks.remove(block)
                self.score += 10

        # Win/game over
        if self.ball.position[1] > HEIGHT - 1:
            print("Game Over!")
            self.top_scores_menu.top_scores.append(self.score)
            self.top_scores_menu.top_scores.sort(reverse=True)
            self.top_scores_menu.top_scores = self.top_scores_menu.top_scores[:3]
            self.top_scores_menu.save_top_scores()
            return False
        elif not self.blocks:
            print("You Win!!!")
            self.top_scores_menu.top_scores.append(self.score)
            self.top_scores_menu.top_scores.sort(reverse=True)
            self.top_scores_menu.top_scores = self.top_scores_menu.top_scores[:3]
            self.top_scores_menu.save_top_scores()
            return False

        return True

    def draw_game(self, screen):
        # Draw paddles, ball, blocks, and score on the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, (self.paddle.position[0], HEIGHT - PADDLE_HEIGHT, self.paddle.width, PADDLE_HEIGHT))
        pygame.draw.circle(screen, BLUE, (int(self.ball.position[0]), int(self.ball.position[1])), self.ball.radius)

        for block in self.blocks:
            # Draw a black outline around the colored brick
            pygame.draw.rect(screen, BLACK, (block.position[0] - 1, block.position[1] - 1, block.width + 2, block.height + 2))
            pygame.draw.rect(screen, RED, (block.position[0], block.position[1], block.width, block.height))

        score_text = self.font.render(f"Score: {self.score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


class Play():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 600, 500
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = '8-BIT WONDER.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.topscores = TopScores(self)
        self.exit = Exit(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Breakout Game")
            clock = pygame.time.Clock()

            paddle = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, 10, [WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT])
            ball = Ball(BALL_RADIUS, 5, [random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS), HEIGHT // 2])

            num_cols = 10  # Set the desired number of columns
            num_rows = 4   # Set the desired number of rows

            # Adjust the Block creation in the main loop to calculate width dynamically
            blocks = [Block(num_cols, j, i) for j in range(num_rows) for i in range(num_cols)]

            game = Game(paddle, ball, blocks)

            while self.playing:  # Use self.playing as the condition for the outer loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    paddle.move_left()
                if keys[pygame.K_RIGHT]:
                    paddle.move_right()

                if not game.update_game():
                    # Reset the game state for a new round
                    paddle.position = [WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT]
                    ball.position = [random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS), HEIGHT // 2]
                    ball.direction = [1, -1]
                    blocks = [Block(num_cols, j, i) for j in range(num_rows) for i in range(num_cols)]
                    game.blocks = blocks
                    game.score = 0
                    self.curr_menu = self.main_menu
                    self.playing = False  # Exit the inner loop


                game.draw_game(screen)
                clock.tick(FPS)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

g = Play()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()