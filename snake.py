"""
SNAKE Game

A take on the classic snake game using Python 'pygame' module

In case of Game Over:
    press 'ENTER' to Start a New Game
    press 'ESC' to Exit
"""
import random

import pygame


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 127, 0)

# Dimensions : (Width, Height)
WIDTH, HEIGHT = (640, 360)

# Fonts
MSG_FONT = ('ubuntu', 40)
SCORE_FONT = ('Arial', 20)

# Snake Properties
PIXEL_SIZE = 10
SNAKE_SPEED = 20

# Creating Scores file, if it doesn't exist
with open("scores.txt", "a+") as f_scores:
    f_scores.seek(0)
    if not f_scores.readline():
        f_scores.write("MaxScore=0")

# Initializing pygame
pygame.init()

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
game_display.fill(BLACK)
pygame.display.set_caption("The Snake Game")

clock = pygame.time.Clock()

message_font = pygame.font.SysFont(*MSG_FONT)
score_font = pygame.font.SysFont(*SCORE_FONT)


def draw_pixel(pixel_x, pixel_y, size, color):
    """Draws a pixel on the game display"""
    pygame.draw.rect(game_display, color, (pixel_x, pixel_y, size, size))


def draw_snake(size, snake_pixels):
    """Draws the snake on the game display"""
    for pixel in snake_pixels:
        draw_pixel(pixel[0], pixel[1], size, GREEN)


def get_new_target():
    """Generates random coordinates for a new target"""
    target_x = (random.randrange(0, WIDTH - PIXEL_SIZE) // 10) * 10
    target_y = (random.randrange(0, HEIGHT - PIXEL_SIZE) // 10) * 10
    return (target_x, target_y)


def print_score(score):
    """Prints the user score"""
    text = score_font.render(f"Score : {score}", True, ORANGE)
    game_display.blit(text, [0, 0])


def print_max_score():
    """Compares and update the Max Score stored in scores.txt"""
    with open("scores.txt", "r+") as f_score:
        max_score = f_score.readline().split('=')[1]

    text = score_font.render(f"High Score : {max_score}", True, ORANGE)
    game_display.blit(text, (round(WIDTH*1.15) // 3, HEIGHT // 2))


def set_max_score(score):
    """Compares and update the Max Score stored in scores.txt"""
    with open("scores.txt", "r+") as f_score:
        prev_high = int(f_score.readline().split('=')[1])

        if score > prev_high:
            f_score.seek(0)
            f_score.truncate()
            f_score.write(f"MaxScore={score}")


def run_game():
    """Gameplay Logic"""
    game_exit = False
    game_over = False

    x_val = WIDTH // 8
    y_val = HEIGHT // 2

    x_speed, y_speed = PIXEL_SIZE, 0

    snake_pixels = []
    snake_length = 2

    target_pixel = get_new_target()

    while not game_exit:

        while game_over:
            game_over_message = message_font.render("Game Over!", True, RED)
            game_display.blit(game_over_message, (WIDTH / 3, HEIGHT / 3))
            print_score(snake_length - 2)
            set_max_score(snake_length - 2)
            print_max_score()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_display.fill(BLACK)
                        run_game()

                    elif event.key == pygame.K_ESCAPE:
                        game_exit = True
                        game_over = False

                elif event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False

        if game_exit:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            elif event.type == pygame.KEYDOWN:
                # Handling Key Presses for Snake Movement
                if event.key == pygame.K_UP and y_speed == 0:
                    x_speed, y_speed = 0, -PIXEL_SIZE
                elif event.key == pygame.K_DOWN and y_speed == 0:
                    x_speed, y_speed = 0, PIXEL_SIZE
                elif event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed, y_speed = -PIXEL_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed, y_speed = PIXEL_SIZE, 0

        if x_val not in range(0, WIDTH) or y_val not in range(0, HEIGHT):
            game_over = True

        # Moving the snake
        x_val += x_speed
        y_val += y_speed

        # Managing Snake Length
        snake_pixels.append([x_val, y_val])

        if len(snake_pixels) > snake_length:
            draw_pixel(snake_pixels[0][0],
                       snake_pixels[0][1], PIXEL_SIZE, BLACK)
            del snake_pixels[0]

        # Checking if the snake runs into itself
        for pixel in snake_pixels[:-1]:
            if pixel == [x_val, y_val] and len(snake_pixels) > 2:
                game_over = True
                break

        game_display.fill(BLACK)

        # Drawing Target        x                y
        draw_pixel(target_pixel[0], target_pixel[1], PIXEL_SIZE, WHITE)

        # Drawing Snake
        draw_snake(PIXEL_SIZE, snake_pixels)

        print_score(snake_length - 2)

        pygame.display.update()

        # Increasing Snake's length
        if target_pixel == (x_val, y_val):
            target_pixel = get_new_target()
            snake_length += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


if __name__ == "__main__":
    run_game()
