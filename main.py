# necessery imports
import pygame
import random
import tkinter

# function to apply the settings will be enhanced later
def apply_settings(window):
    window.destroy()
    reset()

# function for the settings window
def settings_window():
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("300x300")
    window.resizable(False, False)
    window.iconbitmap("setting.ico")
    # creating a main label for the settings window
    main_label = tkinter.Label(window, text="Settings", font=("Arial", 20))
    main_label.pack(side="top")

    # creating apply button
    apply_button = tkinter.Button(window, text="Apply", width=10, height=2, command= lambda: apply_settings(window))
    apply_button.pack(side="bottom")
    window.mainloop()

# function to reset the game
def reset():
    global snake, food, current_direction, score
    snake = Snake(random.choice(row), random.choice(column), pixel_size)
    food = Food(random.choice(row), random.choice(column))
    current_direction = ""
    score = 0

# function for the game over screen
def game_over_screen():
    global running
    end_screen = True
    # keeping the screen running in case player wants to restart the game or edit the settings
    while end_screen:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Your score is: {score}", True, (255, 255, 255))
        screen.blit(text, (800//2-text.get_width()//2, 600//2-text.get_height()//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                    reset()
                    end_screen = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x > 800//2-text.get_width()//2 and mouse_x < 800//2+text.get_width()//2 and mouse_y > 600//2-text.get_height()//2 and mouse_y < 600//2+text.get_height()//2:
                        settings_window()
                        end_screen = False

# initialize pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600))
# setting up the title and icon
pygame.display.set_caption("Snake Game")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)
settings_button = pygame.image.load("setting.png")

    # classes
# snake class
class Snake:
    def __init__(self, x, y, pixel_size):
        self.x = x
        self.y = y
        self.speed = pixel_size
        # list to store the snake's body
        self.body = []
        self.body.append((self.x, self.y))
    def draw(self):
        for i in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (i[0], i[1], pixel_size, pixel_size))

# food class
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, pixel_size, pixel_size))

# variables
pixel_size = 30
row = []
column = []
# getting all the possible positions for the apple and the snake
for i in range(800//pixel_size):
    row.append(i*pixel_size)
for i in range(600//pixel_size):
    column.append(i*pixel_size)

snake = Snake(random.choice(row), random.choice(column), pixel_size)
food = Food(random.choice(row), random.choice(column))
current_direction = ""
score = 0
pygame.clock = pygame.time.Clock()

# main game loop
running = True
while running:
    # setting up the background color
    screen.fill((0, 0, 0))

    # drawing the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # drawing the settings button
    screen.blit(settings_button, (800-settings_button.get_width()-10, 10))

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                current_direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                current_direction = "down"
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                current_direction = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                current_direction = "right"
            if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                reset()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 800-settings_button.get_width()-10 and mouse_x < 800-10 and mouse_y > 10 and mouse_y < 10+settings_button.get_height():
                    settings_window()

    # moving the snake based on the current direction
    if current_direction == "up":
        snake.y -= snake.speed
    if current_direction == "down":
        snake.y += snake.speed
    if current_direction == "left":
        snake.x -= snake.speed
    if current_direction == "right":
        snake.x += snake.speed

    # checking if the snake hit a wall
    if snake.x < 0 or snake.x > 800 or snake.y < 0 or snake.y > 600:
        game_over_screen()
    
    # checking if the snake ate the food
    if snake.x == food.x and snake.y == food.y:
        food = Food(random.choice(row), random.choice(column))
        score += 1

    # drawing the food
    food.draw()

    # drawing the snake(new version of the code)
    snake.body.append((snake.x, snake.y))
    if len(snake.body) > score+1:
        snake.body.pop(0)
    snake.draw()

         # original code
    #if len(snake.body) > score+1:
    #    snake.body.pop(0)
    #for i in snake.body:
    #    pygame.draw.rect(screen, (0, 255, 0), (i[0], i[1], pixel_size, pixel_size))

    # setting the frame rate
    pygame.clock.tick(6)

    # update the screen
    pygame.display.update()

# quiting the game
pygame.quit()