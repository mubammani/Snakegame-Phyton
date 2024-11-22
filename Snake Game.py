import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [[100, 100], [80, 100], [60, 100]]  # Initial snake position
        self.direction = "RIGHT"  # Initial direction

    def move(self):
        head = self.body[0]
        if self.direction == "UP":
            new_head = [head[0], head[1] - CELL_SIZE]
        elif self.direction == "DOWN":
            new_head = [head[0], head[1] + CELL_SIZE]
        elif self.direction == "LEFT":
            new_head = [head[0] - CELL_SIZE, head[1]]
        elif self.direction == "RIGHT":
            new_head = [head[0] + CELL_SIZE, head[1]]

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        # Check collision with walls
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        # Check collision with itself
        if head in self.body[1:]:
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        return [
            random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
        ]

    def respawn(self, snake_body):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break

# Snake Game class
class SnakeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def draw_snake(self):
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    def draw_food(self):
        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food.position[0], self.food.position[1], CELL_SIZE, CELL_SIZE))

    def display_score(self):
        font = pygame.font.SysFont("arial", 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        running = True

        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Restart game if "R" is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()  # Reset the game state

                    # Handle movement keys
                    if not self.game_over:
                        if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                            self.snake.direction = "UP"
                        elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                            self.snake.direction = "DOWN"
                        elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                            self.snake.direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                            self.snake.direction = "RIGHT"

            if not self.game_over:
                self.snake.move()

                # Check if the snake eats the food
                if self.snake.body[0] == self.food.position:
                    self.snake.grow()
                    self.food.respawn(self.snake.body)
                    self.score += 1

                # Check for collisions
                if self.snake.check_collision():
                    self.game_over = True

            # Draw everything
            self.draw_snake()
            self.draw_food()
            self.display_score()

            if self.game_over:
                font = pygame.font.SysFont("arial", 36)
                game_over_text = font.render("Game Over! Press R to Restart", True, RED)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
