import pygame
import time
import random
from datetime import datetime


def main():

    # Variables of the size of the window
    width = 504
    height = 504

    # Making the screen with the width and height
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Makes the board array with nothing on it and a clean board to reset
    board = [
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""]
    ]

    # Makes the pygame window and captions it snake
    pygame.display.set_caption('Snake')
    pygame.init()

    # Setting up variables needed for the running
    run = True
    left = False
    right = False
    snake_parts = [[6, 4], [6, 5], [6, 6]]
    up = False
    down = False
    apple_on = False
    apple_location = None

    # Creating variable to show the frame rate
    frames = 0
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    fps = 30

    # Creating the class for the snake to make the code more understandable
    class Snake:
        def __init__(self, snake_body, snake_direction="up", moved=False, move_counter=0.0, add=False):
            self.snake_body = snake_body
            self.snake_length = len(self.snake_body)
            self.snake_direction = snake_direction
            self.moved = moved
            self.move_counter = move_counter
            self.add = add

        # Check whether the snake should die
        def check_hit(self):

            # Checks whether the snake has hit itself
            for o in range(self.snake_length - 1):
                if self.snake_body[o + 1] == self.snake_body[0]:
                    return False

            # Checks whether the snake has gone out of bounds
            if not -1 < self.snake_body[0][0] < 12 or not -1 < self.snake_body[0][1] < 12:
                return False

            # If the snake has not hit itself or gone out of bounds then it returns True
            return True

        # Changes the direction based on which key is pressed
        def change_direction(self):
            if not self.moved:
                if up:
                    if not self.snake_direction == "down":
                        self.snake_direction = "up"
                        self.moved = True
                elif left:
                    if not self.snake_direction == "right":
                        self.snake_direction = "left"
                        self.moved = True
                elif right:
                    if not self.snake_direction == "left":
                        self.snake_direction = "right"
                        self.moved = True
                elif down:
                    if not self.snake_direction == "up":
                        self.snake_direction = "down"
                        self.moved = True

        # A function to move the snake a tile when the timer is right
        def move(self):
            if self.move_counter >= 0.2:
                o = self.snake_length - 1
                saved = None

                # Saves the end of the snake
                if self.add:
                    saved = [self.snake_body[o][0], self.snake_body[o][1]]

                # Moves the snake forward
                while o > 0:
                    self.snake_body[o][1] = self.snake_body[o - 1][1]
                    self.snake_body[o][0] = self.snake_body[o - 1][0]
                    o -= 1

                # Adds a tile to where the previous last one was
                if self.add:
                    self.snake_body.append(saved)
                    self.add = False

                # Moves the head of the snake in the right direction
                if self.snake_direction == "up":
                    self.snake_body[0][1] -= 1
                elif self.snake_direction == "left":
                    self.snake_body[0][0] -= 1
                elif self.snake_direction == "right":
                    self.snake_body[0][0] += 1
                elif self.snake_direction == "down":
                    self.snake_body[0][1] += 1
                self.moved = False
                self.move_counter = 0

                # Variable for the correct size boxes
                position_x = width/12
                position_y = height/12
                box_width = width/12 - 2 * (width/504)
                box_height = height/12 - 2 * (height/504)

                # Draws a grid with grey as an empty tile and red where the snake is
                for o in range(len(board)):
                    for q in range(len(board[o])):
                        if board[o][q] == "":
                            pygame.draw.rect(screen, (175, 167, 169), pygame.Rect(q * position_x, o * position_y,
                                                                                  box_width, box_height))
                        elif board[o][q] == "x":
                            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(q * position_x, o * position_y,
                                                                              box_width, box_height))
                        elif board[o][q] == "o":
                            pygame.draw.rect(screen, (35, 255, 0), pygame.Rect(q * position_x, o * position_y,
                                                                               box_width, box_height))

                # Updates the display on the pygame window
                pygame.display.update()

        # A function to add a tile to the snake
        def increase_length(self):
            self.add = True

    # Initialises the player as a snake object
    player = Snake(snake_parts)

    # Makes the background colour black
    screen.fill((0, 0, 0))
    while run:
        start = time.time()

        # Gets the time at every frame
        now = datetime.now()
        if not current_time == now.strftime("%H:%M:%S"):
            print(f'There are {frames} fps')
            frames = 0
            current_time = now.strftime("%H:%M:%S")

        # Updates the snake length variable to the actual length of the snake
        player.snake_length = len(player.snake_body)

        # Changes the board array depending on where the snake and the apple are
        for i in range(len(board)):
            for j in range(len(board[i])):
                if [j, i] in player.snake_body:
                    if board[i][j] == "":
                        board[i][j] = "x"
                else:
                    if board[i][j] == "o":
                        board[i][j] = "o"
                    else:
                        board[i][j] = ""

        # If there is not an apple on the screen it makes a new one
        if not apple_on:
            apple_x = random.choice(range(0, 11))
            apple_y = random.choice(range(0, 11))
            if board[apple_y][apple_x] == "":
                board[apple_y][apple_x] = "o"
                apple_location = [apple_y, apple_x]
            while board[apple_y][apple_x] == "x":
                apple_x = random.choice(range(0, 11))
                apple_y = random.choice(range(0, 11))
                if board[apple_y][apple_x] == "":
                    board[apple_y][apple_x] = "o"
                    apple_location = [apple_y, apple_x]
            apple_on = True

        # Checks whether the snake has hit the apple and if it has it removes the apple and makes the snake longer
        if apple_location[0] == player.snake_body[0][1] and apple_location[1] == player.snake_body[0][0]:
            board[apple_location[0]][apple_location[1]] = ""
            apple_on = False
            player.increase_length()

        # Check whether the snake is has hit itself
        run = player.check_hit()

        # Changes the direction based on which key is pressed
        player.change_direction()

        # If the snake needs to move it moves if then resets the counter
        player.move()

        # Loops through the pygame events each frame and checks for specific ones
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Checking whether a key has been pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                # Checks whether any movement keys have been pressed and changes the values accordingly
                elif event.key == pygame.K_a:
                    left = True
                elif event.key == pygame.K_d:
                    right = True
                elif event.key == pygame.K_w:
                    up = True
                elif event.key == pygame.K_s:
                    down = True

            # Checks whether a key has been lifted up
            if event.type == pygame.KEYUP:

                # When the movement keys are lifted up the values are changed accordingly
                if event.key == pygame.K_a:
                    left = False
                elif event.key == pygame.K_d:
                    right = False
                elif event.key == pygame.K_w:
                    up = False
                elif event.key == pygame.K_s:
                    down = False

            # Checks whether the window has been resized
            if event.type == pygame.VIDEORESIZE:
                # Updates the width and height values when the window is resized
                width = event.w
                height = event.h

        # Updates the move counter
        player.move_counter += 1/fps
        print(snake_parts[0][0], snake_parts[0][1])

        # Adds a frame to the frame counter
        frames += 1

        # Records the time at the end and wait until it needs to do the next frame, this makes the frame rate consistent
        end = time.time()
        if ((1/fps) - (end-start)) > 0:
            time.sleep((1/fps) - (end-start))


if __name__ == '__main__':
    main()
