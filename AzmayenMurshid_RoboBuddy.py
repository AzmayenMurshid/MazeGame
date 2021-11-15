import turtle
import time as tm
import math as mt
import random

from RoboBuddyASCII_Levels import *

# Screen SetUp
win = turtle.Screen()
win.bgcolor("black")
win.title("RoboBuddy")

# Set Size of window
win.setup(width=1.0, height=1.0)

# removing navigation buttons (close, minimize, maximize buttons)
canvas = win.getcanvas()
root = canvas.winfo_toplevel()
root.overrideredirect(1)

# creating Class
class RB(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


# Creating the User class
class User(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("cyan")
        self.penup()
        self.speed(0)

    def up(self):
        try:
            # Calculate the spot to move to
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 24

            # Check if the space has walls
            if (move_to_x, move_to_y) not in walls:
                self.goto(move_to_x, move_to_y)

        except Exception:
            print("Game closed")

    def down(self):
        try:
            move_to_x = self.xcor()
            move_to_y = self.ycor() - 24

            if (move_to_x, move_to_y) not in walls:
                self.goto(move_to_x, move_to_y)

        except Exception:
            print("Game closed")

    def left(self, **kwargs):
        try:
            move_to_x = self.xcor() - 24
            move_to_y = self.ycor()

            # Check if the space has walls
            if (move_to_x, move_to_y) not in walls:
                self.goto(move_to_x, move_to_y)

        except Exception:
            print("Game closed")

    def right(self, **kwargs):
        try:
            move_to_x = self.xcor() + 24
            move_to_y = self.ycor()

            # Check if the space has walls
            if (move_to_x, move_to_y) not in walls:
                self.goto(move_to_x, move_to_y)

        except Exception:
            print("Game closed")

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        dist = mt.sqrt((a ** 2) + (b ** 2))

        if dist == 0:
            return True
        else:
            return False


class Vortex(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("purple")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
            self.shape("square")
        elif self.direction == "right":
            dx = 24
            dy = 0
            self.shape("square")
        else:
            dx = 0
            dy = 0

        # Check if user is close
        # if so, chase the user
        if self.is_close(user):
            if user.xcor() < self.xcor():
                self.direction = "left"
            elif user.xcor() > self.xcor():
                self.direction = "right"
            elif user.ycor() < self.ycor():
                self.direction = "down"
            elif user.ycor() > self.ycor():
                self.direction = "up"

        # Calculate the spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # Check if the space has walls
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            # Chose a different direction
            self.direction = random.choice(["up", "down", "left", "right"])

        # Set Timer to move next time
        turtle.ontimer(self.move, t=random.randint(100, 300))  # --> Change speed if you feel like it

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        dist = mt.sqrt((a ** 2) + (b ** 2))

        if dist < 75:  # --:> Change the number if you think the distance between the user and enemy is too far
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# Create levels list & add r1 to the list
rooms = ["", r1]

# Create room SetUp Function
try:
    def setup_room(room):
        for y in range(len(room)):
            for x in range(len(room[y])):
                # Get the character at each (x,y) coordinates
                # NOTE the order of y and x in the next line
                character = room[y][x]
                # Calculate the Screen (x,y) coordinates
                screen_x = -288 + (x * 24)
                screen_y = 288 - (y * 24)

                # Check if there is an X (representing the wall)
                if character == "X":
                    rb.goto(screen_x, screen_y)
                    rb.shape("square")
                    rb.stamp()
                    # Add coordinates to wall list
                    walls.append((screen_x, screen_y))

                # Check if it is a U (representing the User)
                elif character == "U":
                    user.goto(screen_x, screen_y)

                # Check if the character is T (representing Treasure)
                elif character == "V":
                    vortexes.append(Vortex(screen_x, screen_y))

                # Check if the character is T (representing Enemy)
                elif character == "E":
                    enemies.append(Enemy(screen_x, screen_y))


except Exception:
    print("Game closed")

# Creating class instances
rb = RB()
user = User()

# Creating wall coordinate list to contain walls coordinate
walls = []

# Vortexes List to contain vortex coordinate
vortexes = []

# Creating Enemies list
enemies = []

# Terminal Data
# print(walls, finish, LvlChange, treasures) --> Uncomment when needed

# Set up the room
setup_room(rooms[1])

# keyboard Bindings
try:
    turtle.listen()
    turtle.onkey(user.left, "Left")
    turtle.onkey(user.right, "Right")
    turtle.onkey(user.up, "Up")
    turtle.onkey(user.down, "Down")
except Exception:
    print("Game closed")

# Turn off screen updates
win.tracer(0)

# Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=150)  # --> Change speed if feel like it

# Main Game Loop
try:
    while True:
        # Check for player collision with treasure
        # Iterate through treasure list
        for treasure in vortexes:
            if user.is_collision(treasure):
                # print("Player Gold: {}".format(user.gold)) --> Uncomment when needed
                # Destroy the treasure
                treasure.destroy()
                # Remove the treasure from the treasures list
                vortexes.remove(treasure)
                # Transition to next page
                tm.sleep(0.5)
                win.clearscreen()
                win.bgcolor("black")
                turtle.color('cyan')
                style = ('Courier', 30, 'bold')
                turtle.write('Congratulations! RoboBuddy Got to the Vortex!', font=style, align='center')
                # Quit Game
                tm.sleep(5)
                exit()
        for enemy in enemies:
            if user.is_collision(enemy):
                tm.sleep(0.2)
                win.clearscreen()
                win.bgcolor("black")
                turtle.color('cyan')
                style = ('Courier', 30, 'bold')
                turtle.write('RoboBuddy Died! GAME OVER', font=style, align='center')

                # Quit Game
                tm.sleep(5)
                exit()

        # Update screen
        win.update()
except Exception:
    print("Game closed")
