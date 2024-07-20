# necessery imports
import pygame
import random
import tkinter

# function to apply the settings will be enhanced later
def apply_settings(window, food_number, resizability, speed):
    global num_of_food, screen, frame_rate, end_screen
    # checking if the input is correct
    if int(food_number)  <= 0 or int(speed) <= 0:
        return
    # closing the settings window
    window.destroy()
    end_screen = False
    # changing the speed of the snake based on the input
    frame_rate = int(speed)
    # changing the number of food based on the input
    num_of_food = int(food_number)
    # changing the number of food on the screen based on the input
    food.clear()
    for i in range(num_of_food):
        food.append(Food(random.choice(row), random.choice(column)))
    # changing the resizability of the window based on the input
    if resizability:
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((800, 600))
    reset()

# function for the settings window
def settings_window():
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("600x300")
    window.resizable(False, False)
    window.iconbitmap("setting.ico")
    # creating a main label for the settings window
    main_label = tkinter.Label(window, text="Settings", font=("Arial", 20))
    main_label.pack(side="top")
    # creating a frame for the settings
    frame = tkinter.Frame(window)
    frame.pack(side="top")
    # creating a label for the number of food
    food_label = tkinter.Label(frame, text="Number of food:")
    food_label.grid(row=0, column=0)
    # creating a entry for the number of food
    e1 = tkinter.StringVar()
    e1.set(str(num_of_food))
    food_entry = tkinter.Entry(frame, textvariable=e1)
    food_entry.grid(row=0, column=1)
    # instructions for the user
    instructions_label = tkinter.Label(frame, text="*how many will be on the screen at the same time", fg="red")
    instructions_label.grid(row=0, column=2)
    # creating a label for the resizability of the window
    resizability_label = tkinter.Label(frame, text="Resizability:")
    resizability_label.grid(row=1, column=0)
    # creating a checkbutton for the resizability of the window
    resizability_var = tkinter.IntVar()
    resizability_checkbox = tkinter.Checkbutton(frame, variable=resizability_var)
    resizability_checkbox.grid(row=1, column=1)
    # instructions for the user
    instructions_label1 = tkinter.Label(frame, text="*if checked, the window will be resizable", fg="red")
    instructions_label1.grid(row=1, column=2)
    # creating a label for the speed of the snake
    speed_label = tkinter.Label(frame, text="Speed:")
    speed_label.grid(row=2, column=0)
    # creating a entry for the speed of the snake
    e2 = tkinter.StringVar()
    e2.set(str(frame_rate))
    speed_entry = tkinter.Entry(frame, textvariable=e2)
    speed_entry.grid(row=2, column=1)
    # instructions for the user
    instructions_label2 = tkinter.Label(frame, text="*Recommended speed is 6", fg="red")
    instructions_label2.grid(row=2, column=2)

    # creating apply button
    apply_button = tkinter.Button(window, text="Apply", width=10, height=2, command= lambda: apply_settings(window, food_entry.get(), resizability_var.get(), speed_entry.get()))
    apply_button.pack(side="bottom")
    window.mainloop()

# function to reset the game
def reset():
    global snake, food, current_direction, score, row, column, pixel_size, num_of_food
    global width, height
    # getting the width and height of the screen
    width = screen.get_width()
    height = screen.get_height()
    # resetting the row and column lists
    row.clear()
    column.clear()
    # getting the new pixel size
    pixel_size = width//40
    # getting all the possible positions for the apple and the snake with the new pixel size
    for i in range(width//pixel_size):
        row.append(i*pixel_size)
    for i in range(height//pixel_size):
        column.append(i*pixel_size)
    # resetting the food and snake
    food.clear()
    for i in range(num_of_food):
        food.append(Food(random.choice(row), random.choice(column)))
    snake = Snake(random.choice(row), random.choice(column), pixel_size)
    # resetting other variables
    current_direction = ""
    score = 0

# function for the game over screen
def game_over_screen():
    global running, end_screen
    end_screen = True
    # keeping the screen running in case player wants to restart the game or edit the settings
    while end_screen:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        # displaying the game over message
        text = font.render(f"Game Over! Your score is: {score}", True, (255, 255, 255))
        screen.blit(text, (width//2-text.get_width()//2, height//2-text.get_height()//2))
        settings_button = pygame.image.load("setting.png")
        screen.blit(settings_button, (width-settings_button.get_width()-10, 10))
        pygame.display.update()
        # event loop
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
                    if mouse_x > width-settings_button.get_width()-10 and mouse_x < width-10 and mouse_y > 10 and mouse_y < 10+settings_button.get_height():
                        settings_window()

# initialize pygame
pygame.init()
# setting up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
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
pixel_size = width//40
row = []
column = []
num_of_food = 1
# getting all the possible positions for the apple and the snake
for i in range(width//pixel_size):
    row.append(i*pixel_size)
for i in range(height//pixel_size):
    column.append(i*pixel_size)

# getting the starting position of the snake and the foods
snake = Snake(random.choice(row), random.choice(column), pixel_size)
food = []
for i in range(num_of_food):
    food.append(Food(random.choice(row), random.choice(column)))

# creating other variables
current_direction = ""
score = 0
pygame.clock = pygame.time.Clock()
frame_rate = 6
end_screen = False

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
    screen.blit(settings_button, (width-settings_button.get_width()-10, 10))

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # checking and changing the direction of the snake based on the key pressed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if current_direction != "down":
                    current_direction = "up"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if current_direction != "up":
                    current_direction = "down"
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if current_direction != "right":
                    current_direction = "left"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if current_direction != "left":
                    current_direction = "right"
            if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                reset()
        # checking if the settings button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > width-settings_button.get_width()-10 and mouse_x < width-10 and mouse_y > 10 and mouse_y < 10+settings_button.get_height():
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
    if snake.x < 0 or snake.x > width or snake.y < 0 or snake.y > height:
        game_over_screen()
    
    # checking if the snake hit itself
    for i in snake.body:
        if snake.body.count(i) > 1:
            game_over_screen()
    
    # checking if the snake ate at least one food
    #print(food)
    for i in food:
        if snake.x == i.x and snake.y == i.y:
            food.remove(i)
            food.append(Food(random.choice(row), random.choice(column)))
            score += 1

    # drawing the foods
    for i in food:
        i.draw()

    # drawing the snake and updating the body
    snake.body.append((snake.x, snake.y))
    if len(snake.body) > score+1:
        snake.body.pop(0)
    snake.draw()

    # setting the frame rate
    pygame.clock.tick(frame_rate)

    # update the screen
    pygame.display.update()

# quiting the game
pygame.quit()